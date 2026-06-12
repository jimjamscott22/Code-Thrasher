import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core.rate_limit import limiter
from app.db.database import Base, get_db
from app.main import app
from app.models.models import DifficultyLevel, Exercise, TestCase, User

TEST_DB_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSession = async_sessionmaker(engine, expire_on_commit=False)


async def override_get_db():
    async with TestingSession() as session:
        yield session


@pytest.fixture(autouse=True)
def disable_rate_limits():
    limiter.enabled = False
    yield
    limiter.enabled = True


@pytest_asyncio.fixture(autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def client():
    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def auth_headers(client: AsyncClient) -> dict[str, str]:
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
        },
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest_asyncio.fixture
async def admin_headers(client: AsyncClient) -> dict[str, str]:
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "username": "adminuser",
            "email": "admin@example.com",
            "password": "password123",
        },
    )
    token = response.json()["access_token"]
    user_id = response.json()["user"]["id"]

    async with TestingSession() as session:
        user = await session.get(User, user_id)
        assert user is not None
        user.is_admin = True
        await session.commit()

    return {"Authorization": f"Bearer {token}"}


@pytest_asyncio.fixture
async def exercise_with_tests() -> int:
    async with TestingSession() as session:
        exercise = Exercise(
            title="Graded Exercise",
            description="Print forty-two",
            difficulty_level=DifficultyLevel.beginner,
            starter_code="",
        )
        session.add(exercise)
        await session.flush()
        session.add_all(
            [
                TestCase(
                    exercise_id=exercise.id,
                    expected_output="42",
                    score_weight=1.0,
                    is_hidden=False,
                ),
                TestCase(
                    exercise_id=exercise.id,
                    expected_output="42",
                    score_weight=3.0,
                    is_hidden=True,
                ),
            ]
        )
        await session.commit()
        return exercise.id


@pytest_asyncio.fixture
async def dual_output_exercise() -> int:
    async with TestingSession() as session:
        exercise = Exercise(
            title="Dual Output Exercise",
            description="Print one or two",
            difficulty_level=DifficultyLevel.beginner,
            starter_code="",
        )
        session.add(exercise)
        await session.flush()
        session.add_all(
            [
                TestCase(
                    exercise_id=exercise.id,
                    expected_output="1",
                    score_weight=1.0,
                    is_hidden=False,
                ),
                TestCase(
                    exercise_id=exercise.id,
                    expected_output="2",
                    score_weight=1.0,
                    is_hidden=False,
                ),
            ]
        )
        await session.commit()
        return exercise.id


@pytest_asyncio.fixture
async def partial_exercise_with_tests() -> int:
    async with TestingSession() as session:
        exercise = Exercise(
            title="Partial Exercise",
            description="Mixed outputs",
            difficulty_level=DifficultyLevel.beginner,
            starter_code="",
        )
        session.add(exercise)
        await session.flush()
        session.add_all(
            [
                TestCase(
                    exercise_id=exercise.id,
                    expected_output="42",
                    score_weight=1.0,
                    is_hidden=False,
                ),
                TestCase(
                    exercise_id=exercise.id,
                    expected_output="99",
                    score_weight=3.0,
                    is_hidden=True,
                ),
            ]
        )
        await session.commit()
        return exercise.id
