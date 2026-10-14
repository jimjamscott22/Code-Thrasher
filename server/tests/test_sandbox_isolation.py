"""Security-oriented sandbox isolation tests."""

import os

import pytest

from app.services.sandbox import run_python
from app.services.sandbox_isolation import isolation_available

requires_isolation = pytest.mark.skipif(
    not isolation_available(),
    reason=(
        "bubblewrap + codethrasher-sandbox user unavailable (install bubblewrap, "
        "create the sandbox user, and ensure user namespaces work — e.g. in Docker "
        "with kernel.unprivileged_userns_clone=1)"
    ),
)


@requires_isolation
@pytest.mark.asyncio
async def test_submission_cannot_read_api_environment(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql://leak:leak@db:5432/secret")
    monkeypatch.setenv("SECRET_KEY", "super-secret-key")

    code = """
import os
print(os.environ.get("DATABASE_URL", ""))
print(os.environ.get("SECRET_KEY", ""))
"""
    result = await run_python(code)
    assert "leak" not in result.stdout
    assert "super-secret" not in result.stdout


@requires_isolation
@pytest.mark.asyncio
async def test_submission_has_no_outbound_network():
    code = """
import socket
s = socket.socket()
s.settimeout(2)
try:
    s.connect(("1.1.1.1", 80))
    print("connected")
except OSError:
    print("blocked")
finally:
    s.close()
"""
    result = await run_python(code)
    assert "blocked" in result.stdout
    assert "connected" not in result.stdout


@requires_isolation
@pytest.mark.asyncio
async def test_submission_cannot_reach_database_host():
    code = """
import socket
s = socket.socket()
s.settimeout(2)
try:
    s.connect(("db", 5432))
    print("db")
except OSError:
    print("no-db")
finally:
    s.close()
"""
    result = await run_python(code)
    assert "no-db" in result.stdout
    assert "db" not in result.stdout.split()


@requires_isolation
@pytest.mark.asyncio
async def test_fork_bomb_is_contained():
    code = """
import os
count = 0
for _ in range(500):
    try:
        pid = os.fork()
    except OSError:
        print("stopped", count)
        break
    if pid == 0:
        os._exit(0)
    count += 1
else:
    print("stopped", count)
"""
    result = await run_python(code, timeout_seconds=5)
    assert not result.timed_out
    assert "stopped" in result.stdout
    stopped_line = next(line for line in result.stdout.splitlines() if line.startswith("stopped"))
    fork_count = int(stopped_line.split()[1])
    assert fork_count < 200


def test_isolation_module_documents_skip_reason():
    """When isolation is off, tests above skip instead of falsely passing."""
    if isolation_available():
        return
    # Ensure the skip message is informative for CI logs.
    assert "bubblewrap" in requires_isolation.kwargs.get("reason", "")
