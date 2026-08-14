import json
import re

from pydantic import ValidationError

from backend.app.core.parsers.response_parser import ResponseParser
from backend.app.schemas.verification_plan import VerificationPlan
from backend.app.utils.json_repair import repair_json


class VerificationParser:
    """
    Converts raw LLM verification responses into a validated VerificationPlan.
    """
    
    @staticmethod
    def parse(response: str) -> VerificationPlan:

        print("\n***** VerificationParser.parse() CALLED *****\n")

        response = ResponseParser._strip_markdown(response)
        response = repair_json(response)

        response = re.sub(
            r"\b0b([01]+)\b",
            lambda m: str(int(m.group(1), 2)),
            response,
        )

        try:
             data = json.loads(response)

        except json.JSONDecodeError as exc:

            print("\n========== INVALID VERIFICATION JSON ==========\n")
            print(response)
            print("\n===============================================\n")

            print(
                f"JSON error at line {exc.lineno}, "
                f"column {exc.colno}, "
                f"character {exc.pos}"
            )

            raise

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
            print("\nRAW VECTOR:")
            print(vector)
            print(type(vector))
            if not isinstance(vector, dict):
                continue

            inputs = vector.get("inputs")
            expected = vector.get("expected_outputs")

            # Support flat AI output
            if inputs is None and expected is None:

                inputs = {}
                expected = {}

                for key, value in vector.items():

                    upper = key.upper()

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
                    }:
                        expected[key] = value

            else:

                inputs = (
                    inputs
                    or vector.get("stimulus")
                    or {}
                )

                expected = (
                    expected
                    or vector.get("expected_result")
                    or vector.get("expected")
                    or {}
                )

            if not isinstance(inputs, dict):
                inputs = {}

            if not isinstance(expected, dict):
                expected = {}

            inputs = {
                k: v
                for k, v in inputs.items()
                if v is not None
            }

            expected = {
                k: v
                for k, v in expected.items()
                if v is not None
            }
            print("Inputs:", inputs)
            print("Expected Outputs:", expected)
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

        # --------------------------------------------------
        # Generate vectors if only test cases exist
        # --------------------------------------------------

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

        print("\n========== PARSED TEST VECTORS ==========\n")

        for vector in data["test_vectors"]:
            print(vector)

        print("\n=========================================\n")

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