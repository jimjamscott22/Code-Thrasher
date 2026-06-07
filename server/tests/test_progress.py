from httpx import AsyncClient


async def _register_headers(
    client: AsyncClient,
    username: str,
    email: str,
) -> dict[str, str]:
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "username": username,
            "email": email,
            "password": "password123",
        },
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


async def test_progress_empty(client: AsyncClient, auth_headers: dict[str, str]):
    r = await client.get("/api/v1/progress/", headers=auth_headers)
    assert r.status_code == 200
    data = r.json()
    assert data["total_exercises"] == 0
    assert data["completed_count"] == 0
    assert data["exercises"] == {}


async def test_progress_after_solved_submission(
    client: AsyncClient,
    auth_headers: dict[str, str],
):
    ex = (
        await client.post(
            "/api/v1/exercises/",
            json={"title": "Ex", "description": "d", "difficulty_level": "beginner"},
        )
    ).json()
    ex_id = ex["id"]

    await client.post(
        "/api/v1/submit/",
        headers=auth_headers,
        json={
            "exercise_id": ex_id,
            "code": "print(1)",
            "test_results": [
                {"test_case_id": 1, "passed": True, "expected": "1", "actual": "1", "score_weight": 1.0}
            ],
        },
    )

    r = await client.get("/api/v1/progress/", headers=auth_headers)
    data = r.json()
    assert data["total_exercises"] == 1
    assert data["completed_count"] == 1
    ex_progress = data["exercises"][str(ex_id)]
    assert ex_progress["solved"] is True
    assert ex_progress["best_score"] == 100.0
    assert ex_progress["attempts"] == 1


async def test_progress_tracks_best_score(
    client: AsyncClient,
    auth_headers: dict[str, str],
):
    ex_id = (
        await client.post(
            "/api/v1/exercises/",
            json={"title": "Ex", "description": "d", "difficulty_level": "beginner"},
        )
    ).json()["id"]

    # First attempt: 50%
    await client.post(
        "/api/v1/submit/",
        headers=auth_headers,
        json={
            "exercise_id": ex_id,
            "code": "print(0)",
            "test_results": [
                {"test_case_id": 1, "passed": False, "expected": "1", "actual": "0", "score_weight": 1.0},
                {"test_case_id": 2, "passed": True, "expected": "2", "actual": "2", "score_weight": 1.0},
            ],
        },
    )

    # Second attempt: also 50% (different test passing)
    await client.post(
        "/api/v1/submit/",
        headers=auth_headers,
        json={
            "exercise_id": ex_id,
            "code": "print(1)",
            "test_results": [
                {"test_case_id": 1, "passed": True, "expected": "1", "actual": "1", "score_weight": 1.0},
                {"test_case_id": 2, "passed": False, "expected": "2", "actual": "0", "score_weight": 1.0},
            ],
        },
    )

    r = await client.get("/api/v1/progress/", headers=auth_headers)
    data = r.json()
    ex_progress = data["exercises"][str(ex_id)]
    assert ex_progress["solved"] is False
    assert ex_progress["best_score"] == 50.0
    assert ex_progress["attempts"] == 2


async def test_progress_unsolved_does_not_count(
    client: AsyncClient,
    auth_headers: dict[str, str],
):
    ex_id = (
        await client.post(
            "/api/v1/exercises/",
            json={"title": "Ex", "description": "d", "difficulty_level": "beginner"},
        )
    ).json()["id"]

    await client.post(
        "/api/v1/submit/",
        headers=auth_headers,
        json={
            "exercise_id": ex_id,
            "code": "...",
            "test_results": [
                {"test_case_id": 1, "passed": False, "expected": "x", "actual": "y", "score_weight": 1.0}
            ],
        },
    )

    r = await client.get("/api/v1/progress/", headers=auth_headers)
    data = r.json()
    assert data["completed_count"] == 0
    assert data["exercises"][str(ex_id)]["solved"] is False


async def test_progress_total_exercises_count(
    client: AsyncClient,
    auth_headers: dict[str, str],
):
    for i in range(3):
        await client.post(
            "/api/v1/exercises/",
            json={"title": f"Ex {i}", "description": "d", "difficulty_level": "beginner"},
        )

    r = await client.get("/api/v1/progress/", headers=auth_headers)
    assert r.json()["total_exercises"] == 3


async def test_progress_is_scoped_to_current_user(client: AsyncClient):
    first_user = await _register_headers(client, "ada", "ada@example.com")
    second_user = await _register_headers(client, "grace", "grace@example.com")
    ex_id = (
        await client.post(
            "/api/v1/exercises/",
            json={"title": "Ex", "description": "d", "difficulty_level": "beginner"},
        )
    ).json()["id"]

    await client.post(
        "/api/v1/submit/",
        headers=first_user,
        json={
            "exercise_id": ex_id,
            "code": "print(1)",
            "test_results": [
                {"test_case_id": 1, "passed": True, "expected": "1", "actual": "1", "score_weight": 1.0}
            ],
        },
    )

    first_progress = await client.get("/api/v1/progress/", headers=first_user)
    second_progress = await client.get("/api/v1/progress/", headers=second_user)

    assert first_progress.json()["completed_count"] == 1
    assert second_progress.json()["completed_count"] == 0
    assert second_progress.json()["exercises"] == {}


async def test_progress_requires_auth(client: AsyncClient):
    r = await client.get("/api/v1/progress/")

    assert r.status_code == 401
