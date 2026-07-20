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

        name = operation_name.lower()

        mapping = {
            "addition": "+",
            "add": "+",
            "subtraction": "-",
            "subtract": "-",
            "sub": "-",
            "and": "&",
            "or": "|",
            "xor": "^",
        }

        return mapping.get(name)

    def _generate_logic(self, rtl_design: RTLDesign) -> str:
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

        assign_statements = []
        comb_statements = []

        for operation in rtl_design.requirement.operations:

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

        return (
            f"{module_header} (\n"
            f"{port_declarations}\n"
            f");\n\n"
            f"{internal_signals}\n\n"
            f"{rtl_logic}\n\n"
            f"endmodule\n"
        )