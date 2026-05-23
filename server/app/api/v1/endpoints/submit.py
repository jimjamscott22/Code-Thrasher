from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.models.models import Exercise, Submission, SubmissionStatus
from app.schemas.schemas import SubmitRequest, SubmitResponse, TestCaseResult

router = APIRouter(prefix="/submit", tags=["submit"])


@router.post("/", response_model=SubmitResponse)
async def submit_code(
    payload: SubmitRequest,
    db: AsyncSession = Depends(get_db),
) -> SubmitResponse:
    exercise = await db.get(Exercise, payload.exercise_id)
    if not exercise:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found")

    total_weight = sum(r.score_weight for r in payload.test_results)
    earned_weight = sum(r.score_weight for r in payload.test_results if r.passed)
    score = round((earned_weight / total_weight) * 100, 2) if total_weight else 0.0
    sub_status = SubmissionStatus.completed if score == 100.0 else SubmissionStatus.failed

    submission = Submission(
        exercise_id=payload.exercise_id,
        code=payload.code,
        status=sub_status,
        score=score,
        time_taken_ms=payload.time_taken_ms,
    )
    db.add(submission)
    await db.commit()
    await db.refresh(submission)

    return SubmitResponse(
        submission_id=submission.id,
        status=sub_status,
        score=score,
        stdout="",
        stderr="",
        time_taken_ms=payload.time_taken_ms,
        test_results=[TestCaseResult(**r.model_dump()) for r in payload.test_results],
    )
