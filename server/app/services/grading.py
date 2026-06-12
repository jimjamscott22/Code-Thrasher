"""Server-side exercise grading against database test cases."""

from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.models import Exercise, SubmissionStatus, TestCase
from app.schemas.schemas import TestCaseResult
from app.services.sandbox import run_python


@dataclass
class GradingResult:
    score: float
    status: SubmissionStatus
    test_results: list[TestCaseResult]
    stdout: str
    stderr: str


def _redact_expected(test_case: TestCase, expected: str) -> str:
    return "" if test_case.is_hidden else expected


async def grade_submission(
    db: AsyncSession,
    exercise_id: int,
    code: str,
) -> GradingResult:
    result = await db.execute(
        select(Exercise)
        .where(Exercise.id == exercise_id)
        .options(selectinload(Exercise.test_cases))
    )
    exercise = result.scalar_one_or_none()
    if exercise is None:
        raise ValueError("Exercise not found")

    test_cases = sorted(exercise.test_cases, key=lambda tc: tc.id)
    if not test_cases:
        return GradingResult(
            score=0.0,
            status=SubmissionStatus.failed,
            test_results=[],
            stdout="",
            stderr="",
        )

    test_results: list[TestCaseResult] = []
    combined_stdout: list[str] = []
    combined_stderr: list[str] = []
    total_weight = 0.0
    earned_weight = 0.0

    for test_case in test_cases:
        run = await run_python(code, test_case.input_data)
        trimmed_actual = run.stdout.strip()
        trimmed_expected = test_case.expected_output.strip()

        if run.stdout:
            combined_stdout.append(run.stdout)
        if run.stderr:
            combined_stderr.append(run.stderr)

        has_error = bool(run.stderr) or run.timed_out
        passed = not has_error and trimmed_actual == trimmed_expected

        total_weight += test_case.score_weight
        if passed:
            earned_weight += test_case.score_weight

        test_results.append(
            TestCaseResult(
                test_case_id=test_case.id,
                passed=passed,
                expected=_redact_expected(test_case, test_case.expected_output),
                actual=trimmed_actual,
                score_weight=test_case.score_weight,
            )
        )

    score = round((earned_weight / total_weight) * 100, 2) if total_weight else 0.0
    status = SubmissionStatus.completed if score == 100.0 else SubmissionStatus.failed

    return GradingResult(
        score=score,
        status=status,
        test_results=test_results,
        stdout="\n".join(combined_stdout),
        stderr="\n".join(combined_stderr),
    )
