"""
Secure Python execution sandbox.

Strategy:
  1. AST pre-scan — block dangerous imports and builtins before execution.
  2. Child subprocess — code never runs in the API process.
  3. resource limits — memory and CPU capped via the `resource` module.
  4. signal.alarm timeout — hard kill if the subprocess exceeds wall-clock limit.
  5. Temp working directory — subprocess cwd is an isolated tmpdir.

For production, replace the subprocess runner with a Docker container per
submission (exec into a pre-warmed container with seccomp/no-network).
"""

import ast
import resource
import subprocess
import sys
import tempfile
import textwrap
import time
from dataclasses import dataclass

from app.core.config import settings

# Modules that must never be importable in user code.
BLOCKED_MODULES = frozenset(
    [
        "os", "sys", "subprocess", "socket", "shutil", "pathlib",
        "importlib", "ctypes", "multiprocessing", "threading",
        "signal", "resource", "pty", "tty", "termios",
        "fcntl", "mmap", "gc", "builtins", "code", "codeop",
        "compileall", "py_compile", "pickletools", "pickle",
        "shelve", "dbm", "sqlite3", "urllib", "http", "ftplib",
        "smtplib", "poplib", "imaplib", "xmlrpc", "asyncio",
        "concurrent", "selectors", "ssl", "hashlib",
    ]
)

# Built-in names that must not be callable in user code.
BLOCKED_BUILTINS = frozenset(
    ["__import__", "open", "exec", "eval", "compile", "breakpoint", "input"]
)


@dataclass
class SandboxResult:
    stdout: str
    stderr: str
    timed_out: bool
    time_taken_ms: int


def _validate_ast(code: str) -> str | None:
    """Return an error message if the code fails static analysis, else None."""
    try:
        tree = ast.parse(code)
    except SyntaxError as exc:
        return f"SyntaxError: {exc}"

    for node in ast.walk(tree):
        # Block import statements for blocked modules.
        if isinstance(node, ast.Import):
            for alias in node.names:
                root = alias.name.split(".")[0]
                if root in BLOCKED_MODULES:
                    return f"ImportError: module '{alias.name}' is not allowed"
        elif isinstance(node, ast.ImportFrom):
            root = (node.module or "").split(".")[0]
            if root in BLOCKED_MODULES:
                return f"ImportError: module '{node.module}' is not allowed"
        # Block calls to forbidden builtins by name.
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id in BLOCKED_BUILTINS:
                return f"SecurityError: '{node.func.id}' is not allowed"
            if (
                isinstance(node.func, ast.Attribute)
                and node.func.attr in BLOCKED_BUILTINS
            ):
                return f"SecurityError: '{node.func.attr}' is not allowed"

    return None


_RUNNER_TEMPLATE = textwrap.dedent(
    """\
    import resource, signal, sys

    # Hard memory cap — RLIMIT_AS covers virtual address space.
    resource.setrlimit(resource.RLIMIT_AS, ({mem}, {mem}))
    # Hard CPU time cap (seconds).
    resource.setrlimit(resource.RLIMIT_CPU, ({cpu}, {cpu}))
    # Prevent fork bombs.
    resource.setrlimit(resource.RLIMIT_NPROC, (0, 0))

    # Redirect stdin to /dev/null so code can't read terminal input.
    sys.stdin = open("/dev/null", "r")

    # ── user code begins ──
    {code}
    """
)


def run_in_sandbox(code: str, stdin_data: str = "") -> SandboxResult:
    """
    Execute *code* in an isolated subprocess.

    Security measures applied:
    - AST import/builtin blacklist checked before spawning the process.
    - Child process sets its own resource limits (memory, CPU, no-fork).
    - Wall-clock timeout enforced via subprocess.communicate(timeout=…).
    - Runs in a fresh tmpdir so the CWD contains nothing sensitive.
    - stdout/stderr are captured and truncated to SANDBOX_MAX_OUTPUT_BYTES.
    """
    ast_error = _validate_ast(code)
    if ast_error:
        return SandboxResult(
            stdout="",
            stderr=ast_error,
            timed_out=False,
            time_taken_ms=0,
        )

    mem_bytes = settings.SANDBOX_MAX_MEMORY_MB * 1024 * 1024
    wrapper = _RUNNER_TEMPLATE.format(
        mem=mem_bytes,
        cpu=settings.SANDBOX_TIMEOUT_SECONDS,
        code=textwrap.indent(code, "    "),
    )

    start = time.monotonic()
    timed_out = False

    with tempfile.TemporaryDirectory() as tmpdir:
        try:
            proc = subprocess.run(
                [sys.executable, "-c", wrapper],
                input=stdin_data,
                capture_output=True,
                text=True,
                timeout=settings.SANDBOX_TIMEOUT_SECONDS + 1,  # wall-clock grace
                cwd=tmpdir,
            )
            stdout = proc.stdout[: settings.SANDBOX_MAX_OUTPUT_BYTES]
            stderr = proc.stderr[: settings.SANDBOX_MAX_OUTPUT_BYTES]
        except subprocess.TimeoutExpired as exc:
            timed_out = True
            stdout = (exc.stdout or b"")[: settings.SANDBOX_MAX_OUTPUT_BYTES]
            stderr = "Execution timed out."
            if isinstance(stdout, bytes):
                stdout = stdout.decode("utf-8", errors="replace")

    elapsed_ms = int((time.monotonic() - start) * 1000)
    return SandboxResult(
        stdout=stdout,
        stderr=stderr,
        timed_out=timed_out,
        time_taken_ms=elapsed_ms,
    )
