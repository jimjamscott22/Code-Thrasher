"""Ad-hoc execution of user code for an exercise: no grading, nothing persisted."""

from __future__ import annotations

import time

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import Exercise
from app.schemas.schemas import RunResponse
from app.services.sandbox import code_runner


async def run_exercise_code(
    db: AsyncSession,
    exercise_id: int,
    code: str,
    input_data: str = "",
) -> RunResponse:
    result = await db.execute(select(Exercise.language).where(Exercise.id == exercise_id))
    language = result.scalar_one_or_none()
    if language is None:
        raise ValueError("Exercise not found")

    started = time.perf_counter()
    async with code_runner(language, code) as run_code:
        run = await run_code(input_data)
    duration_ms = round((time.perf_counter() - started) * 1000)

    return RunResponse(
        stdout=run.stdout,
        stderr=run.stderr,
        timed_out=run.timed_out,
        output_truncated=run.output_truncated,
        duration_ms=duration_ms,
    )
