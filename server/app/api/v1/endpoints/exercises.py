from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_admin_user, get_current_user
from app.core.rate_limit import get_user_or_remote_address, limiter
from app.db.database import get_db
from app.models.models import DifficultyLevel, Exercise, User
from app.schemas.schemas import (
    ExerciseCreate,
    ExerciseDetail,
    ExerciseListItem,
    ExerciseSolution,
)
from app.services import exercises as exercise_service

router = APIRouter(prefix="/exercises", tags=["exercises"])


@router.get("/", response_model=list[ExerciseListItem])
async def list_exercises(
    difficulty: DifficultyLevel | None = Query(None),
    category_id: int | None = Query(None),
    db: AsyncSession = Depends(get_db),
) -> list[Exercise]:
    return await exercise_service.list_exercises(
        db,
        difficulty=difficulty,
        category_id=category_id,
    )


@router.get("/{exercise_id}", response_model=ExerciseDetail)
async def get_exercise(
    exercise_id: int,
    db: AsyncSession = Depends(get_db),
) -> ExerciseDetail:
    exercise = await exercise_service.get_exercise_by_id(db, exercise_id)
    if not exercise:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found")
    return exercise_service.to_exercise_detail(exercise)


@router.get("/{exercise_id}/solution", response_model=ExerciseSolution)
@limiter.limit("10/minute", key_func=get_user_or_remote_address)
async def get_exercise_solution(
    request: Request,
    exercise_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db),
) -> ExerciseSolution:
    try:
        return await exercise_service.get_exercise_solution(db, exercise_id, current_user)
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.post("/", response_model=ExerciseDetail, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
async def create_exercise(
    request: Request,
    payload: ExerciseCreate,
    _admin: Annotated[User, Depends(get_current_admin_user)],
    db: AsyncSession = Depends(get_db),
) -> ExerciseDetail:
    exercise = await exercise_service.create_exercise(db, payload)
    return exercise_service.to_exercise_detail(exercise)
