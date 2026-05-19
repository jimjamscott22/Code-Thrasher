from fastapi import APIRouter, Depends, HTTPException, Request, status
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.dependencies import get_current_user
from app.db.database import get_db
from app.models.models import Exercise, Submission, SubmissionStatus, TestCase, User
from app.schemas.schemas import SubmitRequest, SubmitResponse, TestCaseResult
from app.services.sandbox import run_in_sandbox

router = APIRouter(prefix="/submit", tags=["submit"])
limiter = Limiter(key_func=get_remote_address)


@router.post("/", response_model=SubmitResponse)
@limiter.limit("10/minute")
async def submit_code(
    request: Request,
    payload: SubmitRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> SubmitResponse:
    # Load exercise + test cases
    result = await db.execute(
        select(Exercise)
        .where(Exercise.id == payload.exercise_id)
        .options(selectinload(Exercise.test_cases))
    )
    exercise: Exercise | None = result.scalar_one_or_none()
    if not exercise:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found")

    test_cases: list[TestCase] = exercise.test_cases
    if not test_cases:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Exercise has no test cases configured",
        )

    test_results: list[TestCaseResult] = []
    total_weight = sum(tc.score_weight for tc in test_cases)
    earned_weight = 0.0
    combined_stdout = ""
    combined_stderr = ""
    max_time = 0

    for tc in test_cases:
        sandbox_result = run_in_sandbox(payload.code, stdin_data=tc.input_data)
        combined_stdout += sandbox_result.stdout
        combined_stderr += sandbox_result.stderr
        max_time = max(max_time, sandbox_result.time_taken_ms)

        actual = sandbox_result.stdout.strip()
        expected = tc.expected_output.strip()
        passed = actual == expected and not sandbox_result.timed_out

        if passed:
            earned_weight += tc.score_weight

        test_results.append(
            TestCaseResult(
                test_case_id=tc.id,
                passed=passed,
                expected=expected,
                actual=actual,
                score_weight=tc.score_weight,
            )
        )

    score = round((earned_weight / total_weight) * 100, 2) if total_weight else 0.0
    sub_status = SubmissionStatus.completed if score == 100.0 else SubmissionStatus.failed

    submission = Submission(
        user_id=current_user.id,
        exercise_id=payload.exercise_id,
        code=payload.code,
        status=sub_status,
        score=score,
        stdout=combined_stdout[: 10_000],
        stderr=combined_stderr[: 10_000],
        time_taken_ms=max_time,
    )
    db.add(submission)

    if sub_status == SubmissionStatus.completed:
        current_user.total_score += int(score)

    await db.commit()
    await db.refresh(submission)

    return SubmitResponse(
        submission_id=submission.id,
        status=sub_status,
        score=score,
        stdout=combined_stdout[: 10_000],
        stderr=combined_stderr[: 10_000],
        time_taken_ms=max_time,
        test_results=test_results,
    )
