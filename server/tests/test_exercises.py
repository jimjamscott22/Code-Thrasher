import pytest
from httpx import AsyncClient


@pytest.fixture
def new_exercise():
    return {
        "title": "Hello World",
        "description": "Print hello",
        "difficulty_level": "beginner",
        "starter_code": "# start here\n",
    }


async def test_list_exercises_empty(client: AsyncClient):
    r = await client.get("/api/v1/exercises/")
    assert r.status_code == 200
    assert r.json() == []


async def test_create_exercise(client: AsyncClient, new_exercise):
    r = await client.post("/api/v1/exercises/", json=new_exercise)
    assert r.status_code == 201
    data = r.json()
    assert data["title"] == new_exercise["title"]
    assert data["difficulty_level"] == "beginner"
    assert data["guide"] == []
    assert data["has_solution"] is False
    assert data["test_cases"] == []
    assert "id" in data


async def test_list_exercises_after_create(client: AsyncClient, new_exercise):
    await client.post("/api/v1/exercises/", json=new_exercise)
    await client.post("/api/v1/exercises/", json={**new_exercise, "title": "Second"})

    r = await client.get("/api/v1/exercises/")
    assert r.status_code == 200
    assert len(r.json()) == 2


async def test_get_exercise_by_id(client: AsyncClient, new_exercise):
    created = (await client.post("/api/v1/exercises/", json=new_exercise)).json()
    ex_id = created["id"]

    r = await client.get(f"/api/v1/exercises/{ex_id}")
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == ex_id
    assert data["title"] == new_exercise["title"]
    assert data["starter_code"] == new_exercise["starter_code"]
    assert "solution_code" not in data
    assert "solution_explanation" not in data
    assert isinstance(data["test_cases"], list)


async def test_get_exercise_solution_requires_reveal(client: AsyncClient, new_exercise):
    guide = [
        {
            "kind": "nudge",
            "title": "Try print",
            "body": "Use stdout for this challenge.",
        }
    ]
    created = (
        await client.post(
            "/api/v1/exercises/",
            json={
                **new_exercise,
                "guide": guide,
                "solution_code": 'print("hello")',
                "solution_explanation": "Printing the string satisfies the expected output.",
            },
        )
    ).json()

    detail = await client.get(f"/api/v1/exercises/{created['id']}")
    assert detail.status_code == 200
    detail_data = detail.json()
    assert detail_data["guide"] == [{**guide[0], "code": None}]
    assert detail_data["has_solution"] is True
    assert "solution_code" not in detail_data

    solution = await client.get(f"/api/v1/exercises/{created['id']}/solution")
    assert solution.status_code == 200
    assert solution.json() == {
        "exercise_id": created["id"],
        "code": 'print("hello")',
        "explanation": "Printing the string satisfies the expected output.",
    }


async def test_get_exercise_solution_not_available(client: AsyncClient, new_exercise):
    created = (await client.post("/api/v1/exercises/", json=new_exercise)).json()

    r = await client.get(f"/api/v1/exercises/{created['id']}/solution")
    assert r.status_code == 404


async def test_get_exercise_not_found(client: AsyncClient):
    r = await client.get("/api/v1/exercises/999")
    assert r.status_code == 404


async def test_list_exercises_filter_by_difficulty(client: AsyncClient, new_exercise):
    await client.post("/api/v1/exercises/", json=new_exercise)
    await client.post(
        "/api/v1/exercises/",
        json={**new_exercise, "title": "Hard one", "difficulty_level": "advanced"},
    )

    r = await client.get("/api/v1/exercises/?difficulty=beginner")
    assert r.status_code == 200
    results = r.json()
    assert len(results) == 1
    assert results[0]["difficulty_level"] == "beginner"
