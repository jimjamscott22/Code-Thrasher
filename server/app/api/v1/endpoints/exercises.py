from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.database import get_db
from app.models.models import DifficultyLevel, Exercise
from app.schemas.schemas import ExerciseCreate, ExerciseDetail, ExerciseListItem

router = APIRouter(prefix="/exercises", tags=["exercises"])


@router.get("/", response_model=list[ExerciseListItem])
async def list_exercises(
    difficulty: DifficultyLevel | None = Query(None),
    category_id: int | None = Query(None),
    db: AsyncSession = Depends(get_db),
) -> list[Exercise]:
    stmt = select(Exercise).options(selectinload(Exercise.category))
    if difficulty:
        stmt = stmt.where(Exercise.difficulty_level == difficulty)
    if category_id:
        stmt = stmt.where(Exercise.category_id == category_id)
    result = await db.execute(stmt)
    return list(result.scalars().all())


@router.get("/{exercise_id}", response_model=ExerciseDetail)
async def get_exercise(exercise_id: int, db: AsyncSession = Depends(get_db)) -> Exercise:
    result = await db.execute(
        select(Exercise)
        .where(Exercise.id == exercise_id)
        .options(
            selectinload(Exercise.category),
            selectinload(Exercise.test_cases),
        )
    )
    exercise = result.scalar_one_or_none()
    if not exercise:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found")
    return exercise


@router.post("/", response_model=ExerciseDetail, status_code=status.HTTP_201_CREATED)
async def create_exercise(
    payload: ExerciseCreate,
    db: AsyncSession = Depends(get_db),
) -> Exercise:
    exercise = Exercise(**payload.model_dump())
    db.add(exercise)
    await db.commit()
    await db.refresh(exercise)
    # reload with relationships
    result = await db.execute(
        select(Exercise)
        .where(Exercise.id == exercise.id)
        .options(selectinload(Exercise.category), selectinload(Exercise.test_cases))
    )
    return result.scalar_one()
