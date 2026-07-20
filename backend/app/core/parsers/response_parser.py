import json
from backend.app.utils.json_repair import repair_json
import re
from typing import Any

from pydantic import ValidationError
from backend.app.utils.json_repair import repair_json
from backend.app.schemas.requirement_spec import RequirementSpec


class ResponseParser:
    """
    Converts raw LLM responses into validated RequirementSpec objects.
    """

    @staticmethod
    def parse_requirement_response(response: str) -> RequirementSpec:
        """
        Parse a raw LLM response into a RequirementSpec.
        """

        response = ResponseParser._strip_markdown(response)
        response = repair_json(response)
        data = json.loads(response)
        # -----------------------------
        # Default required fields
        # -----------------------------

        data.setdefault("description", "")
        data.setdefault("parameters", {})
        data.setdefault("verification_points", [])
        ResponseParser._normalize_ports(data)
        ResponseParser._normalize_operations(data)
        ResponseParser._normalize_verification_points(data)
        try:
            return RequirementSpec.model_validate(data)

        except ValidationError as exc:
            raise ValueError(
                f"Requirement specification validation failed:\n{exc}"
            ) from exc

    @staticmethod
    def _strip_markdown(text: str) -> str:
        """
        Remove ```json ... ``` wrappers if present.
        """

        pattern = r"```(?:json)?(.*?)```"
        match = re.search(pattern, text, re.DOTALL)

        if match:
            return match.group(1).strip()

        return text.strip()

    @staticmethod
    def _normalize_ports(data: dict[str, Any]) -> None:
        """
        Normalize port directions.
        """

        for group in ("inputs", "outputs"):
            for port in data.get(group, []):

                direction = port.get("direction", "").lower()

                if direction == "in":
                    port["direction"] = "input"

                elif direction == "out":
                    port["direction"] = "output"

    @staticmethod
    def _normalize_operations(data: dict[str, Any]) -> None:
        """
        Normalize operation fields returned by different LLMs.
        """

        for operation in data.get("operations", []):

            # name -> operation_name
            if (
                "operation_name" not in operation
                and "name" in operation
            ):
                operation["operation_name"] = operation.pop("name")

            # operation_type -> operation_name
            if (
                "operation_name" not in operation
                and "operation_type" in operation
            ):
                operation["operation_name"] = operation.pop("operation_type")

            # functionality -> description
            if (
                "description" not in operation
                and "functionality" in operation
            ):
                operation["description"] = operation.pop("functionality")

            # function -> description
            if (
                "description" not in operation
                and "function" in operation
            ):
                operation["description"] = operation["function"]

            operation.setdefault("description", "")
    @staticmethod
    def _normalize_verification_points(
        data: dict[str, Any],
    ) -> None:
        """
        Normalize verification points returned by different LLMs.
        """

        normalized = []

        for vp in data.get("verification_points", []):

            if isinstance(vp, str):

                normalized.append(
                    {
                        "name": vp,
                        "description": vp,
                    }
                )

            elif isinstance(vp, dict):

                normalized.append(
                    {
                        "name": vp.get(
                            "name",
                            vp.get(
                                "point_name",
                                "Verification"
                            ),
                        ),
                        "description": vp.get(
                            "description",
                            "",
                        ),
                    }
                )

        data["verification_points"] = normalized