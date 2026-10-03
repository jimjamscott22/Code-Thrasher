import pytest
from httpx import AsyncClient
from sqlalchemy import func, select

from app.models.models import DifficultyLevel, Exercise, Submission
from app.services.sandbox import rust_available
from tests.conftest import TestingSession

requires_rust = pytest.mark.skipif(not rust_available(), reason="rustc not installed")


async def _exercise(language: str) -> int:
    async with TestingSession() as session:
        exercise = Exercise(
            title=f"Run {language}",
            description="Scratch",
            language=language,
            difficulty_level=DifficultyLevel.beginner,
            starter_code="",
        )
        session.add(exercise)
        await session.commit()
        return exercise.id


async def test_run_requires_auth(client: AsyncClient):
    r = await client.post("/api/v1/run/", json={"exercise_id": 1, "code": "print(1)"})
    assert r.status_code in (401, 403)


async def test_run_unknown_exercise(client: AsyncClient, auth_headers: dict[str, str]):
    r = await client.post(
        "/api/v1/run/", headers=auth_headers, json={"exercise_id": 999, "code": "print(1)"}
    )
    assert r.status_code == 404


async def test_run_rejects_empty_code(client: AsyncClient, auth_headers: dict[str, str]):
    exercise_id = await _exercise("python")
    r = await client.post(
        "/api/v1/run/", headers=auth_headers, json={"exercise_id": exercise_id, "code": "  "}
    )
    assert r.status_code == 422


async def test_run_python_uses_exercise_language_and_stdin(
    client: AsyncClient, auth_headers: dict[str, str]
):
    exercise_id = await _exercise("python")
    r = await client.post(
        "/api/v1/run/",
        headers=auth_headers,
        json={"exercise_id": exercise_id, "code": "print(input().upper())", "input_data": "ada"},
    )
    assert r.status_code == 200
    body = r.json()
    assert body["stdout"].strip() == "ADA"
    assert body["stderr"] == ""
    assert body["timed_out"] is False
    assert body["duration_ms"] >= 0


@requires_rust
async def test_run_rust_output_and_compile_error(
    client: AsyncClient, auth_headers: dict[str, str]
):
    exercise_id = await _exercise("rust")

    ok = await client.post(
        "/api/v1/run/",
        headers=auth_headers,
        json={"exercise_id": exercise_id, "code": 'fn main() { println!("hi"); }'},
    )
    assert ok.status_code == 200
    assert ok.json()["stdout"].strip() == "hi"
    assert ok.json()["stderr"] == ""

    bad = await client.post(
        "/api/v1/run/",
        headers=auth_headers,
        json={"exercise_id": exercise_id, "code": 'fn main() { let x: i32 = "a"; }'},
    )
    assert bad.status_code == 200
    assert "mismatched types" in bad.json()["stderr"]
    assert bad.json()["stdout"] == ""


async def test_run_is_not_persisted(client: AsyncClient, auth_headers: dict[str, str]):
    exercise_id = await _exercise("python")
    await client.post(
        "/api/v1/run/", headers=auth_headers, json={"exercise_id": exercise_id, "code": "print(1)"}
    )
    async with TestingSession() as session:
        count = await session.scalar(select(func.count()).select_from(Submission))
    assert count == 0
    me = (await client.get("/api/v1/auth/me", headers=auth_headers)).json()
    assert me["total_score"] == 0
