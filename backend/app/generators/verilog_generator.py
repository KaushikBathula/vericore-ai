"""
Verilog HDL generator.

Generates synthesizable Verilog from an RTLDesign.
"""

from __future__ import annotations

from backend.app.generators.base import HDLGenerator
from backend.app.generators.formatter import VerilogFormatter
from backend.app.schemas.rtl_design import RTLDesign


class VerilogGenerator(HDLGenerator):
    """
    Generates Verilog HDL from an RTLDesign.
    """

    def _generate_port_declarations(
        self,
        rtl_design: RTLDesign,
        use_parameter: bool = False,
    ) -> str:

        ports = []

        print("\n========== PORT DEBUG ==========")

        print("\nInputs:")
        for port in rtl_design.requirement.inputs:
            print(port.model_dump())

        print("\nOutputs:")
        for port in rtl_design.requirement.outputs:
            print(port.model_dump())

        print("\n================================\n")

        for port in rtl_design.requirement.inputs:
            ports.append(
                "    "
                + VerilogFormatter.format_port(
                    port,
                    use_parameter=use_parameter,
                )
            )

        for port in rtl_design.requirement.outputs:
            ports.append(
                "    "
                + VerilogFormatter.format_port(
                    port,
                    use_parameter=use_parameter,
                )
            )

        return ",\n".join(ports)

    def _generate_internal_signals(
        self,
        rtl_design: RTLDesign,
        use_parameter: bool = False,
    ) -> str:

        declarations = []

        for signal in rtl_design.internal_signals:
            declarations.append(
                "    "
                + VerilogFormatter.format_signal(
                    signal,
                    use_parameter=use_parameter,
                )
            )

        return "\n".join(declarations)

    def _find_operator(
        self,
        operation_name: str,
    ) -> str | None:
        """
        Determine the Verilog operator corresponding to
        an operation name.
        """

        name = operation_name.lower().strip()

        if "add" in name or "addition" in name:
            return "+"

        if "sub" in name or "subtract" in name:
            return "-"

        if "xor" in name:
            return "^"

        if "and" in name:
            return "&"

        if (
            name == "or"
            or name.endswith("_or")
            or " or " in name
        ):
            return "|"

        return None

    def _find_output(
        self,
        rtl_design: RTLDesign,
        names: list[str],
    ) -> str | None:
        """
        Find an output using case-insensitive name matching.
        """

        wanted = {
            name.upper()
            for name in names
        }

        for output in rtl_design.requirement.outputs:

            if output.signal_name.upper() in wanted:
                return output.signal_name

        return None

    def _is_comparator(
        self,
        operation_name: str,
        rtl_design: RTLDesign,
    ) -> bool:
        """
        Determine whether the RTL design represents a comparator.

        Detection is intentionally based on both the operation name
        and the output interface so that minor LLM wording variations
        do not prevent comparator generation.
        """

        name = operation_name.lower().strip()

        comparator_keywords = (
            "compar",
            "compare",
            "comparison",
            "magnitude",
            "greater",
            "less",
            "equal",
        )

        if any(
            keyword in name
            for keyword in comparator_keywords
        ):
            return True

        output_names = {
            output.signal_name.upper()
            for output in rtl_design.requirement.outputs
        }

        comparator_outputs = {
            "GT",
            "LT",
            "EQ",
        }

        return comparator_outputs.issubset(
            output_names
        )

    def _generate_comparator_logic(
        self,
        rtl_design: RTLDesign,
    ) -> list[str]:
        """
        Generate standard magnitude comparator logic.

        GT = 1 when A > B
        LT = 1 when A < B
        EQ = 1 when A == B
        """

        inputs = rtl_design.requirement.inputs

        if len(inputs) < 2:
            return []

        a = inputs[0].signal_name
        b = inputs[1].signal_name

        gt_output = self._find_output(
            rtl_design,
            [
                "GT",
                "GREATER",
                "GREATER_THAN",
            ],
        )

        lt_output = self._find_output(
            rtl_design,
            [
                "LT",
                "LESS",
                "LESS_THAN",
            ],
        )

        eq_output = self._find_output(
            rtl_design,
            [
                "EQ",
                "EQUAL",
                "EQUALS",
            ],
        )

        statements = []

        if gt_output is not None:
            statements.append(
                f"    assign {gt_output} = {a} > {b};"
            )

        if lt_output is not None:
            statements.append(
                f"    assign {lt_output} = {a} < {b};"
            )

        if eq_output is not None:
            statements.append(
                f"    assign {eq_output} = {a} == {b};"
            )

        return statements

    def _generate_adder_logic(
        self,
        rtl_design: RTLDesign,
    ) -> list[str]:
        """
        Generate adder logic.
        """

        inputs = rtl_design.requirement.inputs
        outputs = rtl_design.requirement.outputs

        if len(inputs) < 2 or not outputs:
            return []

        a = inputs[0].signal_name
        b = inputs[1].signal_name

        sum_output = outputs[0].signal_name

        carry_output = None

        for output in outputs:
            if output.signal_name.upper() == "CARRY":
                carry_output = output.signal_name
                break

        if carry_output is not None:
            return [
                f"    assign {{{carry_output}, {sum_output}}} "
                f"= {a} + {b};"
            ]

        return [
            f"    assign {sum_output} = {a} + {b};"
        ]

    def _generate_logic(
        self,
        rtl_design: RTLDesign,
    ) -> str:
        """
        Generate synthesizable combinational RTL logic.
        """

        print("\n========== RTL LOGIC DEBUG ==========")

        print(
            "Inputs:",
            [
                port.model_dump()
                for port in rtl_design.requirement.inputs
            ],
        )

        print(
            "Outputs:",
            [
                port.model_dump()
                for port in rtl_design.requirement.outputs
            ],
        )

        print(
            "Operations:",
            [
                operation.model_dump()
                for operation in rtl_design.requirement.operations
            ],
        )

        print("=====================================\n")

        inputs = rtl_design.requirement.inputs
        outputs = rtl_design.requirement.outputs
        operations = rtl_design.requirement.operations

        if len(inputs) < 2:
            return "    // Insufficient inputs for RTL generation"

        if not outputs:
            return "    // No outputs defined"

        # --------------------------------------------------
        # IMPORTANT:
        #
        # Detect a comparator from the interface itself.
        #
        # This prevents the generator from producing an empty
        # module when the LLM uses an unexpected operation name.
        # --------------------------------------------------

        output_names = {
            output.signal_name.upper()
            for output in outputs
        }

        has_comparator_interface = {
            "GT",
            "LT",
            "EQ",
        }.issubset(output_names)

        if has_comparator_interface:

            print(
                "Comparator interface detected."
            )

            comparator_logic = (
                self._generate_comparator_logic(
                    rtl_design
                )
            )

            if comparator_logic:

                print(
                    "\n========== GENERATED COMPARATOR LOGIC =========="
                )

                for statement in comparator_logic:
                    print(statement)

                print(
                    "=================================================\n"
                )

                return "\n\n".join(
                    comparator_logic
                )

        # --------------------------------------------------
        # No operations
        # --------------------------------------------------

        if not operations:
            return "    // No RTL operations defined"

        a = inputs[0].signal_name
        b = inputs[1].signal_name

        assign_statements: list[str] = []
        comb_statements: list[str] = []

        # --------------------------------------------------
        # Process operations
        # --------------------------------------------------

        for operation in operations:

            operation_name = (
                operation.operation_name
                .lower()
                .strip()
            )

            print(
                "Operation:",
                operation.model_dump(),
            )

            print(
                "Operation name:",
                operation.operation_name,
            )

            # --------------------------------------------------
            # Comparator
            # --------------------------------------------------

            if self._is_comparator(
                operation.operation_name,
                rtl_design,
            ):

                comparator_logic = (
                    self._generate_comparator_logic(
                        rtl_design
                    )
                )

                assign_statements.extend(
                    comparator_logic
                )

                continue

            # --------------------------------------------------
            # Adder
            # --------------------------------------------------

            if (
                "add" in operation_name
                or "addition" in operation_name
            ):

                assign_statements.extend(
                    self._generate_adder_logic(
                        rtl_design
                    )
                )

                continue

            # --------------------------------------------------
            # Generic operation handling
            # --------------------------------------------------

            destination = getattr(
                operation,
                "destination",
                None,
            )

            expression = getattr(
                operation,
                "expression",
                None,
            )

            operator = self._find_operator(
                operation.operation_name
            )

            if (
                not expression
                and operator is not None
            ):
                expression = (
                    f"{a} {operator} {b}"
                )

            if not expression:

                print(
                    "WARNING: Unsupported RTL "
                    f"operation: "
                    f"{operation.operation_name}"
                )

                continue

            if not destination:
                destination = (
                    outputs[0].signal_name
                )

            implementation_style = (
                getattr(
                    operation,
                    "implementation_style",
                    "assign",
                )
                .lower()
            )

            if implementation_style == "always_comb":

                comb_statements.append(
                    f"        "
                    f"{destination} = "
                    f"{expression};"
                )

            else:

                assign_statements.append(
                    "    "
                    + VerilogFormatter.format_assign(
                        destination,
                        expression,
                    )
                )

        # --------------------------------------------------
        # Combine logic
        # --------------------------------------------------

        logic: list[str] = []

        if assign_statements:
            logic.extend(
                assign_statements
            )

        if comb_statements:

            logic.append(
                VerilogFormatter.format_always_comb(
                    comb_statements
                )
            )

        if not logic:

            logic.append(
                "    // Unsupported operation"
            )

        print(
            "\n========== GENERATED LOGIC =========="
        )

        for statement in logic:
            print(statement)

        print(
            "=====================================\n"
        )

        return "\n\n".join(logic)

    def generate(
        self,
        rtl_design: RTLDesign,
    ) -> str:
        """
        Generate complete Verilog source.
        """

        use_parameter = False
        parameters = []

        # --------------------------------------------------
        # Parameters
        # --------------------------------------------------

        if rtl_design.parameters:

            use_parameter = True

            for name, value in (
                rtl_design.parameters.items()
            ):

                parameters.append(
                    VerilogFormatter.format_parameter(
                        name,
                        value,
                    )
                )

        elif rtl_design.requirement.inputs:

            width = (
                rtl_design
                .requirement
                .inputs[0]
                .signal_width
            )

            if width > 1:

                use_parameter = True

                parameters.append(
                    VerilogFormatter.format_parameter(
                        "WIDTH",
                        width,
                    )
                )

        # --------------------------------------------------
        # Module header
        # --------------------------------------------------

        module_header = (
            VerilogFormatter.format_module_header(
                rtl_design.requirement.module_name,
                parameters,
            )
        )

        # --------------------------------------------------
        # Ports
        # --------------------------------------------------

        port_declarations = (
            self._generate_port_declarations(
                rtl_design,
                use_parameter=use_parameter,
            )
        )

        # --------------------------------------------------
        # Internal signals
        # --------------------------------------------------

        internal_signals = (
            self._generate_internal_signals(
                rtl_design,
                use_parameter=use_parameter,
            )
        )

        # --------------------------------------------------
        # Logic
        # --------------------------------------------------

        rtl_logic = self._generate_logic(
            rtl_design
        )

        print(
            "\n========== RTL SOURCE =========="
        )

        print(rtl_logic)

        print(
            "================================\n"
        )

        # --------------------------------------------------
        # Complete Verilog
        # --------------------------------------------------

        generated_code = (
            f"{module_header} (\n"
            f"{port_declarations}\n"
            f");\n\n"
            f"{internal_signals}\n\n"
            f"{rtl_logic}\n\n"
            f"endmodule\n"
        )

        print(
            "\n========== COMPLETE GENERATED "
            "VERILOG ==========\n"
        )

        print(generated_code)

        print(
            "\n================================================\n"
        )

        return generated_code