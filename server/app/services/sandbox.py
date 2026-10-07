"""Subprocess-based code runners (Python, Rust, JavaScript) with timeout and output limits."""

from __future__ import annotations

import asyncio
import shutil
import subprocess
import sys
import tempfile
import textwrap
from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import asynccontextmanager
from dataclasses import dataclass
from pathlib import Path

from app.core.config import settings


@dataclass
class SandboxRunResult:
    stdout: str
    stderr: str
    timed_out: bool
    output_truncated: bool


def _truncate_output(text: str, max_bytes: int) -> tuple[str, bool]:
    encoded = text.encode("utf-8", errors="replace")
    if len(encoded) <= max_bytes:
        return text, False
    truncated = encoded[:max_bytes].decode("utf-8", errors="ignore")
    return truncated, True


def _memory_limiter(max_memory_mb: int) -> Callable[[], None] | None:
    if sys.platform == "win32":
        return None

    import resource

    max_memory_bytes = max_memory_mb * 1024 * 1024

    def _set_limits() -> None:
        resource.setrlimit(resource.RLIMIT_AS, (max_memory_bytes, max_memory_bytes))

    return _set_limits


def _timed_out_result(message: str = "Execution timed out") -> SandboxRunResult:
    return SandboxRunResult(
        stdout="", stderr=message, timed_out=True, output_truncated=False
    )


def _result_from_completed(
    completed: subprocess.CompletedProcess[str],
    max_output_bytes: int,
    max_memory_mb: int,
) -> SandboxRunResult:
    stdout, stdout_truncated = _truncate_output(completed.stdout, max_output_bytes)
    stderr, stderr_truncated = _truncate_output(completed.stderr, max_output_bytes)
    output_truncated = stdout_truncated or stderr_truncated

    if output_truncated and not stderr:
        stderr = f"Output exceeded {max_output_bytes} byte limit"

    # A process killed by a signal (returncode < 0) often produces no stderr —
    # e.g. RLIMIT_AS exhaustion crashes the interpreter. Surface it as an error
    # so grading never mistakes a sandbox failure for an empty (wrong) answer.
    if completed.returncode < 0 and not stderr:
        stderr = (
            f"Process terminated by signal {-completed.returncode} "
            f"(possible memory limit of {max_memory_mb} MB exceeded)"
        )

    return SandboxRunResult(
        stdout=stdout,
        stderr=stderr,
        timed_out=False,
        output_truncated=output_truncated,
    )


def _run_python_sync(
    code: str,
    input_data: str,
    timeout_seconds: int,
    max_output_bytes: int,
    max_memory_mb: int,
) -> SandboxRunResult:
    wrapper = textwrap.dedent(
        f"""
        import sys
        from io import StringIO

        sys.stdin = StringIO({input_data!r})
        """
    ).strip()
    full_code = f"{wrapper}\n{code}"

    try:
        completed = subprocess.run(
            [sys.executable, "-c", full_code],
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            preexec_fn=_memory_limiter(max_memory_mb),
        )
    except subprocess.TimeoutExpired:
        return _timed_out_result()

    return _result_from_completed(completed, max_output_bytes, max_memory_mb)


async def run_python(
    code: str,
    input_data: str = "",
    *,
    timeout_seconds: int | None = None,
    max_output_bytes: int | None = None,
    max_memory_mb: int | None = None,
) -> SandboxRunResult:
    return await asyncio.to_thread(
        _run_python_sync,
        code,
        input_data,
        timeout_seconds or settings.SANDBOX_TIMEOUT_SECONDS,
        max_output_bytes or settings.SANDBOX_MAX_OUTPUT_BYTES,
        max_memory_mb or settings.SANDBOX_MAX_MEMORY_MB,
    )


# ── Rust ─────────────────────────────────────────────────────────────────────

RunFn = Callable[[str], Awaitable[SandboxRunResult]]

# An asyncio.Semaphore binds to the event loop it first waits on, so keep one per
# (running loop, limit) rather than a single module-level instance. In production
# there is one loop and one limit, so this is just a lazily created singleton.
_compile_slots: tuple[asyncio.AbstractEventLoop, int, asyncio.Semaphore] | None = None


def _compile_semaphore() -> asyncio.Semaphore:
    global _compile_slots
    loop = asyncio.get_running_loop()
    limit = max(1, settings.SANDBOX_RUST_MAX_CONCURRENT_COMPILES)
    if _compile_slots is None or _compile_slots[:2] != (loop, limit):
        _compile_slots = (loop, limit, asyncio.Semaphore(limit))
    return _compile_slots[2]


def _compile_rust_sync(
    code: str,
    workdir: Path,
    timeout_seconds: int,
    max_output_bytes: int,
) -> SandboxRunResult | None:
    """Compile ``code`` to ``workdir/main``. Returns None on success, else the failure."""
    source = workdir / "main.rs"
    source.write_text(code, encoding="utf-8")

    # No memory rlimit here: rustc maps far more address space than it uses.
    # Warnings are silenced so they are never mistaken for a failed run.
    try:
        completed = subprocess.run(
            [
                "rustc",
                "--edition=2021",
                "-A",
                "warnings",
                "--color=never",
                "-o",
                str(workdir / "main"),
                str(source),
            ],
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            cwd=workdir,
        )
    except FileNotFoundError:
        return SandboxRunResult(
            stdout="",
            stderr="Rust toolchain (rustc) is not installed on the server",
            timed_out=False,
            output_truncated=False,
        )
    except subprocess.TimeoutExpired:
        return _timed_out_result("Compilation timed out")

    if completed.returncode == 0:
        return None

    message = completed.stderr.replace(str(source), "main.rs") or "Compilation failed"
    stderr, _ = _truncate_output(message, max_output_bytes)
    return SandboxRunResult(
        stdout="", stderr=stderr, timed_out=False, output_truncated=False
    )


def _run_rust_binary_sync(
    workdir: Path,
    input_data: str,
    timeout_seconds: int,
    max_output_bytes: int,
    max_memory_mb: int,
) -> SandboxRunResult:
    try:
        completed = subprocess.run(
            [str(workdir / "main")],
            input=input_data,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            cwd=workdir,
            preexec_fn=_memory_limiter(max_memory_mb),
        )
    except subprocess.TimeoutExpired:
        return _timed_out_result()

    return _result_from_completed(completed, max_output_bytes, max_memory_mb)


@asynccontextmanager
async def rust_runner(
    code: str,
    *,
    timeout_seconds: int | None = None,
    max_output_bytes: int | None = None,
    max_memory_mb: int | None = None,
) -> AsyncIterator[RunFn]:
    """Compile ``code`` once and yield a function that runs it on given stdin.

    If compilation fails, the yielded function returns the compiler error for
    every input, so callers can treat it like any other failing run.
    """
    timeout = timeout_seconds or settings.SANDBOX_TIMEOUT_SECONDS
    max_bytes = max_output_bytes or settings.SANDBOX_MAX_OUTPUT_BYTES
    max_mem = max_memory_mb or settings.SANDBOX_MAX_MEMORY_MB

    with tempfile.TemporaryDirectory(prefix="code-thrasher-rust-") as tmp:
        workdir = Path(tmp)
        async with _compile_semaphore():
            failure = await asyncio.to_thread(
                _compile_rust_sync,
                code,
                workdir,
                settings.SANDBOX_RUST_COMPILE_TIMEOUT_SECONDS,
                max_bytes,
            )

        async def run(input_data: str = "") -> SandboxRunResult:
            if failure is not None:
                return failure
            return await asyncio.to_thread(
                _run_rust_binary_sync, workdir, input_data, timeout, max_bytes, max_mem
            )

        yield run


async def run_rust(code: str, input_data: str = "", **limits: int) -> SandboxRunResult:
    async with rust_runner(code, **limits) as run:
        return await run(input_data)


def rust_available() -> bool:
    return shutil.which("rustc") is not None


# ── JavaScript ───────────────────────────────────────────────────────────────

# V8 reserves several hundred MB of address space for JIT code at startup, which
# trips the RLIMIT_AS cap before any user code runs. --jitless skips that
# reservation (and WebAssembly, hence --no-expose-wasm, which would otherwise
# print a warning), so Node runs under the same memory cap as everything else.
# Runtime warnings are silenced so they are never mistaken for a failed run.
NODE_FLAGS = ["--jitless", "--no-expose-wasm", "--no-warnings"]


def _clean_node_stderr(stderr: str, source: str) -> str:
    """Point error traces at main.js and drop stack frames inside Node itself."""
    lines = stderr.replace(source, "main.js").splitlines(keepends=True)
    return "".join(
        line
        for line in lines
        if not (line.lstrip().startswith("at ") and "node:" in line)
        and not line.startswith("Node.js v")
    )


def _run_javascript_sync(
    code: str,
    input_data: str,
    timeout_seconds: int,
    max_output_bytes: int,
    max_memory_mb: int,
) -> SandboxRunResult:
    with tempfile.TemporaryDirectory(prefix="code-thrasher-js-") as tmp:
        source = Path(tmp) / "main.js"
        source.write_text(code, encoding="utf-8")
        try:
            completed = subprocess.run(
                ["node", *NODE_FLAGS, str(source)],
                input=input_data,
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
                cwd=tmp,
                preexec_fn=_memory_limiter(max_memory_mb),
            )
        except FileNotFoundError:
            return SandboxRunResult(
                stdout="",
                stderr="JavaScript runtime (node) is not installed on the server",
                timed_out=False,
                output_truncated=False,
            )
        except subprocess.TimeoutExpired:
            return _timed_out_result()

    completed.stderr = _clean_node_stderr(completed.stderr, str(source))
    return _result_from_completed(completed, max_output_bytes, max_memory_mb)


async def run_javascript(
    code: str,
    input_data: str = "",
    *,
    timeout_seconds: int | None = None,
    max_output_bytes: int | None = None,
    max_memory_mb: int | None = None,
) -> SandboxRunResult:
    return await asyncio.to_thread(
        _run_javascript_sync,
        code,
        input_data,
        timeout_seconds or settings.SANDBOX_TIMEOUT_SECONDS,
        max_output_bytes or settings.SANDBOX_MAX_OUTPUT_BYTES,
        max_memory_mb or settings.SANDBOX_MAX_MEMORY_MB,
    )


def node_available() -> bool:
    return shutil.which("node") is not None


@asynccontextmanager
async def code_runner(language: str, code: str) -> AsyncIterator[RunFn]:
    """Yield ``run(input_data)`` for the exercise's language."""
    if language == "rust":
        async with rust_runner(code) as run:
            yield run
    elif language == "javascript":

        async def run(input_data: str = "") -> SandboxRunResult:
            return await run_javascript(code, input_data)

        yield run
    else:

        async def run(input_data: str = "") -> SandboxRunResult:
            return await run_python(code, input_data)

        yield run
