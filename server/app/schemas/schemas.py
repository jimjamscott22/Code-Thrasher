from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.models.models import DifficultyLevel, SubmissionStatus


# ── Auth ──────────────────────────────────────────────────────────────────────

class UserRegister(BaseModel):
    username: Annotated[str, Field(min_length=3, max_length=50)]
    email: EmailStr
    password: Annotated[str, Field(min_length=8, max_length=128)]


class UserLogin(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserPublic(BaseModel):
    id: int
    username: str
    email: str
    total_score: int
    streak: int
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Categories ────────────────────────────────────────────────────────────────

class CategoryOut(BaseModel):
    id: int
    name: str
    slug: str

    model_config = {"from_attributes": True}


# ── Exercises ─────────────────────────────────────────────────────────────────

class TestCaseOut(BaseModel):
    id: int
    input_data: str
    expected_output: str
    score_weight: float

    model_config = {"from_attributes": True}


class ExerciseListItem(BaseModel):
    id: int
    title: str
    difficulty_level: DifficultyLevel
    category: CategoryOut | None

    model_config = {"from_attributes": True}


class ExerciseDetail(BaseModel):
    id: int
    title: str
    description: str
    hint: str | None
    difficulty_level: DifficultyLevel
    starter_code: str
    category: CategoryOut | None
    test_cases: list[TestCaseOut]

    model_config = {"from_attributes": True}


class ExerciseCreate(BaseModel):
    title: Annotated[str, Field(min_length=1, max_length=200)]
    description: str
    hint: str | None = None
    difficulty_level: DifficultyLevel = DifficultyLevel.beginner
    category_id: int | None = None
    starter_code: str = ""


# ── Submissions ───────────────────────────────────────────────────────────────

class SubmitRequest(BaseModel):
    exercise_id: int
    code: Annotated[str, Field(max_length=50_000)]

    @field_validator("code")
    @classmethod
    def code_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("code must not be empty")
        return v


class TestCaseResult(BaseModel):
    test_case_id: int
    passed: bool
    expected: str
    actual: str
    score_weight: float


class SubmitResponse(BaseModel):
    submission_id: int
    status: SubmissionStatus
    score: float
    stdout: str
    stderr: str
    time_taken_ms: int
    test_results: list[TestCaseResult]


class SubmissionHistory(BaseModel):
    id: int
    exercise_id: int
    status: SubmissionStatus
    score: float
    time_taken_ms: int
    created_at: datetime

    model_config = {"from_attributes": True}
