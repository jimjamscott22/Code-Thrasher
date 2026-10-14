"""Bubblewrap-based isolation for untrusted code execution."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path

from app.core.config import settings

_BWRAP_PROBE: bool | None = None


def sandbox_user_ids() -> tuple[int, int] | None:
    """Return (uid, gid) for the dedicated sandbox account, or None if missing."""
    import pwd

    try:
        entry = pwd.getpwnam(settings.SANDBOX_USER)
    except KeyError:
        return None
    return entry.pw_uid, entry.pw_gid


def bubblewrap_path() -> str | None:
    path = settings.SANDBOX_BUBBLEWRAP_PATH
    resolved = shutil.which(path)
    return resolved


def isolation_available() -> bool:
    """True when bubblewrap + sandbox user work on this host."""
    global _BWRAP_PROBE
    if not settings.SANDBOX_ENABLE_ISOLATION:
        return False
    if sandbox_user_ids() is None:
        return False
    bwrap = bubblewrap_path()
    if bwrap is None:
        return False
    if _BWRAP_PROBE is not None:
        return _BWRAP_PROBE

    uid, gid = sandbox_user_ids()
    assert uid is not None and gid is not None
    try:
        probe = subprocess.run(
            [
                bwrap,
                "--unshare-net",
                "--die-with-parent",
                "--new-session",
                "--uid",
                str(uid),
                "--gid",
                str(gid),
                "--clearenv",
                "--setenv",
                "PATH",
                "/usr/bin:/bin",
                "--ro-bind",
                "/",
                "/",
                "--dev-bind",
                "/dev",
                "/dev",
                "--proc",
                "/proc",
                "--",
                "true",
            ],
            capture_output=True,
            timeout=5,
            check=False,
        )
        _BWRAP_PROBE = probe.returncode == 0
    except (OSError, subprocess.TimeoutExpired):
        _BWRAP_PROBE = False
    return _BWRAP_PROBE


def minimal_runtime_env() -> dict[str, str]:
    """Environment for subprocess fallback when bubblewrap is unavailable."""
    path = os.environ.get("PATH", "/usr/local/bin:/usr/bin:/bin")
    return {
        "PATH": path,
        "LANG": "C.UTF-8",
        "HOME": "/tmp",
        "PYTHONNOUSERSITE": "1",
        "NODE_OPTIONS": "",
    }


def _host_rust_toolchain_dirs() -> tuple[str | None, str | None]:
    rustup = os.environ.get("RUSTUP_HOME")
    cargo = os.environ.get("CARGO_HOME")
    if not rustup:
        candidate = Path.home() / ".rustup"
        if candidate.is_dir():
            rustup = str(candidate)
    if not cargo:
        candidate = Path.home() / ".cargo"
        if candidate.is_dir():
            cargo = str(candidate)
    return rustup, cargo


def wrap_with_bubblewrap(
    argv: list[str],
    *,
    workdir: Path | None = None,
    writable_tmp: bool = True,
    include_rust_toolchain: bool = False,
) -> list[str]:
    """Prefix ``argv`` with bubblewrap flags (network off, clearenv, sandbox user)."""
    bwrap = bubblewrap_path()
    if bwrap is None:
        raise RuntimeError("bubblewrap not available")
    uid, gid = sandbox_user_ids()
    if uid is None or gid is None:
        raise RuntimeError(f"sandbox user {settings.SANDBOX_USER!r} not found")

    path = os.environ.get("PATH", "/usr/local/bin:/usr/bin:/bin")
    home = "/tmp"
    extra_env: list[str] = []
    toolchain_binds: list[str] = []
    if include_rust_toolchain:
        rustup_home, cargo_home = _host_rust_toolchain_dirs()
        if rustup_home:
            toolchain_binds.extend(["--ro-bind", rustup_home, rustup_home])
            extra_env.extend(["--setenv", "RUSTUP_HOME", rustup_home])
        if cargo_home:
            toolchain_binds.extend(["--ro-bind", cargo_home, cargo_home])
            extra_env.extend(["--setenv", "CARGO_HOME", cargo_home])

    prefix: list[str] = [
        bwrap,
        "--unshare-net",
        "--die-with-parent",
        "--new-session",
        "--uid",
        str(uid),
        "--gid",
        str(gid),
        "--clearenv",
        "--setenv",
        "PATH",
        path,
        "--setenv",
        "LANG",
        "C.UTF-8",
        "--setenv",
        "HOME",
        home,
        "--setenv",
        "PYTHONNOUSERSITE",
        "1",
        *extra_env,
        "--ro-bind",
        "/",
        "/",
        "--dev-bind",
        "/dev",
        "/dev",
        "--proc",
        "/proc",
        *toolchain_binds,
    ]
    if writable_tmp:
        prefix.extend(["--tmpfs", "/tmp"])
    if workdir is not None:
        resolved = workdir.resolve()
        prefix.extend(["--bind", str(resolved), str(resolved)])
    prefix.append("--")
    return prefix + argv


def prlimit_argv(
    *,
    max_memory_mb: int | None = None,
    max_processes: int | None = None,
    max_file_size_bytes: int | None = None,
    max_open_files: int | None = None,
) -> list[str]:
    """Build a ``prlimit`` prefix; empty when ``prlimit`` is missing."""
    prlimit = shutil.which("prlimit")
    if prlimit is None:
        return []

    args = [prlimit]
    if max_memory_mb is not None:
        args.append(f"--as={max_memory_mb * 1024 * 1024}")
    if max_processes is not None:
        args.append(f"--nproc={max_processes}")
    if max_file_size_bytes is not None:
        args.append(f"--fsize={max_file_size_bytes}")
    if max_open_files is not None:
        args.append(f"--nofile={max_open_files}")
    if len(args) == 1:
        return []
    args.append("--")
    return args


def preexec_resource_limits(
    *,
    max_memory_mb: int | None = None,
    max_processes: int | None = None,
    max_file_size_bytes: int | None = None,
    max_open_files: int | None = None,
) -> Callable[[], None] | None:
    """``preexec_fn`` for non-bwrap fallback (never apply to the bwrap parent)."""
    if sys.platform == "win32":
        return None

    import resource

    def _apply() -> None:
        if max_memory_mb is not None:
            cap = max_memory_mb * 1024 * 1024
            resource.setrlimit(resource.RLIMIT_AS, (cap, cap))
        if max_processes is not None:
            resource.setrlimit(resource.RLIMIT_NPROC, (max_processes, max_processes))
        if max_file_size_bytes is not None:
            resource.setrlimit(
                resource.RLIMIT_FSIZE, (max_file_size_bytes, max_file_size_bytes)
            )
        if max_open_files is not None:
            resource.setrlimit(resource.RLIMIT_NOFILE, (max_open_files, max_open_files))

    return _apply


def sandbox_rustc_command(rustc_argv: list[str]) -> list[str]:
    """Return argv for ``rustc``, preferring the distro binary when configured."""
    if settings.SANDBOX_RUSTC_PATH:
        return [settings.SANDBOX_RUSTC_PATH, *rustc_argv[1:]]
    return rustc_argv


def build_sandbox_command(
    argv: list[str],
    *,
    workdir: Path | None = None,
    max_memory_mb: int | None = None,
    apply_memory_limit: bool = True,
    apply_resource_limits: bool = True,
    include_rust_toolchain: bool = False,
) -> tuple[list[str], dict[str, str] | None, Callable[[], None] | None]:
    """Return (cmd, env, preexec_fn) for ``subprocess.run``.

    When isolation is available, resource limits are applied inside the sandbox via
    ``prlimit`` so the bubblewrap parent is not starved of process slots.
    """
    if apply_resource_limits:
        limits = {
            "max_memory_mb": max_memory_mb if apply_memory_limit else None,
            "max_processes": settings.SANDBOX_MAX_PROCESSES,
            "max_file_size_bytes": settings.SANDBOX_MAX_FILE_SIZE_BYTES,
            "max_open_files": settings.SANDBOX_MAX_OPEN_FILES,
        }
    else:
        limits = {
            "max_memory_mb": None,
            "max_processes": None,
            "max_file_size_bytes": None,
            "max_open_files": None,
        }

    if isolation_available():
        inner = prlimit_argv(**limits) + argv
        cmd = wrap_with_bubblewrap(
            inner,
            workdir=workdir,
            include_rust_toolchain=include_rust_toolchain,
        )
        return cmd, None, None

    preexec = preexec_resource_limits(**limits) if apply_resource_limits else None
    return argv, minimal_runtime_env(), preexec
