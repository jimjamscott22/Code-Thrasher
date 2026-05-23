import pytest
from httpx import AsyncClient


@pytest.fixture
async def exercise_id(client: AsyncClient):
    r = await client.post(
        "/api/v1/exercises/",
        json={"title": "Test Ex", "description": "desc", "difficulty_level": "beginner"},
    )
    return r.json()["id"]


def _result(tc_id: int, passed: bool, weight: float = 1.0):
    return {
        "test_case_id": tc_id,
        "passed": passed,
        "expected": "42",
        "actual": "42" if passed else "0",
        "score_weight": weight,
    }


async def test_submit_all_pass(client: AsyncClient, exercise_id: int):
    r = await client.post(
        "/api/v1/submit/",
        json={
            "exercise_id": exercise_id,
            "code": "print(42)",
            "test_results": [_result(1, True), _result(2, True)],
            "time_taken_ms": 30,
        },
    )
    assert r.status_code == 200
    data = r.json()
    assert data["score"] == 100.0
    assert data["status"] == "completed"
    assert data["time_taken_ms"] == 30
    assert len(data["test_results"]) == 2
    assert "submission_id" in data


async def test_submit_partial_pass(client: AsyncClient, exercise_id: int):
    r = await client.post(
        "/api/v1/submit/",
        json={
            "exercise_id": exercise_id,
            "code": "print(0)",
            "test_results": [_result(1, True), _result(2, False)],
        },
    )
    assert r.status_code == 200
    data = r.json()
    assert data["score"] == 50.0
    assert data["status"] == "failed"


async def test_submit_all_fail(client: AsyncClient, exercise_id: int):
    r = await client.post(
        "/api/v1/submit/",
        json={
            "exercise_id": exercise_id,
            "code": "print('wrong')",
            "test_results": [_result(1, False), _result(2, False)],
        },
    )
    assert r.status_code == 200
    data = r.json()
    assert data["score"] == 0.0
    assert data["status"] == "failed"


async def test_submit_weighted_scoring(client: AsyncClient, exercise_id: int):
    # Two tests: first has weight 1, second has weight 3. Only first passes.
    # Expected score: 1/4 * 100 = 25.0
    r = await client.post(
        "/api/v1/submit/",
        json={
            "exercise_id": exercise_id,
            "code": "...",
            "test_results": [
                _result(1, True, weight=1.0),
                _result(2, False, weight=3.0),
            ],
        },
    )
    assert r.status_code == 200
    assert r.json()["score"] == 25.0


async def test_submit_exercise_not_found(client: AsyncClient):
    r = await client.post(
        "/api/v1/submit/",
        json={
            "exercise_id": 999,
            "code": "print(1)",
            "test_results": [_result(1, True)],
        },
    )
    assert r.status_code == 404


async def test_submit_empty_code_rejected(client: AsyncClient, exercise_id: int):
    r = await client.post(
        "/api/v1/submit/",
        json={
            "exercise_id": exercise_id,
            "code": "   ",
            "test_results": [],
        },
    )
    assert r.status_code == 422
