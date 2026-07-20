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

    # -----------------------------------------
    # Python booleans -> JSON booleans
    # -----------------------------------------

    text = re.sub(r"\bTrue\b", "true", text)
    text = re.sub(r"\bFalse\b", "false", text)

    # -----------------------------------------
    # Python None -> JSON null
    # -----------------------------------------

    text = re.sub(r"\bNone\b", "null", text)

    # -----------------------------------------
    # Replace ALL single-quoted strings
    #
    # Example:
    # 'result'      -> "result"
    # 'addition'    -> "addition"
    #
    # This also fixes nested dictionaries.
    # -----------------------------------------

    text = re.sub(
        r"'([^']*)'",
        r'"\1"',
        text,
    )

    return text