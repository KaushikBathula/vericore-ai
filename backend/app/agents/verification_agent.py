"""
Verification Agent.

Generates and normalizes verification plans for RTL designs.

The agent uses the LLM for verification planning, but performs
deterministic validation and arithmetic expected-value calculation
where the behavior can be derived from the requirement.
"""

from __future__ import annotations

import json
import logging
import re
from typing import Any

from backend.app.ai.prompts import get_prompt
from backend.app.core.llm_client import LLMClient
from backend.app.core.parsers.verification_parser import VerificationParser
from backend.app.schemas.requirement_spec import RequirementSpec
from backend.app.schemas.rtl_design import RTLDesign
from backend.app.schemas.test_vector import TestVector
from backend.app.schemas.verification_plan import VerificationPlan


logger = logging.getLogger(__name__)


class VerificationAgent:
    """
    Generates a verification plan for an RTL design.

    LLM-generated verification vectors are treated as untrusted input.
    The agent validates signal names, widths, values, and expected
    arithmetic outputs before returning the final VerificationPlan.
    """

    def __init__(self) -> None:
        self.llm = LLMClient()

    def execute(
        self,
        requirement_spec: RequirementSpec,
        rtl_design: RTLDesign,
    ) -> VerificationPlan:

        logger.info("Starting verification planning.")

        # ---------------------------------------------------------
        # 1. Load verification prompt
        # ---------------------------------------------------------

        system_prompt = get_prompt("verification")

        user_prompt = json.dumps(
            {
                "RequirementSpec": requirement_spec.model_dump(
                    mode="json"
                ),
                "RTLDesign": rtl_design.model_dump(
                    mode="json"
                ),
            },
            indent=2,
        )

        # ---------------------------------------------------------
        # 2. Ask LLM for initial verification plan
        # ---------------------------------------------------------

        response = self.llm.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )

        print(
            "\n========== RAW VERIFICATION RESPONSE ==========\n"
        )
        print(response.content)
        print(
            "\n===============================================\n"
        )

        if not response.success:
            raise RuntimeError(
                f"LLM generation failed: {response.error}"
            )

        # ---------------------------------------------------------
        # 3. Parse LLM response
        # ---------------------------------------------------------

        plan = VerificationParser.parse(
            response.content
        )

        # ---------------------------------------------------------
        # 4. Determine signal widths
        # ---------------------------------------------------------

        input_widths = {
            signal.signal_name: signal.signal_width
            for signal in requirement_spec.inputs
            if signal.signal_name
        }

        output_widths = {
            signal.signal_name: signal.signal_width
            for signal in requirement_spec.outputs
            if signal.signal_name
        }

        logger.info(
            "Verification signal widths: inputs=%s outputs=%s",
            input_widths,
            output_widths,
        )

        # ---------------------------------------------------------
        # 5. Detect supported operation
        # ---------------------------------------------------------

        operation = self._detect_operation(
            requirement_spec
        )

        logger.info(
            "Detected verification operation: %s",
            operation,
        )

        # ---------------------------------------------------------
        # 6. Normalize LLM-generated vectors
        # ---------------------------------------------------------

        normalized_vectors: list[TestVector] = []

        for vector in plan.test_vectors:

            # -----------------------------------------------------
            # Make sure we always work with a TestVector object.
            # -----------------------------------------------------

            if isinstance(vector, TestVector):
                vector_data = vector.model_dump()
            elif isinstance(vector, dict):
                vector_data = dict(vector)
            else:
                vector_data = {
                    "name": str(
                        getattr(
                            vector,
                            "name",
                            "Generated Test Vector",
                        )
                    ),
                    "description": str(
                        getattr(
                            vector,
                            "description",
                            "",
                        )
                    ),
                    "inputs": dict(
                        getattr(
                            vector,
                            "inputs",
                            {},
                        )
                    ),
                    "expected_outputs": dict(
                        getattr(
                            vector,
                            "expected_outputs",
                            {},
                        )
                    ),
                    "delay": int(
                        getattr(
                            vector,
                            "delay",
                            10,
                        )
                    ),
                }

            # -----------------------------------------------------
            # Input values
            # -----------------------------------------------------

            inputs = dict(
                vector_data.get(
                    "inputs",
                    {},
                )
            )

            normalized_inputs: dict[str, int] = {}

            for signal_name, value in inputs.items():

                # -------------------------------------------------
                # Reject unknown signals.
                # -------------------------------------------------

                if signal_name not in input_widths:
                    logger.warning(
                        "Removing unknown verification input '%s'.",
                        signal_name,
                    )
                    continue

                # -------------------------------------------------
                # Convert to integer.
                # -------------------------------------------------

                try:
                    numeric_value = int(value)

                except (TypeError, ValueError):

                    logger.warning(
                        "Invalid input value for '%s': %r. "
                        "Replacing with 0.",
                        signal_name,
                        value,
                    )

                    numeric_value = 0

                # -------------------------------------------------
                # Enforce signal width.
                # -------------------------------------------------

                width = input_widths[signal_name]

                if width > 0:

                    max_value = (
                        (2 ** width) - 1
                    )

                    if numeric_value < 0:

                        logger.warning(
                            "Input '%s' value %s is negative. "
                            "Replacing with 0.",
                            signal_name,
                            numeric_value,
                        )

                        numeric_value = 0

                    if numeric_value > max_value:

                        logger.warning(
                            "Input '%s' value %s exceeds "
                            "%d-bit range 0..%d. "
                            "Applying modulo.",
                            signal_name,
                            numeric_value,
                            width,
                            max_value,
                        )

                        numeric_value %= (
                            2 ** width
                        )

                normalized_inputs[
                    signal_name
                ] = numeric_value

            # -----------------------------------------------------
            # Calculate expected outputs.
            # -----------------------------------------------------

            if operation == "unsigned_addition":

                expected_outputs = (
                    self._calculate_addition_outputs(
                        inputs=normalized_inputs,
                        output_widths=output_widths,
                    )
                )

            else:

                expected_outputs = (
                    self._normalize_expected_outputs(
                        expected_outputs=dict(
                            vector_data.get(
                                "expected_outputs",
                                {},
                            )
                        ),
                        output_widths=output_widths,
                    )
                )

            # -----------------------------------------------------
            # Rebuild as a real TestVector object.
            # -----------------------------------------------------

            normalized_vector = TestVector(
                name=str(
                    vector_data.get(
                        "name",
                        "Generated Test Vector",
                    )
                ),
                description=str(
                    vector_data.get(
                        "description",
                        "",
                    )
                ),
                inputs=normalized_inputs,
                expected_outputs=expected_outputs,
                delay=int(
                    vector_data.get(
                        "delay",
                        10,
                    )
                ),
            )

            normalized_vectors.append(
                normalized_vector
            )

        # ---------------------------------------------------------
        # 7. Generate exhaustive vectors for small unsigned
        #    addition designs.
        # ---------------------------------------------------------

        if operation == "unsigned_addition":

            exhaustive_vectors = (
                self._generate_exhaustive_addition_vectors(
                    input_widths=input_widths,
                    output_widths=output_widths,
                )
            )

            if exhaustive_vectors:

                logger.info(
                    "Using deterministic exhaustive verification "
                    "for unsigned addition."
                )

                normalized_vectors = (
                    exhaustive_vectors
                )

        # ---------------------------------------------------------
        # 8. Rebuild final verification plan.
        # ---------------------------------------------------------

        plan = plan.model_copy(
            update={
                "test_vectors": normalized_vectors,
            }
        )

        # ---------------------------------------------------------
        # 9. Display final vectors.
        # ---------------------------------------------------------

        print(
            "\n========== FINAL VERIFICATION VECTORS ==========\n"
        )

        for vector in plan.test_vectors:

            print(
                {
                    "name": vector.name,
                    "inputs": vector.inputs,
                    "expected_outputs": vector.expected_outputs,
                    "delay": vector.delay,
                }
            )

        print(
            "\n=================================================\n"
        )

        logger.info(
            "Verification planning completed successfully."
        )

        return plan

    # =============================================================
    # OPERATION DETECTION
    # =============================================================

    def _detect_operation(
        self,
        requirement_spec: RequirementSpec,
    ) -> str | None:

        """
        Detect supported arithmetic operations from the
        requirement specification.

        Currently supports unsigned addition.
        """

        text_parts: list[str] = []

        text_parts.append(
            requirement_spec.description or ""
        )

        for operation in (
            requirement_spec.operations or []
        ):
            if isinstance(operation, str):
                text_parts.append(operation)

            elif isinstance(operation, dict):
                text_parts.append(
                    json.dumps(operation)
                )

            else:
                text_parts.append(
                    str(operation)
                )

        text = " ".join(text_parts).lower()

        # ---------------------------------------------------------
        # Addition
        # ---------------------------------------------------------

        addition_patterns = [
            r"\badd\b",
            r"\badder\b",
            r"\baddition\b",
            r"\bsum\b",
            r"\ba\s*\+\s*b\b",
            r"\bperform.*addition\b",
        ]

        for pattern in addition_patterns:

            if re.search(
                pattern,
                text,
                flags=re.IGNORECASE,
            ):
                return "unsigned_addition"

        return None

    # =============================================================
    # ADDITION OUTPUT CALCULATION
    # =============================================================

    def _calculate_addition_outputs(
        self,
        inputs: dict[str, int],
        output_widths: dict[str, int],
    ) -> dict[str, int]:

        """
        Calculate deterministic expected outputs for
        unsigned addition.
        """

        if not inputs:
            return {}

        # ---------------------------------------------------------
        # Identify operands.
        #
        # The current project convention uses A and B.
        # If those exist, use them.
        # ---------------------------------------------------------

        if "A" in inputs and "B" in inputs:

            a = int(inputs["A"])
            b = int(inputs["B"])

        else:

            values = list(inputs.values())

            if len(values) < 2:
                return {}

            a = int(values[0])
            b = int(values[1])

        total = a + b

        expected_outputs: dict[str, int] = {}

        # ---------------------------------------------------------
        # SUM
        # ---------------------------------------------------------

        if "SUM" in output_widths:

            sum_width = output_widths["SUM"]

            if sum_width > 0:

                modulus = 2 ** sum_width

                expected_outputs["SUM"] = (
                    total % modulus
                )

            else:

                expected_outputs["SUM"] = total

        # ---------------------------------------------------------
        # CARRY
        # ---------------------------------------------------------

        if "CARRY" in output_widths:

            sum_width = output_widths.get(
                "SUM",
                max(
                    input_widths
                    if False
                    else [1]
                ),
            )

            if sum_width > 0:

                expected_outputs["CARRY"] = int(
                    total >= (2 ** sum_width)
                )

            else:

                expected_outputs["CARRY"] = 0

        # ---------------------------------------------------------
        # Other explicitly declared outputs.
        #
        # We do not invent values for outputs that cannot be
        # deterministically derived from the detected addition.
        # ---------------------------------------------------------

        return expected_outputs

    # =============================================================
    # EXHAUSTIVE ADDITION VECTORS
    # =============================================================

    def _generate_exhaustive_addition_vectors(
        self,
        input_widths: dict[str, int],
        output_widths: dict[str, int],
    ) -> list[TestVector]:

        """
        Generate exhaustive vectors for a small unsigned
        two-operand addition.

        For the 2-bit adder:

            A ∈ {0,1,2,3}
            B ∈ {0,1,2,3}

        Therefore:

            4 × 4 = 16 vectors
        """

        if "A" not in input_widths:
            return []

        if "B" not in input_widths:
            return []

        a_width = input_widths["A"]
        b_width = input_widths["B"]

        # ---------------------------------------------------------
        # Exhaustive generation is intentionally limited to
        # reasonably small input spaces.
        # ---------------------------------------------------------

        if a_width <= 0 or b_width <= 0:
            return []

        a_count = 2 ** a_width
        b_count = 2 ** b_width

        total_vectors = (
            a_count * b_count
        )

        # Prevent accidental explosion for large designs.
        if total_vectors > 256:
            logger.info(
                "Skipping exhaustive addition generation: "
                "%d vectors would be required.",
                total_vectors,
            )
            return []

        vectors: list[TestVector] = []

        for a in range(a_count):

            for b in range(b_count):

                total = a + b

                # -------------------------------------------------
                # SUM
                # -------------------------------------------------

                expected_outputs: dict[str, int] = {}

                if "SUM" in output_widths:

                    sum_width = output_widths["SUM"]

                    if sum_width > 0:

                        expected_outputs["SUM"] = (
                            total
                            % (2 ** sum_width)
                        )

                    else:

                        expected_outputs["SUM"] = (
                            total
                        )

                # -------------------------------------------------
                # CARRY
                # -------------------------------------------------

                if "CARRY" in output_widths:

                    sum_width = output_widths.get(
                        "SUM",
                        max(
                            a_width,
                            b_width,
                        ),
                    )

                    expected_outputs["CARRY"] = int(
                        total >= (2 ** sum_width)
                    )

                # -------------------------------------------------
                # Test-vector description
                # -------------------------------------------------

                description = (
                    f"Verify unsigned addition for "
                    f"A={a}, B={b}. "
                    f"Mathematical sum={total}."
                )

                # -------------------------------------------------
                # IMPORTANT:
                #
                # Return TestVector, NOT dict.
                # -------------------------------------------------

                vectors.append(
                    TestVector(
                        name=(
                            f"Addition Test "
                            f"A={a}, B={b}"
                        ),
                        description=description,
                        inputs={
                            "A": a,
                            "B": b,
                        },
                        expected_outputs=(
                            expected_outputs
                        ),
                        delay=10,
                    )
                )

        return vectors

    # =============================================================
    # EXPECTED OUTPUT NORMALIZATION
    # =============================================================

    def _normalize_expected_outputs(
        self,
        expected_outputs: dict[str, Any],
        output_widths: dict[str, int],
    ) -> dict[str, int]:

        """
        Normalize LLM-generated expected outputs against
        declared output signals and widths.
        """

        normalized: dict[str, int] = {}

        for signal_name, value in (
            expected_outputs.items()
        ):

            # -----------------------------------------------------
            # Remove unknown outputs.
            # -----------------------------------------------------

            if signal_name not in output_widths:

                logger.warning(
                    "Removing unknown verification "
                    "output '%s'.",
                    signal_name,
                )

                continue

            # -----------------------------------------------------
            # Convert to integer.
            # -----------------------------------------------------

            try:

                numeric_value = int(value)

            except (TypeError, ValueError):

                logger.warning(
                    "Invalid expected output value "
                    "for '%s': %r. Replacing with 0.",
                    signal_name,
                    value,
                )

                numeric_value = 0

            # -----------------------------------------------------
            # Normalize according to width.
            # -----------------------------------------------------

            width = output_widths[
                signal_name
            ]

            if width > 0:

                max_value = (
                    (2 ** width) - 1
                )

                if numeric_value < 0:

                    logger.warning(
                        "Expected output '%s' value %s "
                        "is negative. Replacing with 0.",
                        signal_name,
                        numeric_value,
                    )

                    numeric_value = 0

                elif numeric_value > max_value:

                    logger.warning(
                        "Expected output '%s' value %s "
                        "exceeds %d-bit range 0..%d. "
                        "Applying modulo normalization.",
                        signal_name,
                        numeric_value,
                        width,
                        max_value,
                    )

                    numeric_value %= (
                        2 ** width
                    )

            normalized[
                signal_name
            ] = numeric_value

        return normalized