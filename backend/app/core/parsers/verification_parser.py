import json
import re
from backend.app.utils.json_repair import repair_json
from pydantic import ValidationError
from backend.app.schemas.test_vector import TestVector
from backend.app.schemas.verification_plan import VerificationPlan


class VerificationParser:
    """
    Converts raw LLM verification responses into a validated VerificationPlan.
    """

    @staticmethod
    def parse(response: str) -> VerificationPlan:

        cleaned = re.search(r"\{.*\}", response, re.DOTALL)

        if cleaned:
            response = cleaned.group(0)
        response = repair_json(response)

        data = json.loads(response)

        # --------------------------------------------------
        # Normalize Test Cases
        # --------------------------------------------------

        normalized_cases = []

        for tc in data.get("test_cases", []):

            if isinstance(tc, str):

                normalized_cases.append(
                    {
                        "name": tc,
                        "description": tc,
                        "stimulus": "",
                        "expected_result": "",
                    }
                )

                continue

            stimulus = (
                tc.get("stimulus")
                or tc.get("inputs")
                or tc.get("input")
                or tc.get("test_input")
                or ""
            )

            expected = (
                tc.get("expected_result")
                or tc.get("expected_output")
                or tc.get("expected_outputs")
                or tc.get("expected")
                or ""
            )

            normalized_cases.append(
                {
                    "name": tc.get("name", "Unnamed Test"),
                    "description": tc.get("description", ""),
                    "stimulus": str(stimulus),
                    "expected_result": str(expected),
                }
            )

        data["test_cases"] = normalized_cases
        # --------------------------------------------------
        # Normalize Test Vectors
        # --------------------------------------------------

        normalized_vectors = []

        for vector in data.get("test_vectors", []):

            if not isinstance(vector, dict):
                continue

            normalized_vectors.append(
                {
                    "name": vector.get("name", "Unnamed Vector"),
                    "description": vector.get("description", ""),
                    "inputs": vector.get("inputs", {}),
                    "expected_outputs": vector.get(
                        "expected_outputs",
                        {},
                    ),
                    "delay": vector.get("delay", 10),
                }
            )

        data["test_vectors"] = normalized_vectors
        # --------------------------------------------------
        # Normalize Test Vectors
        # --------------------------------------------------

        normalized_vectors = []

        for vector in data.get("test_vectors", []):

            if isinstance(vector, dict):

                inputs = (
                    vector.get("inputs")
                    or vector.get("stimulus")
                    or {}
                )

                expected = (
                    vector.get("expected_outputs")
                    or vector.get("expected_result")
                    or vector.get("expected")
                    or {}
                )

                if not isinstance(inputs, dict):
                    inputs = {}

                if not isinstance(expected, dict):
                    expected = {}

                normalized_vectors.append(
                    {
                        "name": vector.get(
                            "name",
                            "Unnamed Vector",
                        ),
                        "description": vector.get(
                            "description",
                            "",
                        ),
                        "inputs": inputs,
                        "expected_outputs": expected,
                        "delay": int(
                            vector.get("delay", 10)
                        ),
                    }
                )

        data["test_vectors"] = normalized_vectors
        if (
            not data["test_vectors"]
            and data.get("test_cases")
        ):

            generated_vectors = []

            for case in data["test_cases"]:

                generated_vectors.append(
                    {
                        "name": case["name"],
                        "description": case["description"],
                        "inputs": {},
                        "expected_outputs": {},
                        "delay": 10,
                    }
                )

            data["test_vectors"] = generated_vectors
        # --------------------------------------------------
        # Normalize Assertions
        # --------------------------------------------------

        assertions = []

        for item in data.get("assertions", []):

            if isinstance(item, str):
                assertions.append(item)

            elif isinstance(item, dict):

                assertions.append(
                    item.get("assertion")
                    or item.get("description")
                    or item.get("name")
                    or str(item)
                )

        data["assertions"] = assertions

        # --------------------------------------------------
        # Normalize Coverage
        # --------------------------------------------------

        coverage = []

        for item in data.get("coverage_points", []):

            if isinstance(item, str):
                coverage.append(item)

            elif isinstance(item, dict):

                coverage.append(
                    item.get("description")
                    or item.get("name")
                    or str(item)
                )

        data["coverage_points"] = coverage

        try:
            return VerificationPlan.model_validate(data)

        except ValidationError as exc:

            raise ValueError(
                f"Verification validation failed:\n{exc}"
            ) from exc