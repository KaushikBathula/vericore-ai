import json
import re
from typing import Any

from pydantic import ValidationError

from app.schemas.requirement_spec import RequirementSpec


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

        data = json.loads(response)

        ResponseParser._normalize_ports(data)
        ResponseParser._normalize_operations(data)

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

            if (
                "description" not in operation
                and "functionality" in operation
            ):
                operation["description"] = operation.pop("functionality")

            elif (
                "description" not in operation
                and "function" in operation
            ):
                operation["description"] = operation["function"]