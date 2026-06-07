from httpx import AsyncClient


def _user_payload(username: str = "ada", email: str = "ada@example.com"):
    return {
        "username": username,
        "email": email,
        "password": "password123",
    }


async def test_register_returns_token_and_user(client: AsyncClient):
    r = await client.post("/api/v1/auth/register", json=_user_payload())

    assert r.status_code == 201
    data = r.json()
    assert data["token_type"] == "bearer"
    assert data["access_token"]
    assert data["user"]["username"] == "ada"
    assert data["user"]["email"] == "ada@example.com"
    assert "password" not in data["user"]


async def test_register_rejects_duplicate_username(client: AsyncClient):
    await client.post("/api/v1/auth/register", json=_user_payload())

    r = await client.post(
        "/api/v1/auth/register",
        json=_user_payload(email="different@example.com"),
    )

    assert r.status_code == 400
    assert r.json()["detail"] == "Username is already registered"


async def test_register_rejects_duplicate_email(client: AsyncClient):
    await client.post("/api/v1/auth/register", json=_user_payload())

    r = await client.post(
        "/api/v1/auth/register",
        json=_user_payload(username="grace"),
    )

    assert r.status_code == 400
    assert r.json()["detail"] == "Email is already registered"


async def test_login_accepts_username_or_email(client: AsyncClient):
    await client.post("/api/v1/auth/register", json=_user_payload())

    by_username = await client.post(
        "/api/v1/auth/login",
        json={"username_or_email": "ada", "password": "password123"},
    )
    by_email = await client.post(
        "/api/v1/auth/login",
        json={"username_or_email": "ada@example.com", "password": "password123"},
    )

    assert by_username.status_code == 200
    assert by_email.status_code == 200
    assert by_username.json()["access_token"]
    assert by_email.json()["access_token"]


async def test_login_rejects_bad_credentials(client: AsyncClient):
    await client.post("/api/v1/auth/register", json=_user_payload())

    r = await client.post(
        "/api/v1/auth/login",
        json={"username_or_email": "ada", "password": "wrong-password"},
    )

    assert r.status_code == 401
    assert r.json()["detail"] == "Incorrect username or password"


async def test_me_returns_current_user(client: AsyncClient):
    registered = await client.post("/api/v1/auth/register", json=_user_payload())
    token = registered.json()["access_token"]

    r = await client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert r.status_code == 200
    assert r.json()["username"] == "ada"


async def test_me_rejects_missing_token(client: AsyncClient):
    r = await client.get("/api/v1/auth/me")

    assert r.status_code == 401
