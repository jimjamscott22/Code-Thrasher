import pytest
from httpx import AsyncClient

from app.models.models import DifficultyLevel, Exercise, TestCase
from app.services.sandbox import node_available, rust_available
from tests.conftest import TestingSession


async def test_submit_all_pass(
    client: AsyncClient,
    exercise_with_tests: int,
    auth_headers: dict[str, str],
):
    r = await client.post(
        "/api/v1/submit/",
        headers=auth_headers,
        json={
            "exercise_id": exercise_with_tests,
            "code": "print(42)",
            "time_taken_ms": 30,
        },
    )
    assert r.status_code == 200
    data = r.json()
    assert data["score"] == 100.0
    assert data["status"] == "completed"
    assert data["time_taken_ms"] == 30
    assert len(data["test_results"]) == 2
    assert all(result["passed"] for result in data["test_results"])
    assert data["test_results"][1]["expected"] == ""
    assert "submission_id" in data


async def test_submit_partial_pass(
    client: AsyncClient,
    partial_exercise_with_tests: int,
    auth_headers: dict[str, str],
):
    r = await client.post(
        "/api/v1/submit/",
        headers=auth_headers,
        json={
            "exercise_id": partial_exercise_with_tests,
            "code": "print(42)",
        },
    )
    assert r.status_code == 200
    data = r.json()
    assert data["score"] == 25.0
    assert data["status"] == "failed"


async def test_submit_all_fail(
    client: AsyncClient,
    exercise_with_tests: int,
    auth_headers: dict[str, str],
):
    r = await client.post(
        "/api/v1/submit/",
        headers=auth_headers,
        json={
            "exercise_id": exercise_with_tests,
            "code": "print('wrong')",
        },
    )
    assert r.status_code == 200
    data = r.json()
    assert data["score"] == 0.0
    assert data["status"] == "failed"


async def test_submit_exercise_not_found(
    client: AsyncClient,
    auth_headers: dict[str, str],
):
    r = await client.post(
        "/api/v1/submit/",
        headers=auth_headers,
        json={
            "exercise_id": 999,
            "code": "print(1)",
        },
    )
    assert r.status_code == 404


async def test_submit_empty_code_rejected(
    client: AsyncClient,
    exercise_with_tests: int,
    auth_headers: dict[str, str],
):
    r = await client.post(
        "/api/v1/submit/",
        headers=auth_headers,
        json={
            "exercise_id": exercise_with_tests,
            "code": "   ",
        },
    )
    assert r.status_code == 422


async def test_submit_requires_auth(client: AsyncClient, exercise_with_tests: int):
    r = await client.post(
        "/api/v1/submit/",
        json={
            "exercise_id": exercise_with_tests,
            "code": "print(42)",
        },
    )

    assert r.status_code == 401


async def test_submit_updates_user_stats(
    client: AsyncClient,
    exercise_with_tests: int,
    auth_headers: dict[str, str],
):
    await client.post(
        "/api/v1/submit/",
        headers=auth_headers,
        json={
            "exercise_id": exercise_with_tests,
            "code": "print(42)",
        },
    )

    me = await client.get("/api/v1/auth/me", headers=auth_headers)
    assert me.status_code == 200
    data = me.json()
    assert data["total_score"] == 100
    assert data["streak"] >= 1


async def _rust_exercise(language: str = "rust") -> int:
    async with TestingSession() as session:
        exercise = Exercise(
            title="Rust Graded",
            description="Print forty-two",
            language=language,
            difficulty_level=DifficultyLevel.beginner,
            starter_code="",
        )
        session.add(exercise)
        await session.flush()
        session.add_all(
            TestCase(exercise_id=exercise.id, expected_output="42", is_hidden=hidden)
            for hidden in (False, True)
        )
        await session.commit()
        return exercise.id


@pytest.mark.skipif(not rust_available(), reason="rustc not installed")
async def test_submit_rust_pass_and_compile_error(
    client: AsyncClient, auth_headers: dict[str, str]
):
    exercise_id = await _rust_exercise()

    ok = await client.post(
        "/api/v1/submit/",
        headers=auth_headers,
        json={
            "exercise_id": exercise_id,
            "code": 'fn main() { println!("{}", 6 * 7); }',
        },
    )
    assert ok.status_code == 200
    assert ok.json()["status"] == "completed"
    assert ok.json()["score"] == 100.0

    bad = await client.post(
        "/api/v1/submit/",
        headers=auth_headers,
        json={"exercise_id": exercise_id, "code": "fn main() { let x: i32 = \"a\"; }"},
    )
    assert bad.status_code == 200
    body = bad.json()
    assert body["score"] == 0.0
    assert body["status"] == "failed"
    assert "mismatched types" in body["stderr"]
    assert body["stderr"].count("mismatched types") == 1  # not repeated per test case


async def test_python_code_is_not_graded_as_rust(
    client: AsyncClient, auth_headers: dict[str, str]
):
    exercise_id = await _rust_exercise(language="python")
    r = await client.post(
        "/api/v1/submit/",
        headers=auth_headers,
        json={"exercise_id": exercise_id, "code": "print(42)"},
    )
    assert r.json()["status"] == "completed"


@pytest.mark.skipif(not node_available(), reason="node not installed")
async def test_submit_javascript_pass_and_runtime_error(
    client: AsyncClient, auth_headers: dict[str, str]
):
    exercise_id = await _rust_exercise(language="javascript")

    ok = await client.post(
        "/api/v1/submit/",
        headers=auth_headers,
        json={"exercise_id": exercise_id, "code": "console.log(6 * 7);"},
    )
    assert ok.status_code == 200
    assert ok.json()["status"] == "completed"
    assert ok.json()["score"] == 100.0

    bad = await client.post(
        "/api/v1/submit/",
        headers=auth_headers,
        json={"exercise_id": exercise_id, "code": "console.log(answer);"},
    )
    body = bad.json()
    assert body["status"] == "failed"
    assert "ReferenceError: answer is not defined" in body["stderr"]
