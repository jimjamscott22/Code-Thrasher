import pytest
from httpx import AsyncClient


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
