from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field, field_validator

from app.models.models import DifficultyLevel, SubmissionStatus


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

class TestCaseResult(BaseModel):
    test_case_id: int
    passed: bool
    expected: str
    actual: str
    score_weight: float


class SubmitRequest(BaseModel):
    exercise_id: int
    code: Annotated[str, Field(max_length=50_000)]
    test_results: list[TestCaseResult]
    time_taken_ms: int = 0

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


# ── Progress ──────────────────────────────────────────────────────────────────

class ExerciseProgress(BaseModel):
    best_score: float
    attempts: int
    solved: bool


class ProgressResponse(BaseModel):
    total_exercises: int
    completed_count: int
    exercises: dict[int, ExerciseProgress]
