from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.models.models import DifficultyLevel, SubmissionStatus


# ── Users/Auth ────────────────────────────────────────────────────────────────

class UserCreate(BaseModel):
    username: Annotated[str, Field(min_length=3, max_length=50)]
    email: EmailStr
    password: Annotated[str, Field(min_length=8, max_length=128)]

    @field_validator("username")
    @classmethod
    def username_not_blank(cls, v: str) -> str:
        username = v.strip()
        if not username:
            raise ValueError("username must not be empty")
        return username


class UserLogin(BaseModel):
    username_or_email: Annotated[str, Field(min_length=1, max_length=255)]
    password: Annotated[str, Field(min_length=1, max_length=128)]

    @field_validator("username_or_email")
    @classmethod
    def identifier_not_blank(cls, v: str) -> str:
        identifier = v.strip()
        if not identifier:
            raise ValueError("username or email must not be empty")
        return identifier


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    total_score: int
    streak: int
    created_at: datetime

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


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
    is_hidden: bool

    model_config = {"from_attributes": True}


class TestCasePublicOut(BaseModel):
    id: int
    input_data: str
    expected_output: str | None = None
    score_weight: float
    is_hidden: bool


class ExerciseListItem(BaseModel):
    id: int
    title: str
    difficulty_level: DifficultyLevel
    category: CategoryOut | None

    model_config = {"from_attributes": True}


class ExerciseGuideBlock(BaseModel):
    kind: str
    title: str
    body: str
    code: str | None = None


class ExerciseDetail(BaseModel):
    id: int
    title: str
    description: str
    hint: str | None
    guide: list[ExerciseGuideBlock] = Field(default_factory=list)
    has_solution: bool = False
    difficulty_level: DifficultyLevel
    starter_code: str
    category: CategoryOut | None
    test_cases: list[TestCasePublicOut]


class ExerciseSolution(BaseModel):
    exercise_id: int
    code: str
    explanation: str | None = None


class ExerciseCreate(BaseModel):
    title: Annotated[str, Field(min_length=1, max_length=200)]
    description: str
    hint: str | None = None
    guide: list[ExerciseGuideBlock] = Field(default_factory=list)
    difficulty_level: DifficultyLevel = DifficultyLevel.beginner
    category_id: int | None = None
    starter_code: str = ""
    solution_code: str | None = None
    solution_explanation: str | None = None


# ── Submissions ───────────────────────────────────────────────────────────────

class TestCaseResult(BaseModel):
    test_case_id: int
    passed: bool
    expected: str
    actual: str
    score_weight: float


class SubmitRequest(BaseModel):
    exercise_id: int
    code: Annotated[str, Field(max_length=50_000)]
    time_taken_ms: Annotated[int, Field(ge=0, le=3_600_000)] = 0

    @field_validator("code")
    @classmethod
    def code_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("code must not be empty")
        return v


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


# ── Resources ─────────────────────────────────────────────────────────────────

class ResourceSection(BaseModel):
    heading: str
    body: str
    code: str | None = None
    output: str | None = None


class ResourceListItem(BaseModel):
    id: int
    title: str
    slug: str
    topic_area: str
    difficulty_level: DifficultyLevel
    summary: str
    order: int

    model_config = {"from_attributes": True}


class ResourceDetail(BaseModel):
    id: int
    title: str
    slug: str
    topic_area: str
    difficulty_level: DifficultyLevel
    summary: str
    sections: list[ResourceSection]
    order: int

    model_config = {"from_attributes": True}


# ── Progress ──────────────────────────────────────────────────────────────────

class ExerciseProgress(BaseModel):
    best_score: float
    attempts: int
    solved: bool


class ProgressResponse(BaseModel):
    total_exercises: int
    completed_count: int
    exercises: dict[int, ExerciseProgress]
