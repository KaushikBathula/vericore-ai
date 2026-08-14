"""
JSON Repair Utility.

Repairs common LLM-generated JSON formatting issues before
parsing with json.loads().
"""

from __future__ import annotations

import re


def repair_json(text: str) -> str:
    """
    Repair common JSON formatting mistakes produced by LLMs.

    Parameters
    ----------
    text:
        Raw LLM response.

    Returns
    -------
    str
        JSON string with common formatting issues corrected.
    """

    text = text.strip()

    # --------------------------------------------------
    # Remove markdown JSON fences
    # --------------------------------------------------

    text = re.sub(
        r"^```(?:json)?\s*",
        "",
        text,
        flags=re.IGNORECASE,
    )

    text = re.sub(
        r"\s*```$",
        "",
        text,
    )

    text = text.strip()

    # --------------------------------------------------
    # Extract the JSON object
    #
    # This prevents explanatory text before/after JSON
    # from breaking json.loads().
    # --------------------------------------------------

    start = text.find("{")
    end = text.rfind("}")

    if start != -1 and end != -1 and end > start:
        text = text[start:end + 1]

    # --------------------------------------------------
    # Python booleans -> JSON booleans
    # --------------------------------------------------

    text = re.sub(r"\bTrue\b", "true", text)
    text = re.sub(r"\bFalse\b", "false", text)

    # --------------------------------------------------
    # Python None -> JSON null
    # --------------------------------------------------

    text = re.sub(r"\bNone\b", "null", text)

    # --------------------------------------------------
    # Remove trailing commas
    #
    # Example:
    # {
    #   "A": 1,
    # }
    #
    # becomes:
    #
    # {
    #   "A": 1
    # }
    # --------------------------------------------------

    text = re.sub(
        r",\s*([}\]])",
        r"\1",
        text,
    )

    # --------------------------------------------------
    # Replace simple single-quoted strings
    #
    # Example:
    # 'result' -> "result"
    # --------------------------------------------------

    text = re.sub(
        r"'([^'\\]*(?:\\.[^'\\]*)*)'",
        r'"\1"',
        text,
    )

    # --------------------------------------------------
    # Fix missing commas between JSON objects/arrays
    #
    # Example:
    #
    # {
    #   "A": 1
    #   "B": 2
    # }
    #
    # becomes:
    #
    # {
    #   "A": 1,
    #   "B": 2
    # }
    #
    # Also handles:
    #
    # }
    # {
    #
    # and
    #
    # ]
    # {
    # --------------------------------------------------

    text = re.sub(
        r'([}\]])\s*(["])',
        r'\1,\2',
        text,
    )

    # --------------------------------------------------
    # Fix missing comma between primitive values
    #
    # Example:
    #
    # "A": 1
    # "B": 2
    #
    # becomes:
    #
    # "A": 1,
    # "B": 2
    # --------------------------------------------------

    text = re.sub(
        r'([0-9])\s*(")',
        r'\1,\2',
        text,
    )

    text = re.sub(
        r'(true|false|null)\s*(")',
        r'\1,\2',
        text,
    )

    # --------------------------------------------------
    # Fix missing commas after quoted string values
    #
    # Example:
    #
    # "A": "foo"
    # "B": "bar"
    # --------------------------------------------------

    text = re.sub(
        r'("\s*)\n(\s*")',
        r'\1,\n\2',
        text,
    )

    return text.strip()