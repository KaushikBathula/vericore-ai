import json
import re

from pydantic import ValidationError

from backend.app.schemas.requirement_spec import RequirementSpec
from backend.app.schemas.rtl_design import RTLDesign


class RTLResponseParser:
    """
    Converts raw LLM responses into validated RTLDesign objects.
    """

    @staticmethod
    def parse(
        response: str,
        requirement: RequirementSpec,
    ) -> RTLDesign:

        cleaned = re.search(r"\{.*\}", response, re.DOTALL)

        if cleaned:
            response = cleaned.group(0)

        data = json.loads(response)

        # Attach original requirement
        data["requirement"] = requirement

        # ----------------------------------
        # Normalize internal signals
        # ----------------------------------

        signals = data.get("internal_signals", [])
        normalized_signals = []

        for signal in signals:

            if isinstance(signal, str):

                normalized_signals.append(
                    {
                        "signal_name": signal,
                        "signal_width": 1,
                        "signal_type": "wire",
                    }
                )

            else:

                signal.setdefault("signal_width", 1)
                signal.setdefault("signal_type", "wire")

                normalized_signals.append(signal)

        data["internal_signals"] = normalized_signals

        # ----------------------------------
        # Normalize operations
        # ----------------------------------
        

        derived_ops = data.get("derived_operations")

        # If the RTL model omitted operations or returned an empty list,
        # reuse the operations extracted by the Requirement Agent.
        if not derived_ops:

            if "operations" in data and data["operations"]:
                data["derived_operations"] = data.pop("operations")

            else:
                data["derived_operations"] = [
                    op.model_dump()
                    for op in requirement.operations
                ]

        for op in data["derived_operations"]:

            if "name" in op and "operation_name" not in op:
                op["operation_name"] = op.pop("name")

            if "operation_type" in op and "operation_name" not in op:
                op["operation_name"] = op.pop("operation_type")

            if "functionality" in op and "description" not in op:
                op["description"] = op.pop("functionality")

            if "function" in op and "description" not in op:
                op["description"] = op.pop("function")
        try:
            return RTLDesign.model_validate(data)

        except ValidationError as exc:
            raise ValueError(
                f"RTL design validation failed:\n{exc}"
            ) from exc