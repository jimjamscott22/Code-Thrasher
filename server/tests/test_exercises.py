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
    assert isinstance(data["test_cases"], list)


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
