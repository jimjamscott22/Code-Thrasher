"""Subprocess-based Python runner with timeout and output limits."""

from __future__ import annotations

import asyncio
import sys
import textwrap
from dataclasses import dataclass

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


def _run_python_sync(
    code: str,
    input_data: str,
    timeout_seconds: int,
    max_output_bytes: int,
    max_memory_mb: int,
) -> SandboxRunResult:
    import subprocess

    wrapper = textwrap.dedent(
        f"""
        import sys
        from io import StringIO

        sys.stdin = StringIO({input_data!r})
        """
    ).strip()
    full_code = f"{wrapper}\n{code}"

    preexec = None
    if sys.platform != "win32":
        import resource

        max_memory_bytes = max_memory_mb * 1024 * 1024

        def _set_limits() -> None:
            resource.setrlimit(resource.RLIMIT_AS, (max_memory_bytes, max_memory_bytes))

        preexec = _set_limits

    try:
        completed = subprocess.run(
            [sys.executable, "-c", full_code],
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            preexec_fn=preexec,
        )
    except subprocess.TimeoutExpired:
        return SandboxRunResult(
            stdout="",
            stderr="Execution timed out",
            timed_out=True,
            output_truncated=False,
        )

    stdout, stdout_truncated = _truncate_output(completed.stdout, max_output_bytes)
    stderr, stderr_truncated = _truncate_output(completed.stderr, max_output_bytes)
    output_truncated = stdout_truncated or stderr_truncated

    if output_truncated and not stderr:
        stderr = f"Output exceeded {max_output_bytes} byte limit"

    return SandboxRunResult(
        stdout=stdout,
        stderr=stderr,
        timed_out=False,
        output_truncated=output_truncated,
    )


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
