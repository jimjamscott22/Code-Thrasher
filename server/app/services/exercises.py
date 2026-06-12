"""Exercise queries, creation, and public response shaping."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.models import DifficultyLevel, Exercise, SolutionReveal, User
from app.schemas.schemas import (
    ExerciseCreate,
    ExerciseDetail,
    ExerciseGuideBlock,
    ExerciseListItem,
    ExerciseSolution,
    TestCasePublicOut,
)


def to_public_test_case(test_case) -> TestCasePublicOut:
    return TestCasePublicOut(
        id=test_case.id,
        input_data=test_case.input_data,
        expected_output=None if test_case.is_hidden else test_case.expected_output,
        score_weight=test_case.score_weight,
        is_hidden=test_case.is_hidden,
    )


def to_exercise_detail(exercise: Exercise) -> ExerciseDetail:
    guide = [ExerciseGuideBlock.model_validate(block) for block in (exercise.guide or [])]
    return ExerciseDetail(
        id=exercise.id,
        title=exercise.title,
        description=exercise.description,
        hint=exercise.hint,
        guide=guide,
        has_solution=exercise.has_solution,
        difficulty_level=exercise.difficulty_level,
        starter_code=exercise.starter_code,
        category=exercise.category,
        test_cases=[to_public_test_case(tc) for tc in exercise.test_cases],
    )


async def list_exercises(
    db: AsyncSession,
    *,
    difficulty: DifficultyLevel | None = None,
    category_id: int | None = None,
) -> list[Exercise]:
    stmt = select(Exercise).options(selectinload(Exercise.category))
    if difficulty:
        stmt = stmt.where(Exercise.difficulty_level == difficulty)
    if category_id:
        stmt = stmt.where(Exercise.category_id == category_id)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_exercise_by_id(db: AsyncSession, exercise_id: int) -> Exercise | None:
    result = await db.execute(
        select(Exercise)
        .where(Exercise.id == exercise_id)
        .options(
            selectinload(Exercise.category),
            selectinload(Exercise.test_cases),
        )
    )
    return result.scalar_one_or_none()


async def create_exercise(db: AsyncSession, payload: ExerciseCreate) -> Exercise:
    exercise = Exercise(**payload.model_dump())
    db.add(exercise)
    await db.commit()
    await db.refresh(exercise)
    result = await db.execute(
        select(Exercise)
        .where(Exercise.id == exercise.id)
        .options(selectinload(Exercise.category), selectinload(Exercise.test_cases))
    )
    return result.scalar_one()


async def get_exercise_solution(
    db: AsyncSession,
    exercise_id: int,
    user: User,
) -> ExerciseSolution:
    result = await db.execute(select(Exercise).where(Exercise.id == exercise_id))
    exercise = result.scalar_one_or_none()
    if exercise is None:
        raise LookupError("Exercise not found")
    if not exercise.solution_code or not exercise.solution_code.strip():
        raise LookupError("Solution not available")

    existing = await db.execute(
        select(SolutionReveal).where(
            SolutionReveal.user_id == user.id,
            SolutionReveal.exercise_id == exercise_id,
        )
    )
    if existing.scalar_one_or_none() is None:
        db.add(SolutionReveal(user_id=user.id, exercise_id=exercise_id))
        await db.commit()

    return ExerciseSolution(
        exercise_id=exercise.id,
        code=exercise.solution_code,
        explanation=exercise.solution_explanation,
    )
