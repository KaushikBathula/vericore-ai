"""
Utility functions for formatting Verilog HDL constructs.
"""

from backend.app.schemas.port import Port
from backend.app.schemas.signal import Signal


class VerilogFormatter:
    """
    Handles formatting of Verilog HDL constructs.
    """

    @staticmethod
    def format_parameter(name: str, value: str | int) -> str:
        return f"parameter {name} = {value}"

    @staticmethod
    def format_port(
        port: Port,
        use_parameter: bool = False,
        parameter_name: str = "WIDTH",
    ) -> str:

        if use_parameter and port.signal_width > 1:
            width = f"[{parameter_name}-1:0] "
        else:
            width = (
                f"[{port.signal_width - 1}:0] "
                if port.signal_width > 1
                else ""
            )

        return (
            f"{port.direction} "
            f"{width}"
            f"{port.signal_name}"
        )

    @staticmethod
    def format_signal(
        signal: Signal,
        use_parameter: bool = False,
        parameter_name: str = "WIDTH",
    ) -> str:

        signal_type = (
            signal.signal_type.value
            if hasattr(signal.signal_type, "value")
            else str(signal.signal_type)
        )

        if use_parameter and signal.signal_width > 1:
            width = f"[{parameter_name}-1:0] "
        else:
            width = (
                f"[{signal.signal_width - 1}:0] "
                if signal.signal_width > 1
                else ""
            )

        signed = "signed " if signal.signed else ""

        declaration = (
            f"{signal_type} "
            f"{signed}"
            f"{width}"
            f"{signal.signal_name}"
        )

        if signal.default_value is not None:
            declaration += f" = {signal.default_value}"

        return declaration + ";"

    @staticmethod
    def format_assign(destination: str, expression: str) -> str:
        return f"assign {destination} = {expression};"

    @staticmethod
    def format_always_comb(statements: list[str]) -> str:
        """
        Format an always_comb block.
        """

        body = "\n".join(
            f"    {statement}"
            for statement in statements
        )

        return (
            "always_comb begin\n"
            f"{body}\n"
            "end"
        )

    @staticmethod
    def format_module_header(
        module_name: str,
        parameters: list[str] | None = None,
    ) -> str:

        if not parameters:
            return f"module {module_name}"

        parameter_block = ",\n    ".join(parameters)

        return (
            f"module {module_name} #(\n"
            f"    {parameter_block}\n"
            f")"
        )

    @staticmethod
    def indent(text: str, level: int = 1) -> str:

        prefix = "    " * level

        return "\n".join(
            prefix + line if line else ""
            for line in text.splitlines()
        )