"""Catalog checks for seeded exercises.

Every exercise must ship with a guide and a worked solution, and that solution
must produce the expected stdout for every test case.
"""

import pytest

from app.services.sandbox import run_python
from seed import EXERCISE_GUIDES, EXERCISE_SOLUTIONS, EXERCISES


def test_every_exercise_has_guide_and_solution():
    titles = [exercise["title"] for exercise in EXERCISES]
    assert len(titles) == len(set(titles))

    for exercise in EXERCISES:
        title = exercise["title"]
        guide = EXERCISE_GUIDES[title]
        solution = EXERCISE_SOLUTIONS[title]
        assert guide, title
        kinds = {block["kind"] for block in guide}
        assert {"nudge", "pattern", "checklist"} <= kinds
        assert solution["code"].strip(), title
        assert solution["explanation"].strip(), title
        assert exercise["test_cases"], title


@pytest.mark.asyncio
async def test_seeded_solutions_match_expected_output():
    for exercise in EXERCISES:
        code = EXERCISE_SOLUTIONS[exercise["title"]]["code"]
        for test_case in exercise["test_cases"]:
            result = await run_python(code, input_data=test_case["input_data"])
            assert not result.timed_out, exercise["title"]
            assert result.stderr == "", f"{exercise['title']}: {result.stderr}"
            assert (
                result.stdout.strip() == test_case["expected_output"].strip()
            ), exercise["title"]
