from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.core.rate_limit import get_user_or_remote_address, limiter
from app.db.database import get_db
from app.models.models import Submission, User
from app.schemas.schemas import SubmitRequest, SubmitResponse, TestCaseResult
from app.services.grading import grade_submission
from app.services.user_stats import update_user_stats

router = APIRouter(prefix="/submit", tags=["submit"])


@router.post("/", response_model=SubmitResponse)
@limiter.limit("20/minute", key_func=get_user_or_remote_address)
async def submit_code(
    request: Request,
    payload: SubmitRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> SubmitResponse:
    try:
        grading = await grade_submission(db, payload.exercise_id, payload.code)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    await update_user_stats(db, current_user, grading.score)

    submission = Submission(
        user_id=current_user.id,
        exercise_id=payload.exercise_id,
        code=payload.code,
        status=grading.status,
        score=grading.score,
        stdout=grading.stdout,
        stderr=grading.stderr,
        time_taken_ms=payload.time_taken_ms,
    )
    db.add(submission)
    await db.commit()
    await db.refresh(submission)

    return SubmitResponse(
        submission_id=submission.id,
        status=grading.status,
        score=grading.score,
        stdout=grading.stdout,
        stderr=grading.stderr,
        time_taken_ms=payload.time_taken_ms,
        test_results=[TestCaseResult(**r.model_dump()) for r in grading.test_results],
    )
