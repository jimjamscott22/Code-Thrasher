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
    {
        "title": "Greet by Name",
        "description": (
            "## Greet by Name\n\n"
            'A variable `name` holds the string `"Ada"`. Print a greeting in the form '
            "`Hello, Ada!`.\n\n"
            "**Expected output:**\n```\nHello, Ada!\n```"
        ),
        "hint": "Use an f-string: put an `f` before the opening quote and wrap the variable in `{}`, e.g. `f\"Hi {name}\"`.",
        "difficulty_level": DifficultyLevel.beginner,
        "category_slug": "strings",
        "starter_code": 'name = "Ada"\n# Print a greeting that includes the name\n',
        "test_cases": [
            {"input_data": "", "expected_output": "Hello, Ada!", "score_weight": 1.0, "is_hidden": False},
            {"input_data": "", "expected_output": "Hello, Ada!", "score_weight": 1.0, "is_hidden": True},
        ],
    },
    {
        "title": "Even or Odd",
        "description": (
            "## Even or Odd\n\n"
            "A variable `number` holds the integer `7`. Print `Even` if it is even, "
            "or `Odd` if it is odd.\n\n"
            "**Expected output:**\n```\nOdd\n```"
        ),
        "hint": "A number is even when `number % 2 == 0`. Use an `if`/`else` to choose which word to print.",
        "difficulty_level": DifficultyLevel.beginner,
        "category_slug": "basics",
        "starter_code": "number = 7\n# Print \"Even\" or \"Odd\"\n",
        "test_cases": [
            {"input_data": "", "expected_output": "Odd", "score_weight": 1.0, "is_hidden": False},
            {"input_data": "", "expected_output": "Odd", "score_weight": 1.0, "is_hidden": True},
        ],
    },
    {
        "title": "Seconds in a Day",
        "description": (
            "## Seconds in a Day\n\n"
            "Calculate how many seconds there are in a single day and print the result. "
            "There are 24 hours in a day, 60 minutes in an hour, and 60 seconds in a minute.\n\n"
            "**Expected output:**\n```\n86400\n```"
        ),
        "hint": "Multiply the three values together: hours per day, minutes per hour, and seconds per minute.",
        "difficulty_level": DifficultyLevel.beginner,
        "category_slug": "basics",
        "starter_code": "# Calculate and print the number of seconds in one day\n",
        "test_cases": [
            {"input_data": "", "expected_output": "86400", "score_weight": 1.0, "is_hidden": False},
            {"input_data": "", "expected_output": "86400", "score_weight": 1.0, "is_hidden": True},
        ],
    },
    {
        "title": "String Length",
        "description": (
            "## String Length\n\n"
            'A variable `text` holds the string `"programming"`. Print how many characters '
            "it contains.\n\n"
            "**Expected output:**\n```\n11\n```"
        ),
        "hint": "Python's built-in `len()` returns the number of characters in a string.",
        "difficulty_level": DifficultyLevel.beginner,
        "category_slug": "strings",
        "starter_code": 'text = "programming"\n# Print the length of text\n',
        "test_cases": [
            {"input_data": "", "expected_output": "11", "score_weight": 1.0, "is_hidden": False},
            {"input_data": "", "expected_output": "11", "score_weight": 1.0, "is_hidden": True},
        ],
    },
    {
        "title": "Count to Five",
        "description": (
            "## Count to Five\n\n"
            "Print the numbers 1 through 5, each on its own line.\n\n"
            "**Expected output:**\n```\n1\n2\n3\n4\n5\n```"
        ),
        "hint": "Loop with `for i in range(1, 6):` and print `i` inside the loop. `range()` stops before its second argument.",
        "difficulty_level": DifficultyLevel.beginner,
        "category_slug": "loops",
        "starter_code": "# Print the numbers 1 through 5, one per line\n",
        "test_cases": [
            {"input_data": "", "expected_output": "1\n2\n3\n4\n5", "score_weight": 1.0, "is_hidden": False},
            {"input_data": "", "expected_output": "1\n2\n3\n4\n5", "score_weight": 1.0, "is_hidden": True},
        ],
    },
    {
        "title": "Sum of a List",
        "description": (
            "## Sum of a List\n\n"
            "A variable `numbers` holds `[10, 20, 30, 40]`. Print the sum of all its values.\n\n"
            "**Expected output:**\n```\n100\n```"
        ),
        "hint": "The built-in `sum()` function adds up every item in a list.",
        "difficulty_level": DifficultyLevel.beginner,
        "category_slug": "lists",
        "starter_code": "numbers = [10, 20, 30, 40]\n# Print the sum of the list\n",
        "test_cases": [
            {"input_data": "", "expected_output": "100", "score_weight": 1.0, "is_hidden": False},
            {"input_data": "", "expected_output": "100", "score_weight": 1.0, "is_hidden": True},
        ],
    },
    {
        "title": "Multiplication Table",
        "description": (
            "## Multiplication Table\n\n"
            "Print the 7 times table from 1 to 10. Print each product on its own line "
            "(`7 × 1`, `7 × 2`, ... up to `7 × 10`).\n\n"
            "**Expected output:**\n```\n7\n14\n21\n28\n35\n42\n49\n56\n63\n70\n```"
        ),
        "hint": "Loop `for i in range(1, 11):` and print `7 * i` on each pass.",
        "difficulty_level": DifficultyLevel.intermediate,
        "category_slug": "loops",
        "starter_code": "# Print the 7 times table, one product per line\n",
        "test_cases": [
            {
                "input_data": "",
                "expected_output": "7\n14\n21\n28\n35\n42\n49\n56\n63\n70",
                "score_weight": 1.0,
                "is_hidden": False,
            },
            {
                "input_data": "",
                "expected_output": "7\n14\n21\n28\n35\n42\n49\n56\n63\n70",
                "score_weight": 1.0,
                "is_hidden": True,
            },
        ],
    },
    {
        "title": "Count Words",
        "description": (
            "## Count Words\n\n"
            'A variable `sentence` holds `"the quick brown fox"`. Print how many words it '
            "contains.\n\n"
            "**Expected output:**\n```\n4\n```"
        ),
        "hint": "`sentence.split()` breaks the string into a list of words. Use `len()` on that list.",
        "difficulty_level": DifficultyLevel.intermediate,
        "category_slug": "strings",
        "starter_code": 'sentence = "the quick brown fox"\n# Print the number of words\n',
        "test_cases": [
            {"input_data": "", "expected_output": "4", "score_weight": 1.0, "is_hidden": False},
            {"input_data": "", "expected_output": "4", "score_weight": 1.0, "is_hidden": True},
        ],
    },
    {
        "title": "Factorial",
        "description": (
            "## Factorial\n\n"
            "The factorial of a number is the product of all positive integers up to and "
            "including it. Calculate the factorial of `5` (5 × 4 × 3 × 2 × 1) and print it.\n\n"
            "**Expected output:**\n```\n120\n```"
        ),
        "hint": "Start a running total at 1, then multiply it by each number from 1 to 5 in a loop.",
        "difficulty_level": DifficultyLevel.intermediate,
        "category_slug": "loops",
        "starter_code": "n = 5\n# Calculate and print n factorial\n",
        "test_cases": [
            {"input_data": "", "expected_output": "120", "score_weight": 1.0, "is_hidden": False},
            {"input_data": "", "expected_output": "120", "score_weight": 1.0, "is_hidden": True},
        ],
    },
    {
        "title": "Filter Positive Numbers",
        "description": (
            "## Filter Positive Numbers\n\n"
            "A variable `numbers` holds `[-2, 3, -1, 5, 0, 7]`. Print only the numbers "
            "greater than zero, each on its own line, keeping their original order.\n\n"
            "**Expected output:**\n```\n3\n5\n7\n```"
        ),
        "hint": "Loop through the list and use `if n > 0:` to decide whether to print each value. Note that 0 is not positive.",
        "difficulty_level": DifficultyLevel.intermediate,
        "category_slug": "lists",
        "starter_code": "numbers = [-2, 3, -1, 5, 0, 7]\n# Print each positive number on its own line\n",
        "test_cases": [
            {"input_data": "", "expected_output": "3\n5\n7", "score_weight": 1.0, "is_hidden": False},
            {"input_data": "", "expected_output": "3\n5\n7", "score_weight": 1.0, "is_hidden": True},
        ],
    },
]


EXERCISE_GUIDES = {
    "Hello, World!": [
        {
            "kind": "nudge",
            "title": "Name the one action",
            "body": "This challenge only needs one instruction: send a string to the output.",
        },
        {
            "kind": "pattern",
            "title": "Useful Python tool",
            "body": "`print()` writes whatever you pass it to stdout. Wrap text in quotes so Python treats it as a string.",
            "code": 'print("some text")',
        },
        {
            "kind": "checklist",
            "title": "Output check",
            "body": "Match the capitalization, comma, space, and exclamation mark exactly.",
        },
    ],
    "Variable Assignment": [
        {
            "kind": "nudge",
            "title": "Store before printing",
            "body": "Create a variable first, then print the variable name rather than typing the number directly in `print()`.",
        },
        {
            "kind": "pattern",
            "title": "Assignment pattern",
            "body": "The left side is the name. The right side is the value you want to store.",
            "code": "name = value\nprint(name)",
        },
        {
            "kind": "checklist",
            "title": "Output check",
            "body": "The printed result should be the number only, with no label or extra words.",
        },
    ],
    "Area of a Rectangle": [
        {
            "kind": "nudge",
            "title": "Translate the formula",
            "body": "The area formula is already in the prompt. Your job is to express it with the variables provided.",
        },
        {
            "kind": "pattern",
            "title": "Multiplication",
            "body": "Python uses `*` for multiplication.",
            "code": "total = first_number * second_number\nprint(total)",
        },
        {
            "kind": "checklist",
            "title": "Output check",
            "body": "Print the computed area, not the formula text.",
        },
    ],
    "Sum 1 to 10": [
        {
            "kind": "nudge",
            "title": "Inclusive ranges",
            "body": "`range()` stops before its ending value, so include 11 when you want to reach 10.",
        },
        {
            "kind": "pattern",
            "title": "Built-in summing",
            "body": "`sum()` can add every value produced by a range.",
            "code": "total = sum(range(1, 4))\nprint(total)",
        },
        {
            "kind": "checklist",
            "title": "Output check",
            "body": "You only need to print the final total once.",
        },
    ],
    "FizzBuzz": [
        {
            "kind": "nudge",
            "title": "Order matters",
            "body": "Check the combined case first. Numbers divisible by both 3 and 5 are also divisible by each individually.",
        },
        {
            "kind": "pattern",
            "title": "Modulo test",
            "body": "`n % divisor == 0` means there is no remainder.",
            "code": "if n % 3 == 0:\n    print(\"Fizz\")",
        },
        {
            "kind": "checklist",
            "title": "Output check",
            "body": "Print exactly one line for each number from 1 through 15.",
        },
    ],
    "Reverse a String": [
        {
            "kind": "nudge",
            "title": "Think sequence",
            "body": "Strings behave like sequences, so slicing can create a reversed copy.",
        },
        {
            "kind": "pattern",
            "title": "Reverse slice",
            "body": "The step value `-1` walks backward through a sequence.",
            "code": "reversed_text = text[::-1]\nprint(reversed_text)",
        },
        {
            "kind": "checklist",
            "title": "Output check",
            "body": "Do not print quotes around the reversed word.",
        },
    ],
    "Count Vowels": [
        {
            "kind": "nudge",
            "title": "Normalize the letters",
            "body": "Lowercase each character before checking it so uppercase vowels are counted too.",
        },
        {
            "kind": "pattern",
            "title": "Membership test",
            "body": "`in` can check whether a character appears inside a string of allowed letters.",
            "code": "if char.lower() in \"aeiou\":\n    count += 1",
        },
        {
            "kind": "checklist",
            "title": "Output check",
            "body": "Print the count after the loop has inspected every character.",
        },
    ],
    "List Maximum": [
        {
            "kind": "nudge",
            "title": "Let Python scan",
            "body": "You do not need to sort the list. Python has a built-in that finds the largest value.",
        },
        {
            "kind": "pattern",
            "title": "Maximum value",
            "body": "`max()` accepts a list and returns its largest item.",
            "code": "largest = max(values)\nprint(largest)",
        },
        {
            "kind": "checklist",
            "title": "Output check",
            "body": "Print the number itself, not the whole list.",
        },
    ],
    "Palindrome Check": [
        {
            "kind": "nudge",
            "title": "Compare both directions",
            "body": "A palindrome is unchanged when reversed. That means this can be a comparison expression.",
        },
        {
            "kind": "pattern",
            "title": "Boolean expression",
            "body": "Comparisons produce `True` or `False`, which can be printed directly.",
            "code": "is_match = word == word[::-1]\nprint(is_match)",
        },
        {
            "kind": "checklist",
            "title": "Output check",
            "body": "Python booleans are capitalized: `True` and `False`.",
        },
    ],
    "Fibonacci Sequence": [
        {
            "kind": "nudge",
            "title": "Carry two numbers",
            "body": "Each new Fibonacci value depends on the two previous values, so keep both in variables.",
        },
        {
            "kind": "pattern",
            "title": "Tuple update",
            "body": "Python can update two variables at once without losing the old values.",
            "code": "a, b = b, a + b",
        },
        {
            "kind": "checklist",
            "title": "Output check",
            "body": "Print before updating so the sequence starts with 0.",
        },
    ],
    "List Comprehension: Even Squares": [
        {
            "kind": "nudge",
            "title": "Filter then transform",
            "body": "Keep only even numbers, then square the numbers that passed the filter.",
        },
        {
            "kind": "pattern",
            "title": "Comprehension shape",
            "body": "Read it as: make `expression` for each `item` in a collection if a condition is true.",
            "code": "results = [expression for item in items if condition]",
        },
        {
            "kind": "checklist",
            "title": "Output check",
            "body": "The challenge asks for one square per line, so loop over the finished list to print values.",
        },
    ],
    "Caesar Cipher": [
        {
            "kind": "nudge",
            "title": "Shift from zero",
            "body": "Convert each letter to a zero-based position, add the shift, then wrap around the alphabet.",
        },
        {
            "kind": "pattern",
            "title": "Wrap with modulo",
            "body": "`% 26` keeps the shifted position inside the alphabet.",
            "code": "shifted = (position + shift) % 26",
        },
        {
            "kind": "checklist",
            "title": "Output check",
            "body": "Build the encrypted characters into a string, then print that string once.",
        },
    ],
    "Greet by Name": [
        {
            "kind": "nudge",
            "title": "Insert the variable",
            "body": "The greeting is fixed text with the name dropped into the middle of it.",
        },
        {
            "kind": "pattern",
            "title": "f-string interpolation",
            "body": "An `f` before the quotes lets you embed a variable inside `{}`.",
            "code": 'greeting = f"Hello, {name}!"\nprint(greeting)',
        },
        {
            "kind": "checklist",
            "title": "Output check",
            "body": "Match the comma, space, and exclamation mark exactly.",
        },
    ],
    "Even or Odd": [
        {
            "kind": "nudge",
            "title": "Check the remainder",
            "body": "Dividing by 2 leaves a remainder of 0 for even numbers and 1 for odd ones.",
        },
        {
            "kind": "pattern",
            "title": "Branch on a test",
            "body": "An `if`/`else` picks one of two outputs based on a condition.",
            "code": "if number % 2 == 0:\n    print(\"Even\")\nelse:\n    print(\"Odd\")",
        },
        {
            "kind": "checklist",
            "title": "Output check",
            "body": "Print only one word, capitalized exactly as shown.",
        },
    ],
    "Seconds in a Day": [
        {
            "kind": "nudge",
            "title": "Chain the units",
            "body": "Each unit converts into the next: hours into minutes, minutes into seconds.",
        },
        {
            "kind": "pattern",
            "title": "Multiply the factors",
            "body": "Multiplying the conversion factors together gives the total.",
            "code": "total = 24 * 60 * 60\nprint(total)",
        },
        {
            "kind": "checklist",
            "title": "Output check",
            "body": "Print the final number only, with no units or labels.",
        },
    ],
    "String Length": [
        {
            "kind": "nudge",
            "title": "Let Python count",
            "body": "You do not need to loop. A built-in already reports a string's character count.",
        },
        {
            "kind": "pattern",
            "title": "Length built-in",
            "body": "`len()` returns how many characters a string holds.",
            "code": "size = len(text)\nprint(size)",
        },
        {
            "kind": "checklist",
            "title": "Output check",
            "body": "Print the number itself, not the original string.",
        },
    ],
    "Count to Five": [
        {
            "kind": "nudge",
            "title": "Range stops early",
            "body": "`range()` ends one short of its second argument, so reach 6 to include 5.",
        },
        {
            "kind": "pattern",
            "title": "Loop and print",
            "body": "Printing inside the loop produces one line per pass.",
            "code": "for i in range(1, 6):\n    print(i)",
        },
        {
            "kind": "checklist",
            "title": "Output check",
            "body": "Five lines total, from 1 up to 5 in order.",
        },
    ],
    "Sum of a List": [
        {
            "kind": "nudge",
            "title": "Add them all",
            "body": "You want a single total of every value in the list.",
        },
        {
            "kind": "pattern",
            "title": "Built-in summing",
            "body": "`sum()` accepts a list and returns the total of its items.",
            "code": "total = sum(values)\nprint(total)",
        },
        {
            "kind": "checklist",
            "title": "Output check",
            "body": "Print the total once, not each item.",
        },
    ],
    "Multiplication Table": [
        {
            "kind": "nudge",
            "title": "Repeat with a multiplier",
            "body": "Each line is 7 multiplied by the current loop number.",
        },
        {
            "kind": "pattern",
            "title": "Multiply inside a loop",
            "body": "The loop variable supplies the changing factor each pass.",
            "code": "for i in range(1, 11):\n    print(7 * i)",
        },
        {
            "kind": "checklist",
            "title": "Output check",
            "body": "Ten lines, from 7 up to 70, with no extra text.",
        },
    ],
    "Count Words": [
        {
            "kind": "nudge",
            "title": "Split then count",
            "body": "Break the sentence into separate words first, then count how many there are.",
        },
        {
            "kind": "pattern",
            "title": "Split and measure",
            "body": "`.split()` with no argument divides on whitespace into a list.",
            "code": "words = sentence.split()\nprint(len(words))",
        },
        {
            "kind": "checklist",
            "title": "Output check",
            "body": "Print the count number only.",
        },
    ],
    "Factorial": [
        {
            "kind": "nudge",
            "title": "Multiply step by step",
            "body": "Keep a running product and multiply it by each number along the way.",
        },
        {
            "kind": "pattern",
            "title": "Accumulate a product",
            "body": "Start at 1 so the first multiplication keeps the real value.",
            "code": "result = 1\nfor i in range(1, n + 1):\n    result *= i\nprint(result)",
        },
        {
            "kind": "checklist",
            "title": "Output check",
            "body": "Print the final product after the loop finishes.",
        },
    ],
    "Filter Positive Numbers": [
        {
            "kind": "nudge",
            "title": "Decide per number",
            "body": "Visit each value and keep only the ones greater than zero. Zero does not count.",
        },
        {
            "kind": "pattern",
            "title": "Conditional print",
            "body": "An `if` inside the loop prints only the values that pass the test.",
            "code": "for n in numbers:\n    if n > 0:\n        print(n)",
        },
        {
            "kind": "checklist",
            "title": "Output check",
            "body": "Keep the original order and print each kept value on its own line.",
        },
    ],
}


EXERCISE_SOLUTIONS = {
    "Hello, World!": {
        "code": 'print("Hello, World!")',
        "explanation": "`print()` sends the exact greeting string to stdout.",
    },
    "Variable Assignment": {
        "code": "answer = 42\nprint(answer)",
        "explanation": "The value is stored in `answer`, then the variable is printed.",
    },
    "Area of a Rectangle": {
        "code": "length = 5\nwidth = 3\narea = length * width\nprint(area)",
        "explanation": "Multiplying length by width gives the rectangle area.",
    },
    "Sum 1 to 10": {
        "code": "print(sum(range(1, 11)))",
        "explanation": "`range(1, 11)` produces 1 through 10, and `sum()` adds them.",
    },
    "FizzBuzz": {
        "code": (
            "for i in range(1, 16):\n"
            "    if i % 15 == 0:\n"
            "        print(\"FizzBuzz\")\n"
            "    elif i % 3 == 0:\n"
            "        print(\"Fizz\")\n"
            "    elif i % 5 == 0:\n"
            "        print(\"Buzz\")\n"
            "    else:\n"
            "        print(i)"
        ),
        "explanation": "Checking divisibility by 15 first handles numbers divisible by both 3 and 5.",
    },
    "Reverse a String": {
        "code": 'word = "Python"\nprint(word[::-1])',
        "explanation": "The slice step `-1` walks through the string backward.",
    },
    "Count Vowels": {
        "code": (
            'text = "Hello, World!"\n'
            "count = 0\n"
            "for char in text:\n"
            "    if char.lower() in \"aeiou\":\n"
            "        count += 1\n"
            "print(count)"
        ),
        "explanation": "Lowercasing each character makes the vowel check case-insensitive.",
    },
    "List Maximum": {
        "code": "numbers = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]\nprint(max(numbers))",
        "explanation": "`max()` scans the list and returns the largest number.",
    },
    "Palindrome Check": {
        "code": 'word = "racecar"\nprint(word == word[::-1])',
        "explanation": "The comparison prints `True` because the word equals its reversed copy.",
    },
    "Fibonacci Sequence": {
        "code": "a, b = 0, 1\nfor _ in range(10):\n    print(a)\n    a, b = b, a + b",
        "explanation": "Each loop prints the current value, then advances the two-number window.",
    },
    "List Comprehension: Even Squares": {
        "code": "squares = [n ** 2 for n in range(1, 11) if n % 2 == 0]\nfor square in squares:\n    print(square)",
        "explanation": "The comprehension filters even numbers before squaring them.",
    },
    "Caesar Cipher": {
        "code": (
            'message = "hello"\n'
            "shift = 3\n"
            'encrypted = ""\n'
            "for char in message:\n"
            "    encrypted += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))\n"
            "print(encrypted)"
        ),
        "explanation": "Each character is converted to an alphabet index, shifted, wrapped, and converted back.",
    },
    "Greet by Name": {
        "code": 'name = "Ada"\nprint(f"Hello, {name}!")',
        "explanation": "The f-string drops the value of `name` into the greeting text.",
    },
    "Even or Odd": {
        "code": "number = 7\nif number % 2 == 0:\n    print(\"Even\")\nelse:\n    print(\"Odd\")",
        "explanation": "A remainder of 0 when divided by 2 means even; otherwise the number is odd.",
    },
    "Seconds in a Day": {
        "code": "print(24 * 60 * 60)",
        "explanation": "Multiplying hours, minutes, and seconds per unit gives 86400 seconds.",
    },
    "String Length": {
        "code": 'text = "programming"\nprint(len(text))',
        "explanation": "`len()` counts the characters in the string.",
    },
    "Count to Five": {
        "code": "for i in range(1, 6):\n    print(i)",
        "explanation": "`range(1, 6)` yields 1 through 5, each printed on its own line.",
    },
    "Sum of a List": {
        "code": "numbers = [10, 20, 30, 40]\nprint(sum(numbers))",
        "explanation": "`sum()` adds every value in the list and returns the total.",
    },
    "Multiplication Table": {
        "code": "for i in range(1, 11):\n    print(7 * i)",
        "explanation": "Each pass multiplies 7 by the current loop number from 1 to 10.",
    },
    "Count Words": {
        "code": 'sentence = "the quick brown fox"\nprint(len(sentence.split()))',
        "explanation": "`split()` produces a list of words, and `len()` counts them.",
    },
    "Factorial": {
        "code": "n = 5\nresult = 1\nfor i in range(1, n + 1):\n    result *= i\nprint(result)",
        "explanation": "The running product is multiplied by each number from 1 to 5.",
    },
    "Filter Positive Numbers": {
        "code": "numbers = [-2, 3, -1, 5, 0, 7]\nfor n in numbers:\n    if n > 0:\n        print(n)",
        "explanation": "Only values strictly greater than zero are printed, preserving order.",
    },
}


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

        # Insert exercises and refresh guide content for rows seeded before guides existed.
        for ex_data in EXERCISES:
            title = ex_data["title"]
            guide = EXERCISE_GUIDES.get(title, [])
            solution = EXERCISE_SOLUTIONS.get(title, {})

            result = await db.execute(select(Exercise).where(Exercise.title == ex_data["title"]))
            existing_exercise = result.scalar_one_or_none()
            if existing_exercise:
                existing_exercise.guide = guide
                existing_exercise.solution_code = solution.get("code")
                existing_exercise.solution_explanation = solution.get("explanation")
                print(f"  Updated guide: {title}")
                continue

            tc_list = ex_data["test_cases"]
            cat_slug = ex_data["category_slug"]
            exercise_data = {
                key: value
                for key, value in ex_data.items()
                if key not in {"test_cases", "category_slug"}
            }

            exercise = Exercise(
                **exercise_data,
                category=category_map[cat_slug],
                guide=guide,
                solution_code=solution.get("code"),
                solution_explanation=solution.get("explanation"),
            )
            db.add(exercise)
            await db.flush()

            for tc_data in tc_list:
                db.add(TestCase(exercise_id=exercise.id, **tc_data))

            print(f"  Created exercise: {exercise.title}")

        await db.commit()
        print("\nSeeding complete.")


if __name__ == "__main__":
    asyncio.run(seed())
