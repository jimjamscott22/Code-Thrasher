from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.models.models import Exercise, Submission
from app.schemas.schemas import ExerciseProgress, ProgressResponse

router = APIRouter(prefix="/progress", tags=["progress"])


@router.get("/", response_model=ProgressResponse)
async def get_progress(db: AsyncSession = Depends(get_db)) -> ProgressResponse:
    total: int = (
        await db.execute(select(func.count()).select_from(Exercise))
    ).scalar() or 0

    rows = (
        await db.execute(
            select(
                Submission.exercise_id,
                func.count(Submission.id).label("attempts"),
                func.max(Submission.score).label("best_score"),
            ).group_by(Submission.exercise_id)
        )
    ).all()

    exercises = {
        row.exercise_id: ExerciseProgress(
            best_score=row.best_score,
            attempts=row.attempts,
            solved=row.best_score == 100.0,
        )
        for row in rows
    }

    return ProgressResponse(
        total_exercises=total,
        completed_count=sum(1 for p in exercises.values() if p.solved),
        exercises=exercises,
    )
