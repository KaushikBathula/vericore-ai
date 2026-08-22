import json
import re
from typing import Any

from pydantic import ValidationError

from backend.app.schemas.requirement_spec import RequirementSpec
from backend.app.utils.json_repair import repair_json


class ResponseParser:
    """
    Converts raw LLM responses into validated RequirementSpec objects.
    """

    @staticmethod
    def parse_requirement_response(response: str) -> RequirementSpec:
        """
        Parse a raw LLM response into a RequirementSpec.
        """

        # ----------------------------------------
        # Clean LLM response
        # ----------------------------------------

        response = ResponseParser._strip_markdown(response)
        response = repair_json(response)

        # ----------------------------------------
        # Parse JSON
        # ----------------------------------------

        try:
            data = json.loads(response)

        except json.JSONDecodeError as exc:
            raise ValueError(
                f"Invalid JSON in requirement response: {exc}"
            ) from exc

        # ----------------------------------------
        # Default required fields
        # ----------------------------------------

        data.setdefault("description", "")
        data.setdefault("inputs", [])
        data.setdefault("outputs", [])
        data.setdefault("operations", [])
        data.setdefault("parameters", {})
        data.setdefault("verification_points", [])

        # ----------------------------------------
        # Normalize LLM output
        # ----------------------------------------

        ResponseParser._normalize_ports(data)
        ResponseParser._normalize_operations(data)
        ResponseParser._normalize_verification_points(data)

        # ----------------------------------------
        # Validate RequirementSpec
        # ----------------------------------------

        try:
            return RequirementSpec.model_validate(data)

        except ValidationError as exc:
            raise ValueError(
                f"Requirement specification validation failed:\n{exc}"
            ) from exc

    # ============================================================
    # MARKDOWN CLEANUP
    # ============================================================

    @staticmethod
    def _strip_markdown(text: str) -> str:
        """
        Remove ```json ... ``` wrappers if present.
        """

        pattern = r"```(?:json)?(.*?)```"

        match = re.search(
            pattern,
            text,
            re.DOTALL,
        )

        if match:
            return match.group(1).strip()

        return text.strip()

    # ============================================================
    # SIGNAL NAME NORMALIZATION
    # ============================================================

    @staticmethod
    def _normalize_signal_name(name: str) -> str:
        """
        Normalize signal names.

        Examples:

            A[1:0]   -> A
            SUM[7:0] -> SUM
            A[1:0],  -> A
        """

        name = str(name).strip()

        # Remove Verilog bus/range notation.
        #
        # Example:
        # A[1:0] -> A
        # DATA[7:0] -> DATA
        name = re.sub(
            r"\[.*?\]",
            "",
            name,
        )

        # Remove punctuation that may have been introduced
        # by malformed or repaired LLM JSON.
        #
        # Example:
        # A, -> A
        # A; -> A
        name = name.rstrip(
            " ,;:"
        )

        return name.strip()

    # ============================================================
    # PORT NORMALIZATION
    # ============================================================

    @staticmethod
    def _normalize_ports(
        data: dict[str, Any],
    ) -> None:
        """
        Normalize hardware port information.

        The LLM may omit the direction field.

        Direction is inferred from the containing list:

            inputs  -> input
            outputs -> output

        Short forms are also normalized:

            in  -> input
            out -> output
        """

        for group in (
            "inputs",
            "outputs",
        ):

            expected_direction = (
                "input"
                if group == "inputs"
                else "output"
            )

            for port in data.get(
                group,
                [],
            ):

                # ----------------------------------------
                # Normalize direction
                # ----------------------------------------

                direction = port.get(
                    "direction"
                )

                if direction:

                    direction = str(
                        direction
                    ).lower().strip()

                    if direction in (
                        "in",
                        "input",
                    ):
                        port["direction"] = "input"

                    elif direction in (
                        "out",
                        "output",
                    ):
                        port["direction"] = "output"

                    else:
                        # Unknown direction.
                        #
                        # Since the port belongs to either
                        # inputs or outputs, use the group
                        # to infer the correct direction.
                        port["direction"] = (
                            expected_direction
                        )

                else:
                    # Direction was omitted by the LLM.
                    #
                    # Infer it from the list in which the
                    # port appears.
                    port["direction"] = (
                        expected_direction
                    )

                # ----------------------------------------
                # Normalize signal name
                # ----------------------------------------

                if "signal_name" in port:

                    port["signal_name"] = (
                        ResponseParser._normalize_signal_name(
                            port["signal_name"]
                        )
                    )

    # ============================================================
    # OPERATION NORMALIZATION
    # ============================================================

    @staticmethod
    def _normalize_operations(
        data: dict[str, Any],
    ) -> None:
        """
        Normalize operation fields returned by
        different LLM responses.
        """

        for operation in data.get(
            "operations",
            [],
        ):

            # ----------------------------------------
            # name -> operation_name
            # ----------------------------------------

            if (
                "operation_name"
                not in operation
                and "name"
                in operation
            ):

                operation["operation_name"] = (
                    operation.pop("name")
                )

            # ----------------------------------------
            # operation_type -> operation_name
            # ----------------------------------------

            if (
                "operation_name"
                not in operation
                and "operation_type"
                in operation
            ):

                operation["operation_name"] = (
                    operation.pop(
                        "operation_type"
                    )
                )

            # ----------------------------------------
            # functionality -> description
            # ----------------------------------------

            if (
                "description"
                not in operation
                and "functionality"
                in operation
            ):

                operation["description"] = (
                    operation.pop(
                        "functionality"
                    )
                )

            # ----------------------------------------
            # function -> description
            # ----------------------------------------

            if (
                "description"
                not in operation
                and "function"
                in operation
            ):

                operation["description"] = (
                    operation["function"]
                )

            # ----------------------------------------
            # Default description
            # ----------------------------------------

            operation.setdefault(
                "description",
                "",
            )

    # ============================================================
    # VERIFICATION POINT NORMALIZATION
    # ============================================================

    @staticmethod
    def _normalize_verification_points(
        data: dict[str, Any],
    ) -> None:
        """
        Normalize verification points returned by
        different LLM responses.

        VerificationPoint uses:

            description
            test_case
            point_name

        The LLM may return:

            "Verify addition"

        or:

            {
                "name": "CarryCheck",
                "description": "Verify carry"
            }

        or:

            {
                "point_name": "CarryCheck",
                "description": "Verify carry"
            }
        """

        normalized = []

        for vp in data.get(
            "verification_points",
            [],
        ):

            # ----------------------------------------
            # String verification point
            # ----------------------------------------

            if isinstance(
                vp,
                str,
            ):

                normalized.append(
                    {
                        "description": vp,
                        "point_name": vp,
                        "test_case": None,
                    }
                )

            # ----------------------------------------
            # Dictionary verification point
            # ----------------------------------------

            elif isinstance(
                vp,
                dict,
            ):

                point_name = vp.get(
                    "point_name",
                    vp.get(
                        "name",
                        "Verification",
                    ),
                )

                description = vp.get(
                    "description",
                    "",
                )

                normalized.append(
                    {
                        "description": description,
                        "point_name": point_name,
                        "test_case": vp.get(
                            "test_case"
                        ),
                    }
                )

        data["verification_points"] = normalized