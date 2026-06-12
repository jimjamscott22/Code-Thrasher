"""User progress aggregation."""

from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import Exercise, Submission, User
from app.schemas.schemas import ExerciseProgress, ProgressResponse


async def get_user_progress(db: AsyncSession, user: User) -> ProgressResponse:
    total: int = (
        await db.execute(select(func.count()).select_from(Exercise))
    ).scalar() or 0

    rows = (
        await db.execute(
            select(
                Submission.exercise_id,
                func.count(Submission.id).label("attempts"),
                func.max(Submission.score).label("best_score"),
            )
            .where(Submission.user_id == user.id)
            .group_by(Submission.exercise_id)
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
        completed_count=sum(1 for progress in exercises.values() if progress.solved),
        exercises=exercises,
    )
