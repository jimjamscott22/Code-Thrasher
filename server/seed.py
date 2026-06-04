#!/usr/bin/env python3
"""Seed the database with initial categories and exercises.

Run from the server/ directory:
    python seed.py
"""

import asyncio

from sqlalchemy import select

from app.db.database import AsyncSessionLocal
from app.models.models import Category, DifficultyLevel, Exercise, TestCase

CATEGORIES = [
    {"name": "Basics", "slug": "basics"},
    {"name": "Strings", "slug": "strings"},
    {"name": "Lists", "slug": "lists"},
    {"name": "Loops", "slug": "loops"},
    {"name": "Functions", "slug": "functions"},
]

# All exercises produce deterministic output (no stdin needed); test cases verify stdout.
# Exercises are therefore deterministic programs; test cases verify the expected output.
EXERCISES = [
    {
        "title": "Hello, World!",
        "description": (
            "## Hello, World!\n\n"
            "Your very first Python program. Print the classic greeting to the screen.\n\n"
            "**Expected output:**\n```\nHello, World!\n```"
        ),
        "hint": "Use the `print()` function. Strings can be wrapped in single or double quotes.",
        "difficulty_level": DifficultyLevel.beginner,
        "category_slug": "basics",
        "starter_code": "# Write your code below\n",
        "test_cases": [
            {"input_data": "", "expected_output": "Hello, World!", "score_weight": 1.0, "is_hidden": False},
            {"input_data": "", "expected_output": "Hello, World!", "score_weight": 1.0, "is_hidden": True},
        ],
    },
    {
        "title": "Variable Assignment",
        "description": (
            "## Variable Assignment\n\n"
            "Assign the integer `42` to a variable named `answer` and print it.\n\n"
            "**Expected output:**\n```\n42\n```"
        ),
        "hint": "Use the `=` operator to assign a value to a variable, then pass the variable to `print()`.",
        "difficulty_level": DifficultyLevel.beginner,
        "category_slug": "basics",
        "starter_code": "# Assign 42 to answer and print it\n",
        "test_cases": [
            {"input_data": "", "expected_output": "42", "score_weight": 1.0, "is_hidden": False},
            {"input_data": "", "expected_output": "42", "score_weight": 1.0, "is_hidden": True},
        ],
    },
    {
        "title": "Area of a Rectangle",
        "description": (
            "## Area of a Rectangle\n\n"
            "Given a `length` of 5 and a `width` of 3, calculate the area of the rectangle and print the result.\n\n"
            "**Expected output:**\n```\n15\n```"
        ),
        "hint": "The area of a rectangle is length multiplied by width (`length * width`).",
        "difficulty_level": DifficultyLevel.beginner,
        "category_slug": "basics",
        "starter_code": "length = 5\nwidth = 3\n# Calculate and print the area\n",
        "test_cases": [
            {"input_data": "", "expected_output": "15", "score_weight": 1.0, "is_hidden": False},
            {"input_data": "", "expected_output": "15", "score_weight": 1.0, "is_hidden": True},
        ],
    },
    {
        "title": "Sum 1 to 10",
        "description": (
            "## Sum 1 to 10\n\n"
            "Calculate and print the sum of all integers from 1 to 10 (inclusive).\n\n"
            "**Expected output:**\n```\n55\n```"
        ),
        "hint": "Try Python's built-in `sum()` with `range()`, or use a loop that adds to a running total.",
        "difficulty_level": DifficultyLevel.beginner,
        "category_slug": "basics",
        "starter_code": "# Print the sum of numbers from 1 to 10\n",
        "test_cases": [
            {"input_data": "", "expected_output": "55", "score_weight": 1.0, "is_hidden": False},
            {"input_data": "", "expected_output": "55", "score_weight": 1.0, "is_hidden": True},
        ],
    },
    {
        "title": "FizzBuzz",
        "description": (
            "## FizzBuzz\n\n"
            "Print numbers from 1 to 15. For multiples of 3 print `Fizz`, for multiples of 5 "
            "print `Buzz`, and for multiples of both 3 and 5 print `FizzBuzz`.\n\n"
            "**Expected output:**\n```\n1\n2\nFizz\n4\nBuzz\nFizz\n7\n8\nFizz\nBuzz\n11\nFizz\n13\n14\nFizzBuzz\n```"
        ),
        "hint": "Use the modulo operator `%` to check divisibility. Check the combined condition (divisible by both 3 and 5) *before* checking each one individually.",
        "difficulty_level": DifficultyLevel.beginner,
        "category_slug": "loops",
        "starter_code": "for i in range(1, 16):\n    pass  # replace with your logic\n",
        "test_cases": [
            {
                "input_data": "",
                "expected_output": "1\n2\nFizz\n4\nBuzz\nFizz\n7\n8\nFizz\nBuzz\n11\nFizz\n13\n14\nFizzBuzz",
                "score_weight": 1.0,
                "is_hidden": False,
            },
            {
                "input_data": "",
                "expected_output": "1\n2\nFizz\n4\nBuzz\nFizz\n7\n8\nFizz\nBuzz\n11\nFizz\n13\n14\nFizzBuzz",
                "score_weight": 1.0,
                "is_hidden": True,
            },
        ],
    },
    {
        "title": "Reverse a String",
        "description": (
            "## Reverse a String\n\n"
            'Reverse the string `"Python"` and print the result.\n\n'
            "**Expected output:**\n```\nnohtyP\n```"
        ),
        "hint": "Python strings support slicing. The slice `[::-1]` reverses any sequence.",
        "difficulty_level": DifficultyLevel.beginner,
        "category_slug": "strings",
        "starter_code": 'word = "Python"\n# Print the reversed string\n',
        "test_cases": [
            {"input_data": "", "expected_output": "nohtyP", "score_weight": 1.0, "is_hidden": False},
            {"input_data": "", "expected_output": "nohtyP", "score_weight": 1.0, "is_hidden": True},
        ],
    },
    {
        "title": "Count Vowels",
        "description": (
            "## Count Vowels\n\n"
            'Count the number of vowels (a, e, i, o, u — case-insensitive) in `"Hello, World!"` '
            "and print the count.\n\n"
            "**Expected output:**\n```\n3\n```"
        ),
        "hint": "Loop through each character and check if it's in the set of vowels. Use `.lower()` to handle uppercase letters.",
        "difficulty_level": DifficultyLevel.beginner,
        "category_slug": "strings",
        "starter_code": 'text = "Hello, World!"\n# Count and print the number of vowels\n',
        "test_cases": [
            {"input_data": "", "expected_output": "3", "score_weight": 1.0, "is_hidden": False},
            {"input_data": "", "expected_output": "3", "score_weight": 1.0, "is_hidden": True},
        ],
    },
    {
        "title": "List Maximum",
        "description": (
            "## List Maximum\n\n"
            "Find and print the largest number in `[3, 1, 4, 1, 5, 9, 2, 6, 5, 3]`.\n\n"
            "**Expected output:**\n```\n9\n```"
        ),
        "hint": "Python has a built-in `max()` function that works on any iterable.",
        "difficulty_level": DifficultyLevel.beginner,
        "category_slug": "lists",
        "starter_code": "numbers = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]\n# Print the maximum value\n",
        "test_cases": [
            {"input_data": "", "expected_output": "9", "score_weight": 1.0, "is_hidden": False},
            {"input_data": "", "expected_output": "9", "score_weight": 1.0, "is_hidden": True},
        ],
    },
    {
        "title": "Palindrome Check",
        "description": (
            "## Palindrome Check\n\n"
            'A palindrome reads the same forwards and backwards. Check whether `"racecar"` is a '
            "palindrome and print `True` or `False`.\n\n"
            "**Expected output:**\n```\nTrue\n```"
        ),
        "hint": "Compare the string to its reverse. If they're equal, it's a palindrome. Try `word == word[::-1]`.",
        "difficulty_level": DifficultyLevel.intermediate,
        "category_slug": "strings",
        "starter_code": 'word = "racecar"\n# Print True if word is a palindrome, False otherwise\n',
        "test_cases": [
            {"input_data": "", "expected_output": "True", "score_weight": 1.0, "is_hidden": False},
            {"input_data": "", "expected_output": "True", "score_weight": 1.0, "is_hidden": True},
        ],
    },
    {
        "title": "Fibonacci Sequence",
        "description": (
            "## Fibonacci Sequence\n\n"
            "Print the first 10 numbers of the Fibonacci sequence, one per line. "
            "The sequence starts with 0 and 1; each subsequent number is the sum of the two before it.\n\n"
            "**Expected output:**\n```\n0\n1\n1\n2\n3\n5\n8\n13\n21\n34\n```"
        ),
        "hint": "Use two variables to track the last two numbers. Start with `a, b = 0, 1`, print `a`, then update: `a, b = b, a + b`.",
        "difficulty_level": DifficultyLevel.intermediate,
        "category_slug": "loops",
        "starter_code": "# Print the first 10 Fibonacci numbers, one per line\n",
        "test_cases": [
            {
                "input_data": "",
                "expected_output": "0\n1\n1\n2\n3\n5\n8\n13\n21\n34",
                "score_weight": 1.0,
                "is_hidden": False,
            },
            {
                "input_data": "",
                "expected_output": "0\n1\n1\n2\n3\n5\n8\n13\n21\n34",
                "score_weight": 1.0,
                "is_hidden": True,
            },
        ],
    },
    {
        "title": "List Comprehension: Even Squares",
        "description": (
            "## List Comprehension: Even Squares\n\n"
            "Use a list comprehension to create a list of the squares of all even numbers from 1 to 10. "
            "Print each square on its own line.\n\n"
            "**Expected output:**\n```\n4\n16\n36\n64\n100\n```"
        ),
        "hint": "A list comprehension looks like `[expr for x in iterable if condition]`. Filter even numbers with `if n % 2 == 0`, then square with `n ** 2`.",
        "difficulty_level": DifficultyLevel.intermediate,
        "category_slug": "lists",
        "starter_code": "# Build a list of squares of even numbers from 1 to 10, then print each value\n",
        "test_cases": [
            {
                "input_data": "",
                "expected_output": "4\n16\n36\n64\n100",
                "score_weight": 1.0,
                "is_hidden": False,
            },
            {
                "input_data": "",
                "expected_output": "4\n16\n36\n64\n100",
                "score_weight": 1.0,
                "is_hidden": True,
            },
        ],
    },
    {
        "title": "Caesar Cipher",
        "description": (
            "## Caesar Cipher\n\n"
            'Encrypt the message `"hello"` using a Caesar cipher with a shift of 3 and print the result.\n\n'
            "In a Caesar cipher each letter is shifted forward by the shift amount, wrapping from z back to a.\n\n"
            "**Expected output:**\n```\nkhoor\n```"
        ),
        "hint": (
            "Use `ord()` to get a character's ASCII value and `chr()` to convert back. "
            "For a lowercase letter `c` with shift `s`: `chr((ord(c) - ord('a') + s) % 26 + ord('a'))`."
        ),
        "difficulty_level": DifficultyLevel.intermediate,
        "category_slug": "strings",
        "starter_code": 'message = "hello"\nshift = 3\n# Print the Caesar cipher encrypted message\n',
        "test_cases": [
            {"input_data": "", "expected_output": "khoor", "score_weight": 1.0, "is_hidden": False},
            {"input_data": "", "expected_output": "khoor", "score_weight": 1.0, "is_hidden": True},
        ],
    },
]


async def seed() -> None:
    async with AsyncSessionLocal() as db:
        # Upsert categories and build a slug → model map
        category_map: dict[str, Category] = {}
        for cat_data in CATEGORIES:
            result = await db.execute(select(Category).where(Category.slug == cat_data["slug"]))
            cat = result.scalar_one_or_none()
            if not cat:
                cat = Category(**cat_data)
                db.add(cat)
                await db.flush()
                print(f"  Created category: {cat_data['name']}")
            category_map[cat_data["slug"]] = cat

        # Insert exercises (skip if title already exists)
        for ex_data in EXERCISES:
            result = await db.execute(select(Exercise).where(Exercise.title == ex_data["title"]))
            if result.scalar_one_or_none():
                print(f"  Skipping (already exists): {ex_data['title']}")
                continue

            tc_list = ex_data.pop("test_cases")
            cat_slug = ex_data.pop("category_slug")

            exercise = Exercise(**ex_data, category=category_map[cat_slug])
            db.add(exercise)
            await db.flush()

            for tc_data in tc_list:
                db.add(TestCase(exercise_id=exercise.id, **tc_data))

            print(f"  Created exercise: {exercise.title}")

        await db.commit()
        print("\nSeeding complete.")


if __name__ == "__main__":
    asyncio.run(seed())
