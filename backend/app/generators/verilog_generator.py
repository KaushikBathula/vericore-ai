"""
Verilog HDL generator.
"""

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

    def _find_operator(self, operation_name: str) -> str | None:
        """
        Determine the Verilog operator corresponding to an operation name.
        Supports multiple naming conventions returned by different LLMs.
        """

        name = operation_name.lower()

        if "add" in name:
            return "+"

        if "sub" in name:
            return "-"

        if "xor" in name:
            return "^"

        if "and" in name:
            return "&"

        # Check OR after XOR so "xor" isn't matched as "or"
        if name == "or" or name.endswith("_or") or " or " in name:
            return "|"

        return None

    def _generate_logic(self, rtl_design: RTLDesign) -> str:
        print("\n========== RTL LOGIC DEBUG ==========")
        print("Inputs :", rtl_design.requirement.inputs)
        print("Outputs:", rtl_design.requirement.outputs)
        print("Operations:", rtl_design.requirement.operations)
        print("=====================================\n")
        """
        Generate RTL logic.
        """
        
        if (
            len(rtl_design.requirement.inputs) < 2
            or len(rtl_design.requirement.outputs) < 1
            or not rtl_design.requirement.operations
        ):
            return "    // No RTL logic generated"

        a = rtl_design.requirement.inputs[0].signal_name
        b = rtl_design.requirement.inputs[1].signal_name
        out = rtl_design.requirement.outputs[0].signal_name
        carry = (
            rtl_design.requirement.outputs[1].signal_name
            if len(rtl_design.requirement.outputs) > 1
            else None
        )
        assign_statements = []
        comb_statements = []

        for operation in rtl_design.requirement.operations:
            print("Operation:", operation)
            print("Operation name:", operation.operation_name)
            print("Mapped operator:", self._find_operator(operation.operation_name))

            # Backward-compatible destination
            destination = getattr(
                operation,
                "destination",
                None,
            ) or out

            # Backward-compatible expression
            expression = getattr(
                operation,
                "expression",
                None,
            )

            # Fallback to operator mapping
            if not expression:

                operator = self._find_operator(
                    operation.operation_name
                )

                if operator is None:
                    continue

                expression = f"{a} {operator} {b}"
            # Special handling for adders
            if "add" in operation.operation_name.lower():

                sum_signal = rtl_design.requirement.outputs[0].signal_name
                carry_signal = None

            for port in rtl_design.requirement.outputs:
                    if port.signal_name.upper() == "CARRY":
                        carry_signal = port.signal_name
                        break

            if carry_signal:
                    assign_statements.append(
                        f"    assign {{{carry_signal}, {sum_signal}}} = {a} + {b};"
                    )
            else:
                    assign_statements.append(
                        f"    assign {sum_signal} = {a} + {b};"
                    )

            continue
            # Backward-compatible implementation style
            implementation_style = getattr(
                operation,
                "implementation_style",
                "assign",
            ).lower()

            if implementation_style == "always_comb":

                comb_statements.append(
                    f"{destination} = {expression};"
                )

            else:

                assign_statements.append(
                    "    "
                    + VerilogFormatter.format_assign(
                        destination,
                        expression,
                    )
                )

        logic = []

        if assign_statements:
            logic.extend(assign_statements)

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
        print("\n========== GENERATED LOGIC ==========")
        print(logic)
        print("=====================================\n")
        return "\n\n".join(logic)

    def generate(self, rtl_design: RTLDesign) -> str:

        use_parameter = False

        parameters = []

        if rtl_design.parameters:

            use_parameter = True

            for name, value in rtl_design.parameters.items():

                parameters.append(
                    VerilogFormatter.format_parameter(
                        name,
                        value,
                    )
                )

        elif rtl_design.requirement.inputs:

            width = rtl_design.requirement.inputs[
                0
            ].signal_width

            if width > 1:

                use_parameter = True

                parameters.append(
                    VerilogFormatter.format_parameter(
                        "WIDTH",
                        width,
                    )
                )

        module_header = VerilogFormatter.format_module_header(
            rtl_design.requirement.module_name,
            parameters,
        )

        port_declarations = self._generate_port_declarations(
            rtl_design,
            use_parameter=use_parameter,
        )

        internal_signals = self._generate_internal_signals(
            rtl_design,
            use_parameter=use_parameter,
        )

        rtl_logic = self._generate_logic(
            rtl_design
        )

        print("\n========== RTL SOURCE ==========")
        print(rtl_logic)
        print("================================\n")

        generated_code = (
            f"{module_header} (\n"
            f"{port_declarations}\n"
            f");\n\n"
            f"{internal_signals}\n\n"
            f"{rtl_logic}\n\n"
            f"endmodule\n"
        )

        print("\n========== COMPLETE GENERATED VERILOG ==========\n")
        print(generated_code)
        print("\n================================================\n")

        return generated_code