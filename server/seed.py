#!/usr/bin/env python3
"""Seed the database with initial categories and exercises.

Run from the server/ directory:
    python seed.py
"""

import asyncio

from sqlalchemy import select

from app.db.database import AsyncSessionLocal
from app.models.models import Category, DifficultyLevel, Exercise, Resource, TestCase

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
    {
        "title": "Define a Function",
        "description": (
            "## Define a Function\n\n"
            "Define a function named `greet` that prints `\"Hello from a function!\"`. "
            "Then, call the function.\n\n"
            "**Expected output:**\n```\nHello from a function!\n```"
        ),
        "hint": "Use the `def` keyword to define a function, and don't forget to call it afterwards with `greet()`.",
        "difficulty_level": DifficultyLevel.beginner,
        "category_slug": "functions",
        "starter_code": "# Define and call your function here\n",
        "test_cases": [
            {"input_data": "", "expected_output": "Hello from a function!", "score_weight": 1.0, "is_hidden": False},
            {"input_data": "", "expected_output": "Hello from a function!", "score_weight": 1.0, "is_hidden": True},
        ],
    },
    {
        "title": "Function with Arguments",
        "description": (
            "## Function with Arguments\n\n"
            "Define a function named `add_numbers` that takes two parameters, `a` and `b`, "
            "and prints their sum. Then, call the function with the arguments `5` and `7`.\n\n"
            "**Expected output:**\n```\n12\n```"
        ),
        "hint": "Put the parameters inside the parentheses when defining the function: `def add_numbers(a, b):`. Then call it with `add_numbers(5, 7)`.",
        "difficulty_level": DifficultyLevel.beginner,
        "category_slug": "functions",
        "starter_code": "# Define add_numbers and call it with 5 and 7\n",
        "test_cases": [
            {"input_data": "", "expected_output": "12", "score_weight": 1.0, "is_hidden": False},
            {"input_data": "", "expected_output": "12", "score_weight": 1.0, "is_hidden": True},
        ],
    },
    {
        "title": "Return a Value",
        "description": (
            "## Return a Value\n\n"
            "Define a function named `get_square` that takes one parameter, `n`, and "
            "returns its square. Call the function with the argument `4` and print the returned value.\n\n"
            "**Expected output:**\n```\n16\n```"
        ),
        "hint": "Use the `return` keyword inside the function to send the value back. Then print the result of the function call.",
        "difficulty_level": DifficultyLevel.beginner,
        "category_slug": "functions",
        "starter_code": "# Define get_square, call it with 4, and print the result\n",
        "test_cases": [
            {"input_data": "", "expected_output": "16", "score_weight": 1.0, "is_hidden": False},
            {"input_data": "", "expected_output": "16", "score_weight": 1.0, "is_hidden": True},
        ],
    },
    {
        "title": "Append to a List",
        "description": (
            "## Append to a List\n\n"
            "A list `fruits` contains `[\"apple\", \"banana\"]`. Append `\"orange\"` to the list, "
            "then print the entire list.\n\n"
            "**Expected output:**\n```\n['apple', 'banana', 'orange']\n```"
        ),
        "hint": "Use the `.append()` method on the list to add a new item to the end.",
        "difficulty_level": DifficultyLevel.beginner,
        "category_slug": "lists",
        "starter_code": "fruits = [\"apple\", \"banana\"]\n# Append \"orange\" and print the list\n",
        "test_cases": [
            {"input_data": "", "expected_output": "['apple', 'banana', 'orange']", "score_weight": 1.0, "is_hidden": False},
            {"input_data": "", "expected_output": "['apple', 'banana', 'orange']", "score_weight": 1.0, "is_hidden": True},
        ],
    },
    {
        "title": "Maximum of Two Numbers",
        "description": (
            "## Maximum of Two Numbers\n\n"
            "Define a function named `maximum` that takes two parameters, `a` and `b`, and "
            "returns the larger of the two. Call it with `3` and `9` and print the returned value.\n\n"
            "**Expected output:**\n```\n9\n```"
        ),
        "hint": "Use an `if`/`else` inside the function to decide which value to return, or use the built-in `max()`.",
        "difficulty_level": DifficultyLevel.beginner,
        "category_slug": "functions",
        "starter_code": "# Define maximum, call it with 3 and 9, and print the result\n",
        "test_cases": [
            {"input_data": "", "expected_output": "9", "score_weight": 1.0, "is_hidden": False},
            {"input_data": "", "expected_output": "9", "score_weight": 1.0, "is_hidden": True},
        ],
    },
    {
        "title": "Default Parameter Value",
        "description": (
            "## Default Parameter Value\n\n"
            "Define a function named `power` that takes a `base` and an `exponent` that "
            "defaults to `2`. It should return `base` raised to `exponent`. Call it with just "
            "`power(5)` and print the result.\n\n"
            "**Expected output:**\n```\n25\n```"
        ),
        "hint": "Give a parameter a default by writing `exponent=2` in the function definition. Then `power(5)` uses the default.",
        "difficulty_level": DifficultyLevel.intermediate,
        "category_slug": "functions",
        "starter_code": "# Define power with a default exponent, then call power(5) and print the result\n",
        "test_cases": [
            {"input_data": "", "expected_output": "25", "score_weight": 1.0, "is_hidden": False},
            {"input_data": "", "expected_output": "25", "score_weight": 1.0, "is_hidden": True},
        ],
    },
    {
        "title": "Sum a List with a Function",
        "description": (
            "## Sum a List with a Function\n\n"
            "Define a function named `total` that takes one parameter, `numbers` (a list), and "
            "returns the sum of its values. Call it with `[1, 2, 3, 4]` and print the result.\n\n"
            "**Expected output:**\n```\n10\n```"
        ),
        "hint": "Inside the function, return `sum(numbers)`. Then print the result of calling the function.",
        "difficulty_level": DifficultyLevel.intermediate,
        "category_slug": "functions",
        "starter_code": "# Define total, call it with [1, 2, 3, 4], and print the result\n",
        "test_cases": [
            {"input_data": "", "expected_output": "10", "score_weight": 1.0, "is_hidden": False},
            {"input_data": "", "expected_output": "10", "score_weight": 1.0, "is_hidden": True},
        ],
    },
    {
        "title": "Recursive Factorial",
        "description": (
            "## Recursive Factorial\n\n"
            "Define a function named `factorial` that calculates a number's factorial by "
            "calling itself (recursion). The factorial of `0` or `1` is `1`. Call it with `5` "
            "and print the result.\n\n"
            "**Expected output:**\n```\n120\n```"
        ),
        "hint": "A recursive function calls itself with a smaller value. Base case: `n <= 1` returns `1`. Otherwise return `n * factorial(n - 1)`.",
        "difficulty_level": DifficultyLevel.intermediate,
        "category_slug": "functions",
        "starter_code": "# Define a recursive factorial, call it with 5, and print the result\n",
        "test_cases": [
            {"input_data": "", "expected_output": "120", "score_weight": 1.0, "is_hidden": False},
            {"input_data": "", "expected_output": "120", "score_weight": 1.0, "is_hidden": True},
        ],
    },
    {
        "title": "Sort a List",
        "description": (
            "## Sort a List\n\n"
            "A variable `numbers` holds `[5, 2, 8, 1, 9, 3]`. Print a new list with the values "
            "sorted in ascending order.\n\n"
            "**Expected output:**\n```\n[1, 2, 3, 5, 8, 9]\n```"
        ),
        "hint": "The built-in `sorted()` function returns a new sorted list without changing the original.",
        "difficulty_level": DifficultyLevel.beginner,
        "category_slug": "lists",
        "starter_code": "numbers = [5, 2, 8, 1, 9, 3]\n# Print the list sorted in ascending order\n",
        "test_cases": [
            {"input_data": "", "expected_output": "[1, 2, 3, 5, 8, 9]", "score_weight": 1.0, "is_hidden": False},
            {"input_data": "", "expected_output": "[1, 2, 3, 5, 8, 9]", "score_weight": 1.0, "is_hidden": True},
        ],
    },
    {
        "title": "Count Occurrences",
        "description": (
            "## Count Occurrences\n\n"
            "A variable `numbers` holds `[1, 2, 2, 3, 2, 4]`. Print how many times the value "
            "`2` appears in the list.\n\n"
            "**Expected output:**\n```\n3\n```"
        ),
        "hint": "Lists have a `.count()` method that returns how many times a value appears: `numbers.count(2)`.",
        "difficulty_level": DifficultyLevel.intermediate,
        "category_slug": "lists",
        "starter_code": "numbers = [1, 2, 2, 3, 2, 4]\n# Print how many times 2 appears\n",
        "test_cases": [
            {"input_data": "", "expected_output": "3", "score_weight": 1.0, "is_hidden": False},
            {"input_data": "", "expected_output": "3", "score_weight": 1.0, "is_hidden": True},
        ],
    },
    {
        "title": "Countdown with While",
        "description": (
            "## Countdown with While\n\n"
            "Use a `while` loop to count down from `5` to `1`, printing each number on its own "
            "line.\n\n"
            "**Expected output:**\n```\n5\n4\n3\n2\n1\n```"
        ),
        "hint": "Start a variable at 5. While it is greater than or equal to 1, print it and then subtract 1 with `n -= 1`.",
        "difficulty_level": DifficultyLevel.beginner,
        "category_slug": "loops",
        "starter_code": "# Use a while loop to count down from 5 to 1\n",
        "test_cases": [
            {"input_data": "", "expected_output": "5\n4\n3\n2\n1", "score_weight": 1.0, "is_hidden": False},
            {"input_data": "", "expected_output": "5\n4\n3\n2\n1", "score_weight": 1.0, "is_hidden": True},
        ],
    },
    {
        "title": "Sum of Even Numbers",
        "description": (
            "## Sum of Even Numbers\n\n"
            "Calculate and print the sum of all even numbers from 1 to 10 (inclusive).\n\n"
            "**Expected output:**\n```\n30\n```"
        ),
        "hint": "Loop through the numbers, and use `if n % 2 == 0:` to add only the even ones to a running total.",
        "difficulty_level": DifficultyLevel.intermediate,
        "category_slug": "loops",
        "starter_code": "# Print the sum of even numbers from 1 to 10\n",
        "test_cases": [
            {"input_data": "", "expected_output": "30", "score_weight": 1.0, "is_hidden": False},
            {"input_data": "", "expected_output": "30", "score_weight": 1.0, "is_hidden": True},
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
    "Define a Function": [
        {
            "kind": "nudge",
            "title": "Two steps",
            "body": "First you define the function, then you must call it for the code inside to run.",
        },
        {
            "kind": "pattern",
            "title": "Function definition",
            "body": "Use `def` to name the function, and indent the code that belongs inside it.",
            "code": "def my_function():\n    print(\"Inside!\")\n\nmy_function()",
        },
        {
            "kind": "checklist",
            "title": "Output check",
            "body": "Ensure the printed string matches exactly, including the exclamation mark.",
        },
    ],
    "Function with Arguments": [
        {
            "kind": "nudge",
            "title": "Pass values in",
            "body": "The function needs to accept variables in its definition, and you provide the actual numbers when calling it.",
        },
        {
            "kind": "pattern",
            "title": "Parameters",
            "body": "List the parameter names inside the parentheses.",
            "code": "def show_sum(x, y):\n    print(x + y)\n\nshow_sum(3, 4)",
        },
        {
            "kind": "checklist",
            "title": "Output check",
            "body": "Print only the final sum, which should be 12.",
        },
    ],
    "Return a Value": [
        {
            "kind": "nudge",
            "title": "Return, don't print inside",
            "body": "The function itself should hand the value back using `return`. The `print()` happens outside.",
        },
        {
            "kind": "pattern",
            "title": "Returning data",
            "body": "Use the `return` keyword to send a result back to the caller.",
            "code": "def double(x):\n    return x * 2\n\nresult = double(5)\nprint(result)",
        },
        {
            "kind": "checklist",
            "title": "Output check",
            "body": "Print the returned value, which should be 16.",
        },
    ],
    "Append to a List": [
        {
            "kind": "nudge",
            "title": "Modify in place",
            "body": "The `.append()` method changes the list directly. You don't need to assign the result to a new variable.",
        },
        {
            "kind": "pattern",
            "title": "List append",
            "body": "Call `.append()` on the list object with the new item in the parentheses.",
            "code": "my_list.append(\"new_item\")",
        },
        {
            "kind": "checklist",
            "title": "Output check",
            "body": "Print the entire list object, which will format with brackets and quotes.",
        },
    ],
    "Maximum of Two Numbers": [
        {
            "kind": "nudge",
            "title": "Compare, then return",
            "body": "The function should decide which of its two inputs is larger and hand that value back.",
        },
        {
            "kind": "pattern",
            "title": "Conditional return",
            "body": "You can return different values based on a comparison, or lean on the built-in `max()`.",
            "code": "def bigger(a, b):\n    if a > b:\n        return a\n    return b",
        },
        {
            "kind": "checklist",
            "title": "Output check",
            "body": "Print the value returned by the call, which should be 9.",
        },
    ],
    "Default Parameter Value": [
        {
            "kind": "nudge",
            "title": "Optional argument",
            "body": "A default lets the caller skip an argument. When omitted, the default value is used.",
        },
        {
            "kind": "pattern",
            "title": "Default in the signature",
            "body": "Assign the default right in the parameter list.",
            "code": "def scale(x, factor=2):\n    return x * factor\n\nprint(scale(5))",
        },
        {
            "kind": "checklist",
            "title": "Output check",
            "body": "Calling with one argument uses the default exponent, giving 25.",
        },
    ],
    "Sum a List with a Function": [
        {
            "kind": "nudge",
            "title": "Wrap the work in a function",
            "body": "The summing logic lives inside the function; the printing happens where you call it.",
        },
        {
            "kind": "pattern",
            "title": "Return a computed value",
            "body": "`sum()` totals the list, and `return` sends that total to the caller.",
            "code": "def total(numbers):\n    return sum(numbers)\n\nprint(total([1, 2, 3]))",
        },
        {
            "kind": "checklist",
            "title": "Output check",
            "body": "Print the returned total once, which should be 10.",
        },
    ],
    "Recursive Factorial": [
        {
            "kind": "nudge",
            "title": "Shrink the problem",
            "body": "A factorial of n is n times the factorial of n - 1. Keep reducing until you hit the base case.",
        },
        {
            "kind": "pattern",
            "title": "Base case plus recursion",
            "body": "Stop the recursion at 1, otherwise call the function again with a smaller number.",
            "code": "def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n - 1)",
        },
        {
            "kind": "checklist",
            "title": "Output check",
            "body": "Print the result of calling the function with 5, which should be 120.",
        },
    ],
    "Sort a List": [
        {
            "kind": "nudge",
            "title": "Let Python order it",
            "body": "You do not need to swap values by hand. A built-in returns a sorted copy.",
        },
        {
            "kind": "pattern",
            "title": "Sorted copy",
            "body": "`sorted()` returns a new list in ascending order and leaves the original untouched.",
            "code": "ordered = sorted(values)\nprint(ordered)",
        },
        {
            "kind": "checklist",
            "title": "Output check",
            "body": "Print the whole list with brackets, sorted smallest to largest.",
        },
    ],
    "Count Occurrences": [
        {
            "kind": "nudge",
            "title": "Ask the list",
            "body": "The list itself can report how many times a value shows up.",
        },
        {
            "kind": "pattern",
            "title": "Count method",
            "body": "`.count()` returns how many times the given value appears.",
            "code": "times = items.count(target)\nprint(times)",
        },
        {
            "kind": "checklist",
            "title": "Output check",
            "body": "Print the count number only, which should be 3.",
        },
    ],
    "Countdown with While": [
        {
            "kind": "nudge",
            "title": "Loop while a condition holds",
            "body": "A while loop keeps running until its condition becomes false, so update your counter each pass.",
        },
        {
            "kind": "pattern",
            "title": "Decrement inside the loop",
            "body": "Print first, then subtract so the loop eventually stops.",
            "code": "n = 5\nwhile n >= 1:\n    print(n)\n    n -= 1",
        },
        {
            "kind": "checklist",
            "title": "Output check",
            "body": "Five lines from 5 down to 1, one per line.",
        },
    ],
    "Sum of Even Numbers": [
        {
            "kind": "nudge",
            "title": "Add only the evens",
            "body": "Walk through the numbers and accumulate just the ones divisible by 2.",
        },
        {
            "kind": "pattern",
            "title": "Conditional accumulation",
            "body": "Use a running total and an `if` test inside the loop.",
            "code": "total = 0\nfor n in range(1, 11):\n    if n % 2 == 0:\n        total += n\nprint(total)",
        },
        {
            "kind": "checklist",
            "title": "Output check",
            "body": "Print the final total once, which should be 30.",
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
    "Define a Function": {
        "code": "def greet():\n    print(\"Hello from a function!\")\n\ngreet()",
        "explanation": "The function is defined with `def` and then called by its name followed by parentheses.",
    },
    "Function with Arguments": {
        "code": "def add_numbers(a, b):\n    print(a + b)\n\nadd_numbers(5, 7)",
        "explanation": "The function takes two parameters and prints their sum. It is then called with the arguments 5 and 7.",
    },
    "Return a Value": {
        "code": "def get_square(n):\n    return n ** 2\n\nprint(get_square(4))",
        "explanation": "The function calculates the square and uses `return` to pass it back. The caller then prints the returned value.",
    },
    "Append to a List": {
        "code": "fruits = [\"apple\", \"banana\"]\nfruits.append(\"orange\")\nprint(fruits)",
        "explanation": "The `.append()` method adds the new string to the end of the list, and then the updated list is printed.",
    },
    "Maximum of Two Numbers": {
        "code": "def maximum(a, b):\n    if a > b:\n        return a\n    return b\n\nprint(maximum(3, 9))",
        "explanation": "The function compares the two parameters and returns the larger one, which is then printed.",
    },
    "Default Parameter Value": {
        "code": "def power(base, exponent=2):\n    return base ** exponent\n\nprint(power(5))",
        "explanation": "Because `exponent` defaults to 2, calling `power(5)` squares the base to give 25.",
    },
    "Sum a List with a Function": {
        "code": "def total(numbers):\n    return sum(numbers)\n\nprint(total([1, 2, 3, 4]))",
        "explanation": "The function returns the sum of the list it receives, and the caller prints that total.",
    },
    "Recursive Factorial": {
        "code": "def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n - 1)\n\nprint(factorial(5))",
        "explanation": "The base case stops recursion at 1, and each call multiplies n by the factorial of n - 1.",
    },
    "Sort a List": {
        "code": "numbers = [5, 2, 8, 1, 9, 3]\nprint(sorted(numbers))",
        "explanation": "`sorted()` returns a new list arranged in ascending order.",
    },
    "Count Occurrences": {
        "code": "numbers = [1, 2, 2, 3, 2, 4]\nprint(numbers.count(2))",
        "explanation": "The `.count()` method reports how many times the value 2 appears in the list.",
    },
    "Countdown with While": {
        "code": "n = 5\nwhile n >= 1:\n    print(n)\n    n -= 1",
        "explanation": "The loop prints the current value, then decreases it until the condition fails at 0.",
    },
    "Sum of Even Numbers": {
        "code": "total = 0\nfor n in range(1, 11):\n    if n % 2 == 0:\n        total += n\nprint(total)",
        "explanation": "Only even numbers are added to the running total, producing 2 + 4 + 6 + 8 + 10 = 30.",
    },
}


RESOURCES = [
    {
        "title": "Variables & Data Types",
        "slug": "variables-and-data-types",
        "topic_area": "Basics",
        "difficulty_level": DifficultyLevel.beginner,
        "summary": "Learn how Python stores data in variables and explore the core built-in types: int, float, str, and bool.",
        "order": 1,
        "sections": [
            {
                "heading": "What is a Variable?",
                "body": "A variable is a named container that holds a value. In Python you create one by assigning a value to a name with the = operator. There is no need to declare a type first — Python figures it out automatically.",
                "code": "age = 25\nname = \"Alice\"\npi = 3.14159\nis_active = True\n\nprint(age, name, pi, is_active)",
                "output": "25 Alice 3.14159 True",
            },
            {
                "heading": "Core Data Types",
                "body": "Python has four primary scalar types:\n\n• int — whole numbers (42, -7, 0)\n• float — decimal numbers (3.14, -0.5)\n• str — text wrapped in quotes (\"hello\", 'world')\n• bool — either True or False\n\nUse the built-in type() function to inspect any value.",
                "code": "print(type(42))       # <class 'int'>\nprint(type(3.14))     # <class 'float'>\nprint(type(\"hello\"))  # <class 'str'>\nprint(type(True))     # <class 'bool'>",
                "output": "<class 'int'>\n<class 'float'>\n<class 'str'>\n<class 'bool'>",
            },
            {
                "heading": "Type Conversion",
                "body": "Python provides built-in functions to convert between types. This is useful when you need arithmetic on user input (which is always a string) or when you want a whole number from a float.",
                "code": "num = int(\"42\")\nprint(num + 8)       # 50\n\ntag = str(100)\nprint(\"Item \" + tag)  # Item 100\n\nprint(int(9.99))     # 9 — truncates, does not round",
                "output": "50\nItem 100\n9",
            },
            {
                "heading": "Naming Conventions",
                "body": "Variable names must start with a letter or underscore, can contain letters, digits, and underscores, and are case-sensitive. Python programmers conventionally use snake_case — lowercase words joined with underscores.",
                "code": "user_age = 30\nmax_score = 100\n_internal = True\n\n# These would cause errors:\n# 2cool = True       # starts with a digit\n# my-var = 5         # hyphens are not allowed\n# class = \"Python\"   # 'class' is a reserved keyword",
            },
        ],
    },
    {
        "title": "Strings & String Methods",
        "slug": "strings-and-string-methods",
        "topic_area": "Strings",
        "difficulty_level": DifficultyLevel.beginner,
        "summary": "Explore Python strings: creation, indexing, slicing, formatting with f-strings, and the most useful built-in string methods.",
        "order": 2,
        "sections": [
            {
                "heading": "Creating Strings",
                "body": "Strings are sequences of characters enclosed in single quotes, double quotes, or triple quotes. Triple-quoted strings can span multiple lines.",
                "code": "greeting = \"Hello, World!\"\npath = 'C:\\\\Users\\\\alice'\nmultiline = \"\"\"Line one\nLine two\nLine three\"\"\"\n\nprint(len(greeting))  # 13",
                "output": "13",
            },
            {
                "heading": "Indexing and Slicing",
                "body": "Individual characters are accessed with bracket notation. Indices start at 0. Negative indices count from the end. Slicing extracts a substring with [start:stop:step].",
                "code": "s = \"Python\"\nprint(s[0])     # P\nprint(s[-1])    # n\nprint(s[1:4])   # yth\nprint(s[::-1])  # nohtyP",
                "output": "P\nn\nyth\nnohtyP",
            },
            {
                "heading": "f-Strings",
                "body": "f-strings (formatted string literals) let you embed expressions directly inside a string by prefixing it with f and wrapping variables or expressions in {}.",
                "code": "name = \"Ada\"\nage = 36\nprint(f\"Hello, {name}! You are {age} years old.\")\nprint(f\"Next year you will be {age + 1}.\")",
                "output": "Hello, Ada! You are 36 years old.\nNext year you will be 37.",
            },
            {
                "heading": "Common String Methods",
                "body": "String methods return new strings without modifying the original. The most frequently used ones are shown below.",
                "code": "text = \"  Hello, World!  \"\nprint(text.strip())          # remove surrounding whitespace\nprint(text.lower())          # lowercase\nprint(text.upper())          # uppercase\nprint(text.replace(\"World\", \"Python\"))\nprint(\"a,b,c\".split(\",\"))    # ['a', 'b', 'c']\nprint(\"-\".join([\"a\", \"b\", \"c\"]))  # a-b-c",
                "output": "Hello, World!\n  hello, world!  \n  HELLO, WORLD!  \n  Hello, Python!  \n['a', 'b', 'c']\na-b-c",
            },
        ],
    },
    {
        "title": "Lists & List Operations",
        "slug": "lists-and-list-operations",
        "topic_area": "Lists",
        "difficulty_level": DifficultyLevel.beginner,
        "summary": "Master Python lists: creating, indexing, slicing, mutating, sorting, and the most useful list methods.",
        "order": 3,
        "sections": [
            {
                "heading": "Creating Lists",
                "body": "A list is an ordered, mutable collection of items. Items can be of any type and you can mix types in the same list. Create a list with square brackets.",
                "code": "fruits = [\"apple\", \"banana\", \"cherry\"]\nnumbers = [1, 2, 3, 4, 5]\nmixed = [42, \"hello\", True, 3.14]\nempty = []\n\nprint(len(fruits))  # 3",
                "output": "3",
            },
            {
                "heading": "Indexing and Slicing",
                "body": "Access elements by position. Negative indices count from the end. Slices return a new list.",
                "code": "items = [10, 20, 30, 40, 50]\nprint(items[0])    # 10\nprint(items[-1])   # 50\nprint(items[1:3])  # [20, 30]\nprint(items[::2])  # [10, 30, 50]",
                "output": "10\n50\n[20, 30]\n[10, 30, 50]",
            },
            {
                "heading": "Mutating a List",
                "body": "Lists are mutable — you can add, remove, and change elements in place.",
                "code": "fruits = [\"apple\", \"banana\"]\nfruits.append(\"cherry\")       # add to end\nfruits.insert(1, \"blueberry\") # insert at index 1\nfruits.remove(\"banana\")       # remove first match\npopped = fruits.pop()         # remove and return last\nprint(fruits)\nprint(popped)",
                "output": "['apple', 'blueberry', 'cherry']\ncherry",
            },
            {
                "heading": "Sorting and Searching",
                "body": "sorted() returns a new sorted list; list.sort() sorts in place. Use in to check membership and index() to find position.",
                "code": "nums = [3, 1, 4, 1, 5, 9, 2, 6]\nprint(sorted(nums))          # ascending copy\nprint(sorted(nums, reverse=True))  # descending copy\nprint(5 in nums)             # True\nprint(nums.index(4))         # 2\nprint(nums.count(1))         # 2",
                "output": "[1, 1, 2, 3, 4, 5, 6, 9]\n[9, 6, 5, 4, 3, 2, 1, 1]\nTrue\n2\n2",
            },
        ],
    },
    {
        "title": "Dictionaries",
        "slug": "dictionaries",
        "topic_area": "Data Structures",
        "difficulty_level": DifficultyLevel.beginner,
        "summary": "Learn Python dictionaries: creating key-value stores, reading and updating entries, and iterating over them.",
        "order": 4,
        "sections": [
            {
                "heading": "Creating Dictionaries",
                "body": "A dictionary maps keys to values. Keys must be immutable (strings, numbers, tuples). Values can be anything. Create one with curly braces and colons.",
                "code": "person = {\n    \"name\": \"Alice\",\n    \"age\": 30,\n    \"city\": \"London\",\n}\nprint(person[\"name\"])   # Alice\nprint(len(person))      # 3",
                "output": "Alice\n3",
            },
            {
                "heading": "Reading and Writing Entries",
                "body": "Access values with d[key]. Use .get() to supply a default when the key might be absent. Add or update entries with d[key] = value. Remove with del or .pop().",
                "code": "d = {\"x\": 10, \"y\": 20}\nprint(d.get(\"z\", 0))  # 0 — safe default\nd[\"z\"] = 30           # add new key\nd[\"x\"] = 99           # update existing\ndel d[\"y\"]\nprint(d)",
                "output": "0\n{'x': 99, 'z': 30}",
            },
            {
                "heading": "Iterating",
                "body": "Dictionaries expose three views: .keys(), .values(), and .items(). The .items() view is the most useful because it gives both key and value at once.",
                "code": "scores = {\"Alice\": 95, \"Bob\": 87, \"Carol\": 92}\nfor name, score in scores.items():\n    print(f\"{name}: {score}\")",
                "output": "Alice: 95\nBob: 87\nCarol: 92",
            },
            {
                "heading": "Useful Dict Methods",
                "body": "Key membership testing with in is O(1) — much faster than scanning a list. dict.update() merges another dict into the current one.",
                "code": "config = {\"debug\": True, \"port\": 8080}\noverrides = {\"port\": 9090, \"host\": \"localhost\"}\nconfig.update(overrides)\nprint(config)\nprint(\"debug\" in config)   # True\nprint(\"ssl\" in config)     # False",
                "output": "{'debug': True, 'port': 9090, 'host': 'localhost'}\nTrue\nFalse",
            },
        ],
    },
    {
        "title": "Tuples & Sets",
        "slug": "tuples-and-sets",
        "topic_area": "Data Structures",
        "difficulty_level": DifficultyLevel.beginner,
        "summary": "Understand Python tuples (immutable sequences) and sets (unordered collections of unique values), and when to use each.",
        "order": 5,
        "sections": [
            {
                "heading": "Tuples",
                "body": "A tuple is an immutable ordered sequence. Use parentheses (or no brackets at all). Because tuples cannot change, they are safe to use as dictionary keys and convey intent that data should not be modified.",
                "code": "point = (3, 7)\nrgb = (255, 128, 0)\nsingle = (42,)   # trailing comma makes it a tuple, not grouping\n\nx, y = point     # tuple unpacking\nprint(x, y)\nprint(point[0])",
                "output": "3 7\n3",
            },
            {
                "heading": "Sets",
                "body": "A set is an unordered collection of unique values. Duplicate entries are silently dropped. Sets support fast membership tests and set algebra (union, intersection, difference).",
                "code": "nums = {1, 2, 3, 2, 1}\nprint(nums)          # {1, 2, 3} — duplicates removed\nnums.add(4)\nnums.discard(2)\nprint(nums)\nprint(3 in nums)     # True",
                "output": "{1, 2, 3}\n{1, 3, 4}\nTrue",
            },
            {
                "heading": "Set Operations",
                "body": "Sets support mathematical set operations. These are especially useful for finding common elements or differences between two collections.",
                "code": "a = {1, 2, 3, 4}\nb = {3, 4, 5, 6}\n\nprint(a | b)   # union:        {1, 2, 3, 4, 5, 6}\nprint(a & b)   # intersection: {3, 4}\nprint(a - b)   # difference:   {1, 2}\nprint(a ^ b)   # symmetric diff: {1, 2, 5, 6}",
                "output": "{1, 2, 3, 4, 5, 6}\n{3, 4}\n{1, 2}\n{1, 2, 5, 6}",
            },
        ],
    },
    {
        "title": "Conditional Logic",
        "slug": "conditional-logic",
        "topic_area": "Control Flow",
        "difficulty_level": DifficultyLevel.beginner,
        "summary": "Control program flow using if, elif, and else statements, comparison operators, and logical operators.",
        "order": 6,
        "sections": [
            {
                "heading": "if / elif / else",
                "body": "Python executes only the block whose condition is True. Use elif to test multiple conditions in sequence and else as a fallback.",
                "code": "score = 72\n\nif score >= 90:\n    grade = \"A\"\nelif score >= 80:\n    grade = \"B\"\nelif score >= 70:\n    grade = \"C\"\nelse:\n    grade = \"F\"\n\nprint(grade)",
                "output": "C",
            },
            {
                "heading": "Comparison Operators",
                "body": "Comparisons return True or False. Python uses == for equality (not = which is assignment) and != for inequality. All six operators: ==, !=, <, >, <=, >=.",
                "code": "print(5 == 5)    # True\nprint(5 != 3)    # True\nprint(10 > 3)    # True\nprint(2 >= 2)    # True\nprint(\"abc\" < \"abd\")  # True — lexicographic",
                "output": "True\nTrue\nTrue\nTrue\nTrue",
            },
            {
                "heading": "Logical Operators",
                "body": "Combine conditions with and, or, and not. Python evaluates them lazily: and stops as soon as it finds a False, or stops as soon as it finds a True.",
                "code": "age = 25\nhas_ticket = True\n\nif age >= 18 and has_ticket:\n    print(\"Entry allowed\")\n\nif age < 13 or age > 65:\n    print(\"Discount applies\")\nelse:\n    print(\"Full price\")",
                "output": "Entry allowed\nFull price",
            },
            {
                "heading": "Truthiness",
                "body": "In Python, many values evaluate as False in a boolean context: 0, 0.0, empty string \"\", empty list [], empty dict {}, and None. Everything else is truthy. This lets you write concise guards.",
                "code": "items = []\nif not items:\n    print(\"List is empty\")\n\nname = \"Alice\"\nif name:\n    print(f\"Hello, {name}!\")",
                "output": "List is empty\nHello, Alice!",
            },
        ],
    },
    {
        "title": "Loops",
        "slug": "loops",
        "topic_area": "Control Flow",
        "difficulty_level": DifficultyLevel.beginner,
        "summary": "Repeat work efficiently using for loops over sequences and range(), while loops for condition-driven repetition, and flow control with break and continue.",
        "order": 7,
        "sections": [
            {
                "heading": "for Loops",
                "body": "A for loop iterates over any sequence — a list, string, range, or any iterable. The loop variable takes each value in turn.",
                "code": "fruits = [\"apple\", \"banana\", \"cherry\"]\nfor fruit in fruits:\n    print(fruit)\n\nfor i in range(1, 4):\n    print(i)",
                "output": "apple\nbanana\ncherry\n1\n2\n3",
            },
            {
                "heading": "while Loops",
                "body": "A while loop keeps running as long as its condition is True. You must update the condition inside the loop or you get an infinite loop.",
                "code": "count = 5\nwhile count > 0:\n    print(count)\n    count -= 1\nprint(\"Done\")",
                "output": "5\n4\n3\n2\n1\nDone",
            },
            {
                "heading": "break and continue",
                "body": "break exits the loop immediately. continue skips the rest of the current iteration and moves to the next one.",
                "code": "for n in range(1, 10):\n    if n == 5:\n        break          # stop at 5\n    if n % 2 == 0:\n        continue       # skip even numbers\n    print(n)",
                "output": "1\n3",
            },
            {
                "heading": "enumerate and zip",
                "body": "enumerate() pairs each item with its index, eliminating manual index tracking. zip() pairs items from two or more iterables together.",
                "code": "names = [\"Alice\", \"Bob\", \"Carol\"]\nfor i, name in enumerate(names, start=1):\n    print(f\"{i}. {name}\")\n\nscores = [95, 87, 92]\nfor name, score in zip(names, scores):\n    print(f\"{name}: {score}\")",
                "output": "1. Alice\n2. Bob\n3. Carol\nAlice: 95\nBob: 87\nCarol: 92",
            },
        ],
    },
    {
        "title": "Functions",
        "slug": "functions",
        "topic_area": "Functions",
        "difficulty_level": DifficultyLevel.beginner,
        "summary": "Write reusable blocks of code with def, pass arguments and defaults, and use return to send results back to the caller.",
        "order": 8,
        "sections": [
            {
                "heading": "Defining and Calling",
                "body": "Use def to define a function. The indented block is its body. A function only executes when called by its name followed by parentheses.",
                "code": "def greet():\n    print(\"Hello from a function!\")\n\ngreet()   # call it\ngreet()   # call it again",
                "output": "Hello from a function!\nHello from a function!",
            },
            {
                "heading": "Parameters and Arguments",
                "body": "Parameters are the names in the function definition. Arguments are the actual values you pass when calling the function.",
                "code": "def add(a, b):\n    print(a + b)\n\nadd(3, 7)    # 10\nadd(10, 20)  # 30",
                "output": "10\n30",
            },
            {
                "heading": "Return Values",
                "body": "Use return to send a value back to the caller. A function without an explicit return statement returns None.",
                "code": "def square(n):\n    return n ** 2\n\nresult = square(9)\nprint(result)           # 81\nprint(square(4) + 1)    # 17",
                "output": "81\n17",
            },
            {
                "heading": "Default and Keyword Arguments",
                "body": "Parameters can have default values, making them optional. You can also pass arguments by name (keyword arguments) to improve readability.",
                "code": "def power(base, exponent=2):\n    return base ** exponent\n\nprint(power(5))          # 25 — uses default\nprint(power(2, 10))      # 1024\nprint(power(exponent=3, base=4))  # 64 — keyword args",
                "output": "25\n1024\n64",
            },
        ],
    },
    {
        "title": "List & Dictionary Comprehensions",
        "slug": "list-and-dict-comprehensions",
        "topic_area": "Advanced Collections",
        "difficulty_level": DifficultyLevel.intermediate,
        "summary": "Write concise, expressive transformations over collections using list comprehensions, dict comprehensions, and set comprehensions.",
        "order": 9,
        "sections": [
            {
                "heading": "List Comprehensions",
                "body": "A list comprehension builds a new list by applying an expression to each item in an iterable, optionally filtering with a condition. It replaces a for loop + append pattern with a single readable line.",
                "code": "# Traditional approach\nsquares = []\nfor n in range(1, 6):\n    squares.append(n ** 2)\n\n# Comprehension\nsquares = [n ** 2 for n in range(1, 6)]\nprint(squares)",
                "output": "[1, 4, 9, 16, 25]",
            },
            {
                "heading": "Filtering with a Condition",
                "body": "Add an if clause to keep only items that satisfy a condition. The expression, loop, and filter are read left to right.",
                "code": "evens = [n for n in range(1, 11) if n % 2 == 0]\nprint(evens)\n\nlong_words = [w for w in [\"cat\", \"elephant\", \"ox\", \"giraffe\"] if len(w) > 3]\nprint(long_words)",
                "output": "[2, 4, 6, 8, 10]\n['elephant', 'giraffe']",
            },
            {
                "heading": "Dict Comprehensions",
                "body": "Dict comprehensions build dictionaries from iterables using {key_expr: value_expr for item in iterable}.",
                "code": "words = [\"apple\", \"banana\", \"cherry\"]\nlengths = {word: len(word) for word in words}\nprint(lengths)\n\nsquare_map = {n: n ** 2 for n in range(1, 6)}\nprint(square_map)",
                "output": "{'apple': 5, 'banana': 6, 'cherry': 6}\n{1: 1, 2: 4, 3: 9, 4: 16, 5: 25}",
            },
            {
                "heading": "Set Comprehensions",
                "body": "Set comprehensions use curly braces without colons. Duplicates are automatically removed — useful for extracting unique values.",
                "code": "text = \"hello world\"\nunique_chars = {ch for ch in text if ch != \" \"}\nprint(sorted(unique_chars))",
                "output": "['d', 'e', 'h', 'l', 'o', 'r', 'w']",
            },
        ],
    },
    {
        "title": "Error Handling",
        "slug": "error-handling",
        "topic_area": "Error Handling",
        "difficulty_level": DifficultyLevel.intermediate,
        "summary": "Catch and handle exceptions gracefully with try/except/else/finally, raise your own errors, and learn which exception types to use.",
        "order": 10,
        "sections": [
            {
                "heading": "try / except",
                "body": "Wrap code that might fail in a try block. If an exception occurs, Python jumps to the matching except block instead of crashing.",
                "code": "try:\n    result = 10 / 0\nexcept ZeroDivisionError:\n    print(\"Cannot divide by zero\")\n\ntry:\n    num = int(\"abc\")\nexcept ValueError as e:\n    print(f\"Error: {e}\")",
                "output": "Cannot divide by zero\nError: invalid literal for int() with base 10: 'abc'",
            },
            {
                "heading": "else and finally",
                "body": "The else block runs only if no exception was raised. The finally block always runs — useful for cleanup such as closing files or releasing resources.",
                "code": "try:\n    result = 10 / 2\nexcept ZeroDivisionError:\n    print(\"Division failed\")\nelse:\n    print(f\"Result: {result}\")\nfinally:\n    print(\"Always runs\")",
                "output": "Result: 5.0\nAlways runs",
            },
            {
                "heading": "Catching Multiple Exceptions",
                "body": "List multiple exception types in a tuple to handle them the same way. Use a bare except Exception as e to catch any exception and inspect it.",
                "code": "def safe_divide(a, b):\n    try:\n        return a / b\n    except (TypeError, ZeroDivisionError) as e:\n        print(f\"Caught: {e}\")\n        return None\n\nprint(safe_divide(10, 2))\nprint(safe_divide(10, 0))\nprint(safe_divide(10, \"x\"))",
                "output": "5.0\nCaught: division by zero\nNone\nCaught: unsupported operand type(s) for /: 'int' and 'str'\nNone",
            },
            {
                "heading": "Raising Exceptions",
                "body": "Use raise to signal that something went wrong. You can raise built-in exceptions or define your own by subclassing Exception.",
                "code": "def set_age(age):\n    if age < 0:\n        raise ValueError(f\"Age cannot be negative: {age}\")\n    return age\n\ntry:\n    set_age(-5)\nexcept ValueError as e:\n    print(e)",
                "output": "Age cannot be negative: -5",
            },
        ],
    },
    {
        "title": "File I/O",
        "slug": "file-io",
        "topic_area": "File Operations",
        "difficulty_level": DifficultyLevel.intermediate,
        "summary": "Read from and write to files using open(), context managers, and common patterns for working with text and CSV data.",
        "order": 11,
        "sections": [
            {
                "heading": "Opening and Reading Files",
                "body": "Use open() with a context manager (with statement) so the file is automatically closed even if an error occurs. Modes: 'r' = read (default), 'w' = write, 'a' = append.",
                "code": "# Write a sample file first\nwith open(\"notes.txt\", \"w\") as f:\n    f.write(\"Line one\\n\")\n    f.write(\"Line two\\n\")\n\n# Read the entire file at once\nwith open(\"notes.txt\") as f:\n    content = f.read()\nprint(content)",
                "output": "Line one\nLine two\n",
            },
            {
                "heading": "Reading Line by Line",
                "body": "Iterating over a file object yields one line at a time, including the trailing newline. Use .strip() to remove it. readlines() returns a list of all lines.",
                "code": "with open(\"notes.txt\") as f:\n    for line in f:\n        print(line.strip())\n\n# Or get a list\nwith open(\"notes.txt\") as f:\n    lines = f.readlines()\nprint(lines)",
                "output": "Line one\nLine two\n['Line one\\n', 'Line two\\n']",
            },
            {
                "heading": "Writing and Appending",
                "body": "Mode 'w' creates the file or overwrites it. Mode 'a' appends without erasing existing content. Use print(..., file=f) as an alternative to f.write().",
                "code": "with open(\"log.txt\", \"a\") as f:\n    f.write(\"New entry\\n\")\n\nwith open(\"log.txt\", \"w\") as f:\n    print(\"Hello\", file=f)\n    print(\"World\", file=f)",
            },
            {
                "heading": "Handling Missing Files",
                "body": "Opening a file that doesn't exist raises FileNotFoundError. Always check for this when reading user-specified paths.",
                "code": "try:\n    with open(\"missing.txt\") as f:\n        print(f.read())\nexcept FileNotFoundError:\n    print(\"File not found\")",
                "output": "File not found",
            },
        ],
    },
    {
        "title": "Classes & OOP",
        "slug": "classes-and-oop",
        "topic_area": "OOP",
        "difficulty_level": DifficultyLevel.intermediate,
        "summary": "Model real-world entities with classes, define behaviour with methods, share state with attributes, and understand inheritance.",
        "order": 12,
        "sections": [
            {
                "heading": "Defining a Class",
                "body": "__init__ is the constructor — it runs when you create an instance. self refers to the specific instance. Instance attributes are set on self.",
                "code": "class Dog:\n    def __init__(self, name, breed):\n        self.name = name\n        self.breed = breed\n\n    def bark(self):\n        print(f\"{self.name} says: Woof!\")\n\nfido = Dog(\"Fido\", \"Labrador\")\nfido.bark()\nprint(fido.name)",
                "output": "Fido says: Woof!\nFido",
            },
            {
                "heading": "Class vs Instance Attributes",
                "body": "Class attributes are shared by all instances. Instance attributes (set on self) are unique to each object.",
                "code": "class Counter:\n    count = 0   # class attribute\n\n    def __init__(self, name):\n        self.name = name       # instance attribute\n        Counter.count += 1\n\na = Counter(\"a\")\nb = Counter(\"b\")\nprint(Counter.count)   # 2 — shared",
                "output": "2",
            },
            {
                "heading": "Inheritance",
                "body": "A subclass inherits all methods and attributes from the parent class. Use super() to call the parent's __init__ or any overridden method.",
                "code": "class Animal:\n    def __init__(self, name):\n        self.name = name\n\n    def speak(self):\n        return \"...\"\n\nclass Cat(Animal):\n    def speak(self):\n        return f\"{self.name} says: Meow!\"\n\nclass Duck(Animal):\n    def speak(self):\n        return f\"{self.name} says: Quack!\"\n\nfor animal in [Cat(\"Whiskers\"), Duck(\"Donald\")]:\n    print(animal.speak())",
                "output": "Whiskers says: Meow!\nDonald says: Quack!",
            },
            {
                "heading": "Special Methods (Dunder Methods)",
                "body": "Double-underscore methods let you define how your objects behave with Python operators and built-ins. __str__ controls what print() shows. __len__ enables len(). __eq__ enables == comparison.",
                "code": "class Point:\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n\n    def __str__(self):\n        return f\"Point({self.x}, {self.y})\"\n\n    def __add__(self, other):\n        return Point(self.x + other.x, self.y + other.y)\n\np1 = Point(1, 2)\np2 = Point(3, 4)\nprint(p1 + p2)",
                "output": "Point(4, 6)",
            },
        ],
    },
    {
        "title": "Modules & Imports",
        "slug": "modules-and-imports",
        "topic_area": "Modules",
        "difficulty_level": DifficultyLevel.intermediate,
        "summary": "Organise code across files with Python's module system, import from the standard library, and understand packages.",
        "order": 13,
        "sections": [
            {
                "heading": "Importing Modules",
                "body": "A module is any Python file. Import it with import or grab specific names with from ... import. The standard library ships hundreds of useful modules.",
                "code": "import math\nprint(math.sqrt(144))    # 12.0\nprint(math.pi)           # 3.141592...\n\nfrom math import factorial\nprint(factorial(5))       # 120",
                "output": "12.0\n3.141592653589793\n120",
            },
            {
                "heading": "Useful Standard Library Modules",
                "body": "Python's standard library covers a vast range of tasks. Here are the most commonly used modules you should know.",
                "code": "import random\nimport datetime\nimport os\nimport json\n\nprint(random.randint(1, 10))       # random integer\nprint(datetime.date.today())        # today's date\nprint(os.getcwd())                  # current directory\n\ndata = {\"key\": \"value\"}\nprint(json.dumps(data))            # serialize to JSON string",
            },
            {
                "heading": "Creating Your Own Module",
                "body": "Any .py file is a module. Place it in the same directory and import it by filename (without .py). The if __name__ == '__main__': guard lets a file run standalone OR be imported without executing its script-level code.",
                "code": "# mathutils.py\ndef double(n):\n    return n * 2\n\nif __name__ == \"__main__\":\n    print(double(5))   # only runs when executed directly\n\n# main.py\n# import mathutils\n# print(mathutils.double(7))   # 14",
            },
            {
                "heading": "Packages",
                "body": "A package is a directory containing an __init__.py file and one or more module files. Python will treat it as a namespace, allowing hierarchical imports like from mypackage.utils import helper.",
                "code": "# Directory structure:\n# mypackage/\n#   __init__.py\n#   utils.py\n#   models.py\n\n# Import from a package:\n# from mypackage.utils import some_function",
            },
        ],
    },
    {
        "title": "Slicing & Unpacking",
        "slug": "slicing-and-unpacking",
        "topic_area": "Data Manipulation",
        "difficulty_level": DifficultyLevel.intermediate,
        "summary": "Master Python's powerful slice syntax, starred unpacking, and tuple unpacking to work with sequences concisely.",
        "order": 14,
        "sections": [
            {
                "heading": "Slice Syntax",
                "body": "Slices take the form [start:stop:step]. Omitting start defaults to 0, omitting stop defaults to the end, and step defaults to 1. Negative step reverses direction.",
                "code": "s = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]\nprint(s[2:5])    # [2, 3, 4]\nprint(s[:3])     # [0, 1, 2]\nprint(s[7:])     # [7, 8, 9]\nprint(s[::2])    # [0, 2, 4, 6, 8]\nprint(s[::-1])   # reversed",
                "output": "[2, 3, 4]\n[0, 1, 2]\n[7, 8, 9]\n[0, 2, 4, 6, 8]\n[9, 8, 7, 6, 5, 4, 3, 2, 1, 0]",
            },
            {
                "heading": "Tuple Unpacking",
                "body": "Any iterable on the right side of an assignment can be unpacked into multiple variables on the left side. The number of variables must match the number of items.",
                "code": "x, y, z = (1, 2, 3)\nprint(x, y, z)\n\nfirst, second = \"hi\"\nprint(first, second)\n\na, b = b, a  # swap without temp variable (a=2, b=1 after)\nprint(a, b)",
                "output": "1 2 3\nh i\n2 1",
            },
            {
                "heading": "Starred Unpacking",
                "body": "The * prefix in an assignment collects the remaining items into a list. It can appear at the start, middle, or end.",
                "code": "first, *rest = [1, 2, 3, 4, 5]\nprint(first)   # 1\nprint(rest)    # [2, 3, 4, 5]\n\n*head, last = [10, 20, 30]\nprint(head)    # [10, 20]\nprint(last)    # 30",
                "output": "1\n[2, 3, 4, 5]\n[10, 20]\n30",
            },
            {
                "heading": "Unpacking in Loops and Function Calls",
                "body": "Unpacking works inside for loops (e.g. for k, v in d.items()) and when spreading iterables into function arguments with * (spread) and ** (dict spread).",
                "code": "pairs = [(\"a\", 1), (\"b\", 2), (\"c\", 3)]\nfor letter, number in pairs:\n    print(letter, number)\n\ndef add(x, y):\n    return x + y\n\nargs = [3, 7]\nprint(add(*args))",
                "output": "a 1\nb 2\nc 3\n10",
            },
        ],
    },
    {
        "title": "Lambda & Higher-Order Functions",
        "slug": "lambda-and-higher-order-functions",
        "topic_area": "Functional Python",
        "difficulty_level": DifficultyLevel.intermediate,
        "summary": "Write concise anonymous functions with lambda, and use map(), filter(), and sorted() with key functions for expressive data pipelines.",
        "order": 15,
        "sections": [
            {
                "heading": "Lambda Functions",
                "body": "A lambda is a short, anonymous function written as a single expression. It is most useful when you need a throwaway function to pass to another function.",
                "code": "square = lambda n: n ** 2\nprint(square(5))   # 25\n\nadd = lambda a, b: a + b\nprint(add(3, 4))   # 7",
                "output": "25\n7",
            },
            {
                "heading": "sorted() with key=",
                "body": "The key parameter of sorted() (and list.sort()) accepts a function that is called on each item to produce its sort key. Lambda makes this concise.",
                "code": "words = [\"banana\", \"apple\", \"cherry\", \"fig\"]\nprint(sorted(words))                  # alphabetical\nprint(sorted(words, key=len))         # by length\nprint(sorted(words, key=lambda w: w[-1]))  # by last char",
                "output": "['apple', 'banana', 'cherry', 'fig']\n['fig', 'apple', 'banana', 'cherry']\n['banana', 'apple', 'fig', 'cherry']",
            },
            {
                "heading": "map() and filter()",
                "body": "map(fn, iterable) applies a function to every item, returning a lazy iterator. filter(fn, iterable) keeps only items for which fn returns True. Wrap with list() to materialise.",
                "code": "nums = [1, 2, 3, 4, 5]\nsquared = list(map(lambda n: n ** 2, nums))\nprint(squared)\n\nevens = list(filter(lambda n: n % 2 == 0, nums))\nprint(evens)",
                "output": "[1, 4, 9, 16, 25]\n[2, 4]",
            },
            {
                "heading": "Functions as First-Class Objects",
                "body": "In Python, functions are objects. You can pass them as arguments, return them from other functions, and store them in variables or data structures. This is the foundation of higher-order programming.",
                "code": "def apply(fn, values):\n    return [fn(v) for v in values]\n\ndef double(n):\n    return n * 2\n\nprint(apply(double, [1, 2, 3, 4]))\nprint(apply(str, [10, 20, 30]))",
                "output": "[2, 4, 6, 8]\n['10', '20', '30']",
            },
        ],
    },
    {
        "title": "Generators & Iterators",
        "slug": "generators-and-iterators",
        "topic_area": "Iterators",
        "difficulty_level": DifficultyLevel.intermediate,
        "summary": "Produce values lazily with generator functions and expressions to avoid materialising large sequences in memory.",
        "order": 16,
        "sections": [
            {
                "heading": "The Iterator Protocol",
                "body": "Any object with __iter__ and __next__ methods is an iterator. Calling next() on it yields the next value. StopIteration signals the end. For loops use this protocol internally.",
                "code": "nums = iter([10, 20, 30])\nprint(next(nums))   # 10\nprint(next(nums))   # 20\nprint(next(nums))   # 30\n# next(nums) would raise StopIteration",
                "output": "10\n20\n30",
            },
            {
                "heading": "Generator Functions",
                "body": "Replace return with yield to turn a function into a generator. Each call to next() resumes execution until the next yield. The function's local state is preserved between calls.",
                "code": "def count_up(start, stop):\n    current = start\n    while current <= stop:\n        yield current\n        current += 1\n\nfor n in count_up(1, 5):\n    print(n)",
                "output": "1\n2\n3\n4\n5",
            },
            {
                "heading": "Generator Expressions",
                "body": "Generator expressions look like list comprehensions but use parentheses instead of brackets. They are lazy — values are computed on demand, saving memory.",
                "code": "# List comprehension — builds entire list in memory\nall_squares = [n ** 2 for n in range(1_000_000)]\n\n# Generator expression — computes one value at a time\ngen_squares = (n ** 2 for n in range(1_000_000))\n\n# Take only what you need\nprint(next(gen_squares))   # 0\nprint(next(gen_squares))   # 1",
                "output": "0\n1",
            },
            {
                "heading": "Practical Use: Large Files",
                "body": "Generators shine when processing data that doesn't fit in memory. Iterating a file object line by line is itself a generator pattern — only one line is in memory at a time.",
                "code": "def read_large_file(path):\n    with open(path) as f:\n        for line in f:         # lazy: one line at a time\n            yield line.strip()\n\n# Usage:\n# for line in read_large_file(\"huge.log\"):\n#     process(line)",
            },
        ],
    },
    {
        "title": "Decorators",
        "slug": "decorators",
        "topic_area": "Advanced Functions",
        "difficulty_level": DifficultyLevel.intermediate,
        "summary": "Extend or modify function behaviour without changing its source using Python's decorator syntax and the functools.wraps helper.",
        "order": 17,
        "sections": [
            {
                "heading": "Functions Returning Functions",
                "body": "A decorator is just a function that takes a function and returns a new function. Understanding closures is the key: the inner function 'closes over' the original function.",
                "code": "def shout(fn):\n    def wrapper(*args, **kwargs):\n        result = fn(*args, **kwargs)\n        return str(result).upper()\n    return wrapper\n\ndef greet(name):\n    return f\"hello, {name}\"\n\nlouder = shout(greet)\nprint(louder(\"alice\"))",
                "output": "HELLO, ALICE",
            },
            {
                "heading": "The @ Syntax",
                "body": "The @ symbol is syntactic sugar for applying a decorator. @decorator placed above a function definition is equivalent to fn = decorator(fn).",
                "code": "from functools import wraps\n\ndef log_calls(fn):\n    @wraps(fn)   # preserves fn.__name__ and __doc__\n    def wrapper(*args, **kwargs):\n        print(f\"Calling {fn.__name__}\")\n        return fn(*args, **kwargs)\n    return wrapper\n\n@log_calls\ndef add(a, b):\n    return a + b\n\nresult = add(3, 4)\nprint(result)",
                "output": "Calling add\n7",
            },
            {
                "heading": "Decorators with Arguments",
                "body": "To pass arguments to a decorator, add another wrapper layer. The outermost function takes the decorator arguments and returns the actual decorator.",
                "code": "def repeat(times):\n    def decorator(fn):\n        @wraps(fn)\n        def wrapper(*args, **kwargs):\n            for _ in range(times):\n                fn(*args, **kwargs)\n        return wrapper\n    return decorator\n\n@repeat(3)\ndef hello():\n    print(\"Hello!\")\n\nhello()",
                "output": "Hello!\nHello!\nHello!",
            },
            {
                "heading": "Common Built-in Decorators",
                "body": "Python ships several useful decorators in the standard library. @staticmethod and @classmethod modify method binding in classes. @property turns a method into a computed attribute. @functools.cache memoizes expensive function calls.",
                "code": "class Circle:\n    def __init__(self, radius):\n        self.radius = radius\n\n    @property\n    def area(self):\n        import math\n        return math.pi * self.radius ** 2\n\nc = Circle(5)\nprint(f\"{c.area:.2f}\")   # access like attribute, no ()",
                "output": "78.54",
            },
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

        # Upsert resources
        for res_data in RESOURCES:
            result = await db.execute(select(Resource).where(Resource.slug == res_data["slug"]))
            existing = result.scalar_one_or_none()
            if existing:
                existing.title = res_data["title"]
                existing.summary = res_data["summary"]
                existing.sections = res_data["sections"]
                existing.order = res_data["order"]
                print(f"  Updated resource: {res_data['title']}")
            else:
                db.add(Resource(**res_data))
                print(f"  Created resource: {res_data['title']}")

        await db.commit()
        print("\nSeeding complete.")


if __name__ == "__main__":
    asyncio.run(seed())
