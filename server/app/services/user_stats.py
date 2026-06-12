"""Update user score and streak after a submission."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import Submission, User


async def update_user_stats(db: AsyncSession, user: User, score: float) -> None:
    user.total_score += int(score)

    now = datetime.now(UTC)
    today = now.date()
    yesterday = today - timedelta(days=1)

    last_submission_at = (
        await db.execute(
            select(func.max(Submission.created_at)).where(Submission.user_id == user.id)
        )
    ).scalar_one_or_none()

    if last_submission_at is None:
        user.streak = max(user.streak, 1)
        return

    last_date = last_submission_at.date()
    if last_date == today:
        return
    if last_date == yesterday:
        user.streak += 1
    else:
        user.streak = 1
