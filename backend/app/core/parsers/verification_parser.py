"""
Verification response parser.

Converts raw LLM verification responses into a validated
VerificationPlan while tolerating common LLM formatting errors.
"""

from __future__ import annotations

import json
import logging
import re
from typing import Any

from pydantic import ValidationError

from backend.app.core.parsers.response_parser import ResponseParser
from backend.app.schemas.verification_plan import VerificationPlan
from backend.app.utils.json_repair import repair_json


logger = logging.getLogger(__name__)


class VerificationParser:
    """
    Converts raw LLM verification responses into a validated
    VerificationPlan.

    The parser is deliberately tolerant of common LLM output
    problems such as:

    - Markdown code fences
    - Leading/trailing explanatory text
    - 0b binary literals
    - Single quotes
    - Trailing commas
    - Partially malformed JSON
    - Missing optional fields
    """

    @staticmethod
    def parse(response: str) -> VerificationPlan:
        """
        Parse and normalize an LLM verification response.
        """

        if not response or not response.strip():
            raise ValueError(
                "Verification LLM returned an empty response."
            )

        logger.info(
            "Parsing verification response."
        )

        cleaned = VerificationParser._clean_response(
            response
        )

        data = VerificationParser._parse_json(
            cleaned
        )

        if not isinstance(data, dict):
            raise ValueError(
                "Verification response must contain a JSON object."
            )

        # ---------------------------------------------------------
        # Normalize top-level collections
        # ---------------------------------------------------------

        data.setdefault("test_cases", [])
        data.setdefault("test_vectors", [])
        data.setdefault("assertions", [])
        data.setdefault("coverage_points", [])

        # ---------------------------------------------------------
        # Normalize test cases
        # ---------------------------------------------------------

        data["test_cases"] = (
            VerificationParser._normalize_test_cases(
                data.get("test_cases", [])
            )
        )

        # ---------------------------------------------------------
        # Normalize test vectors
        # ---------------------------------------------------------

        data["test_vectors"] = (
            VerificationParser._normalize_test_vectors(
                data.get("test_vectors", [])
            )
        )

        # ---------------------------------------------------------
        # Generate vectors from test cases if necessary
        # ---------------------------------------------------------

        if (
            not data["test_vectors"]
            and data["test_cases"]
        ):
            data["test_vectors"] = (
                VerificationParser._vectors_from_test_cases(
                    data["test_cases"]
                )
            )

        # ---------------------------------------------------------
        # Normalize assertions
        # ---------------------------------------------------------

        data["assertions"] = (
            VerificationParser._normalize_string_list(
                data.get("assertions", [])
            )
        )

        # ---------------------------------------------------------
        # Normalize coverage
        # ---------------------------------------------------------

        data["coverage_points"] = (
            VerificationParser._normalize_string_list(
                data.get("coverage_points", [])
            )
        )

        # ---------------------------------------------------------
        # Validate final schema
        # ---------------------------------------------------------

        try:
            plan = VerificationPlan.model_validate(
                data
            )

        except ValidationError as exc:

            logger.error(
                "Verification plan validation failed: %s",
                exc,
            )

            raise ValueError(
                f"Verification validation failed:\n{exc}"
            ) from exc

        logger.info(
            "Verification response parsed successfully."
        )

        return plan

    # =============================================================
    # RESPONSE CLEANING
    # =============================================================

    @staticmethod
    def _clean_response(
        response: str,
    ) -> str:
        """
        Remove common LLM formatting noise.
        """

        cleaned = response.strip()

        # Remove markdown fences.
        cleaned = ResponseParser._strip_markdown(
            cleaned
        ).strip()

        # Remove common 0b binary literals.
        cleaned = re.sub(
            r"\b0b([01]+)\b",
            lambda match: str(
                int(match.group(1), 2)
            ),
            cleaned,
        )

        # First attempt at project JSON repair.
        try:
            repaired = repair_json(
                cleaned
            )

            if repaired:
                cleaned = repaired.strip()

        except Exception as exc:
            logger.warning(
                "JSON repair utility failed: %s",
                exc,
            )

        return cleaned

    # =============================================================
    # JSON PARSING
    # =============================================================

    @staticmethod
    def _parse_json(
        response: str,
    ) -> dict[str, Any]:
        """
        Parse JSON with several progressively more tolerant
        recovery strategies.
        """

        # ---------------------------------------------------------
        # Attempt 1: direct JSON
        # ---------------------------------------------------------

        try:
            return json.loads(response)

        except json.JSONDecodeError:
            pass

        # ---------------------------------------------------------
        # Attempt 2: extract JSON object from surrounding text
        # ---------------------------------------------------------

        extracted = (
            VerificationParser._extract_json_object(
                response
            )
        )

        if extracted is not None:

            try:
                return json.loads(
                    extracted
                )

            except json.JSONDecodeError:
                pass

        # ---------------------------------------------------------
        # Attempt 3: repair extracted JSON
        # ---------------------------------------------------------

        if extracted is not None:

            try:
                repaired = repair_json(
                    extracted
                )

                return json.loads(
                    repaired
                )

            except Exception:
                pass

        # ---------------------------------------------------------
        # Attempt 4: tolerant quote/trailing-comma repair
        # ---------------------------------------------------------

        tolerant = (
            VerificationParser._tolerant_json_cleanup(
                response
            )
        )

        try:
            return json.loads(
                tolerant
            )

        except json.JSONDecodeError as exc:

            logger.error(
                "Unable to parse verification JSON."
            )

            print(
                "\n========== INVALID VERIFICATION JSON ==========\n"
            )
            print(response[:2000])
            print(
                "\n========== END INVALID RESPONSE PREVIEW ========\n"
            )

            print(
                f"JSON error at line {exc.lineno}, "
                f"column {exc.colno}, "
                f"character {exc.pos}"
            )

            raise ValueError(
                "Verification LLM returned invalid JSON."
            ) from exc

    # =============================================================
    # JSON OBJECT EXTRACTION
    # =============================================================

    @staticmethod
    def _extract_json_object(
        response: str,
    ) -> str | None:
        """
        Extract the outermost JSON object from a response
        containing explanatory text around it.
        """

        start = response.find("{")

        if start < 0:
            return None

        depth = 0
        in_string = False
        escaped = False

        for index in range(
            start,
            len(response),
        ):

            char = response[index]

            if escaped:
                escaped = False
                continue

            if char == "\\":
                escaped = True
                continue

            if char == '"':
                in_string = not in_string
                continue

            if in_string:
                continue

            if char == "{":
                depth += 1

            elif char == "}":
                depth -= 1

                if depth == 0:
                    return response[
                        start:index + 1
                    ]

        return None

    # =============================================================
    # TOLERANT JSON CLEANUP
    # =============================================================

    @staticmethod
    def _tolerant_json_cleanup(
        response: str,
    ) -> str:
        """
        Apply conservative JSON cleanup.

        This intentionally avoids aggressive transformations
        that could corrupt valid string values.
        """

        cleaned = response.strip()

        # Extract object if surrounded by prose.
        extracted = (
            VerificationParser._extract_json_object(
                cleaned
            )
        )

        if extracted is not None:
            cleaned = extracted

        # Remove trailing commas before } or ].
        cleaned = re.sub(
            r",\s*([}\]])",
            r"\1",
            cleaned,
        )

        # Convert common Python boolean/null literals.
        cleaned = re.sub(
            r"\bTrue\b",
            "true",
            cleaned,
        )

        cleaned = re.sub(
            r"\bFalse\b",
            "false",
            cleaned,
        )

        cleaned = re.sub(
            r"\bNone\b",
            "null",
            cleaned,
        )

        # Convert simple single-quoted JSON keys/values.
        #
        # This is intentionally conservative.
        cleaned = re.sub(
            r"'([^'\\]*(?:\\.[^'\\]*)*)'",
            lambda match: json.dumps(
                match.group(1)
            ),
            cleaned,
        )

        return cleaned

    # =============================================================
    # TEST CASE NORMALIZATION
    # =============================================================

    @staticmethod
    def _normalize_test_cases(
        test_cases: Any,
    ) -> list[dict[str, str]]:
        """
        Normalize LLM test-case representations.
        """

        if not isinstance(
            test_cases,
            list,
        ):
            return []

        normalized: list[
            dict[str, str]
        ] = []

        for index, test_case in enumerate(
            test_cases
        ):

            if isinstance(
                test_case,
                str,
            ):

                normalized.append(
                    {
                        "name": test_case,
                        "description": test_case,
                        "stimulus": "",
                        "expected_result": "",
                    }
                )

                continue

            if not isinstance(
                test_case,
                dict,
            ):
                continue

            stimulus = (
                test_case.get("stimulus")
                or test_case.get("inputs")
                or test_case.get("input")
                or test_case.get("test_input")
                or ""
            )

            expected = (
                test_case.get(
                    "expected_result"
                )
                or test_case.get(
                    "expected_output"
                )
                or test_case.get(
                    "expected_outputs"
                )
                or test_case.get(
                    "expected"
                )
                or ""
            )

            normalized.append(
                {
                    "name": str(
                        test_case.get(
                            "name",
                            f"Test {index + 1}",
                        )
                    ),
                    "description": str(
                        test_case.get(
                            "description",
                            "",
                        )
                    ),
                    "stimulus": str(
                        stimulus
                    ),
                    "expected_result": str(
                        expected
                    ),
                }
            )

        return normalized

    # =============================================================
    # TEST VECTOR NORMALIZATION
    # =============================================================

    @staticmethod
    def _normalize_test_vectors(
        vectors: Any,
    ) -> list[dict[str, Any]]:
        """
        Normalize LLM-generated test vectors.
        """

        if not isinstance(
            vectors,
            list,
        ):
            return []

        normalized: list[
            dict[str, Any]
        ] = []

        for vector in vectors:

            if not isinstance(
                vector,
                dict,
            ):
                continue

            inputs = vector.get(
                "inputs"
            )

            expected = vector.get(
                "expected_outputs"
            )

            # -----------------------------------------------------
            # Support flat AI output.
            # -----------------------------------------------------

            if (
                inputs is None
                and expected is None
            ):

                inputs = {}
                expected = {}

                for key, value in vector.items():

                    upper = str(
                        key
                    ).upper()

                    if upper in {
                        "A",
                        "B",
                        "CLK",
                        "RST",
                        "RESET",
                        "ENABLE",
                    }:

                        inputs[key] = value

                    elif upper in {
                        "SUM",
                        "CARRY",
                        "OUT",
                        "Y",
                        "Q",
                        "GT",
                        "LT",
                        "EQ",
                    }:

                        expected[key] = value

            else:

                inputs = (
                    inputs
                    or vector.get(
                        "stimulus"
                    )
                    or {}
                )

                expected = (
                    expected
                    or vector.get(
                        "expected_result"
                    )
                    or vector.get(
                        "expected"
                    )
                    or {}
                )

            if not isinstance(
                inputs,
                dict,
            ):
                inputs = {}

            if not isinstance(
                expected,
                dict,
            ):
                expected = {}

            inputs = {
                key: value
                for key, value in inputs.items()
                if value is not None
            }

            expected = {
                key: value
                for key, value in expected.items()
                if value is not None
            }

            try:
                delay = int(
                    vector.get(
                        "delay",
                        10,
                    )
                )

            except (
                TypeError,
                ValueError,
            ):
                delay = 10

            normalized.append(
                {
                    "name": str(
                        vector.get(
                            "name",
                            "Unnamed Vector",
                        )
                    ),
                    "description": str(
                        vector.get(
                            "description",
                            "",
                        )
                    ),
                    "inputs": inputs,
                    "expected_outputs": expected,
                    "delay": delay,
                }
            )

        return normalized

    # =============================================================
    # TEST VECTOR GENERATION
    # =============================================================

    @staticmethod
    def _vectors_from_test_cases(
        test_cases: list[
            dict[str, str]
        ],
    ) -> list[dict[str, Any]]:
        """
        Create minimal vectors when the LLM supplied only
        test cases.

        The VerificationAgent performs the deterministic
        expected-value calculation later.
        """

        vectors: list[
            dict[str, Any]
        ] = []

        for case in test_cases:

            vectors.append(
                {
                    "name": case["name"],
                    "description": case[
                        "description"
                    ],
                    "inputs": {},
                    "expected_outputs": {},
                    "delay": 10,
                }
            )

        return vectors

    # =============================================================
    # STRING LIST NORMALIZATION
    # =============================================================

    @staticmethod
    def _normalize_string_list(
        values: Any,
    ) -> list[str]:
        """
        Normalize assertions or coverage points.
        """

        if not isinstance(
            values,
            list,
        ):
            return []

        normalized: list[str] = []

        for item in values:

            if isinstance(
                item,
                str,
            ):

                normalized.append(
                    item
                )

            elif isinstance(
                item,
                dict,
            ):

                normalized.append(
                    str(
                        item.get(
                            "assertion"
                        )
                        or item.get(
                            "description"
                        )
                        or item.get(
                            "name"
                        )
                        or item
                    )
                )

            else:

                normalized.append(
                    str(item)
                )

        return normalized