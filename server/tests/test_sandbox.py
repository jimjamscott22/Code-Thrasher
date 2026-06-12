import pytest

from app.services.sandbox import run_python


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
