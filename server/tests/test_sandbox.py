import pytest

from app.services.sandbox import run_python, run_rust, rust_available, rust_runner


@pytest.mark.asyncio
async def test_run_python_success():
    result = await run_python('print("hello")')
    assert result.stdout.strip() == "hello"
    assert result.stderr == ""
    assert not result.timed_out


@pytest.mark.asyncio
async def test_run_python_with_input():
    result = await run_python("name = input()\nprint(name)", input_data="Ada")
    assert result.stdout.strip() == "Ada"
    assert not result.timed_out


@pytest.mark.asyncio
async def test_run_python_syntax_error():
    result = await run_python("print(")
    assert result.stderr
    assert not result.timed_out


@pytest.mark.asyncio
async def test_run_python_timeout():
    result = await run_python("import time\ntime.sleep(30)", timeout_seconds=1)
    assert result.timed_out
    assert "timed out" in result.stderr.lower()


requires_rust = pytest.mark.skipif(not rust_available(), reason="rustc not installed")


@requires_rust
@pytest.mark.asyncio
async def test_run_rust_success():
    result = await run_rust('fn main() { println!("hello"); }')
    assert result.stdout.strip() == "hello"
    assert result.stderr == ""
    assert not result.timed_out


@requires_rust
@pytest.mark.asyncio
async def test_run_rust_reads_stdin():
    code = """
    use std::io::read_to_string;
    fn main() {
        let name = read_to_string(std::io::stdin()).unwrap();
        println!("hi {}", name.trim());
    }
    """
    result = await run_rust(code, input_data="Ada")
    assert result.stdout.strip() == "hi Ada"
    assert result.stderr == ""


@requires_rust
@pytest.mark.asyncio
async def test_run_rust_warnings_are_not_errors():
    result = await run_rust('fn main() { let unused = 1; println!("ok"); }')
    assert result.stdout.strip() == "ok"
    assert result.stderr == ""


@requires_rust
@pytest.mark.asyncio
async def test_run_rust_compile_error_reports_main_rs():
    result = await run_rust("fn main() { let x: i32 = \"nope\"; }")
    assert "mismatched types" in result.stderr
    assert "main.rs" in result.stderr
    assert result.stdout == ""
    assert not result.timed_out


@requires_rust
@pytest.mark.asyncio
async def test_run_rust_panic_is_an_error():
    result = await run_rust('fn main() { panic!("boom"); }')
    assert "boom" in result.stderr


@requires_rust
@pytest.mark.asyncio
async def test_run_rust_timeout():
    result = await run_rust("fn main() { loop {} }", timeout_seconds=1)
    assert result.timed_out


@requires_rust
@pytest.mark.asyncio
async def test_rust_runner_compiles_once_for_many_inputs():
    code = """
    use std::io::read_to_string;
    fn main() { print!("{}", read_to_string(std::io::stdin()).unwrap()); }
    """
    async with rust_runner(code) as run:
        assert (await run("a")).stdout == "a"
        assert (await run("b")).stdout == "b"


@pytest.mark.asyncio
async def test_run_rust_without_toolchain(monkeypatch):
    monkeypatch.setenv("PATH", "")
    result = await run_rust("fn main() {}")
    assert "not installed" in result.stderr


@pytest.mark.parametrize("limit", [1, 2])
@pytest.mark.asyncio
async def test_rust_compiles_are_capped(monkeypatch, limit):
    import asyncio
    import threading
    import time

    from app.core.config import settings
    from app.services import sandbox

    monkeypatch.setattr(settings, "SANDBOX_RUST_MAX_CONCURRENT_COMPILES", limit)

    lock = threading.Lock()
    active = peak = 0

    def fake_compile(code, workdir, timeout_seconds, max_output_bytes):
        nonlocal active, peak
        with lock:
            active += 1
            peak = max(peak, active)
        time.sleep(0.05)
        with lock:
            active -= 1
        # Report a failure so no binary is needed for the run step.
        return sandbox.SandboxRunResult("", "stub", False, False)

    monkeypatch.setattr(sandbox, "_compile_rust_sync", fake_compile)

    results = await asyncio.gather(*(run_rust("fn main() {}") for _ in range(8)))

    assert all(r.stderr == "stub" for r in results)
    assert peak == limit


@pytest.mark.asyncio
async def test_failed_compile_releases_its_slot(monkeypatch):
    from app.core.config import settings
    from app.services import sandbox

    monkeypatch.setattr(settings, "SANDBOX_RUST_MAX_CONCURRENT_COMPILES", 1)

    def boom(*args, **kwargs):
        raise RuntimeError("compiler exploded")

    monkeypatch.setattr(sandbox, "_compile_rust_sync", boom)

    for _ in range(2):  # the second call would hang if the slot leaked
        with pytest.raises(RuntimeError):
            await run_rust("fn main() {}")
