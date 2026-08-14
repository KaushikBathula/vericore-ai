import json
import re

from pydantic import ValidationError
from backend.app.utils.json_repair import repair_json
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
        response = repair_json(response)
        data = json.loads(response)

        # Attach original requirement
        data["requirement"] = requirement

        # -----------------------------
        # Parameters
        # -----------------------------
        if "parameters" not in data:
            data["parameters"] = {}

        # -----------------------------
        # Internal signals
        # -----------------------------
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


        # If the LLM omitted internal signals, derive
        # implementation signals from the RTL operations.
        if not normalized_signals:

            output_names = {
                output.signal_name
                for output in requirement.outputs
            }

            for operation in requirement.operations:

                operation_name = operation.operation_name.lower()

                if operation_name == "addition":
                    signal_name = "addition_result"

                elif operation_name == "subtraction":
                    signal_name = "subtraction_result"

                else:
                    signal_name = f"{operation_name}_result"

                # Avoid creating an internal signal that
                # conflicts with an existing output.
                if signal_name in output_names:
                    continue

                # Avoid duplicates.
                if any(
                    signal["signal_name"] == signal_name
                    for signal in normalized_signals
                ):
                    continue

                normalized_signals.append(
                    {
                        "signal_name": signal_name,
                        "signal_width": max(
                            (
                                output.signal_width
                                for output in requirement.outputs
                            ),
                            default=1,
                        ),
                        "signal_type": "wire",
                    }
                )      

        data["internal_signals"] = normalized_signals

        # -----------------------------
        # Operations
        # -----------------------------
        derived_ops = data.get("derived_operations")

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

            if "signal_name" in op and "operation_name" not in op:
                op["operation_name"] = op.pop("signal_name")    

            if "functionality" in op and "description" not in op:
                op["description"] = op.pop("functionality")

            if "function" in op and "description" not in op:
                op["description"] = op.pop("function")

    # -----------------------------
    # Normalize RTL generation fields
    # -----------------------------

            op.setdefault("destination", None)

            op.setdefault("expression", None)

            op.setdefault("implementation_style", "assign")

            op.setdefault("operands", [])

            op.setdefault("operator", None)

        
        try:
            return RTLDesign.model_validate(data)

        except ValidationError as exc:
            raise ValueError(
                f"RTL design validation failed:\n{exc}"
            ) from exc