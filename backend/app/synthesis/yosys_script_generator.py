"""
Yosys Script Generator.

Generates Yosys synthesis scripts.
"""

from __future__ import annotations

from pathlib import Path


class YosysScriptGenerator:
    """
    Generates a Yosys synthesis script.
    """

    def generate(
        self,
        rtl_file: Path,
        top_module: str,
        netlist_file: Path,
    ) -> str:
        """
        Generate a Yosys synthesis script.

        Parameters
        ----------
        rtl_file:
            RTL Verilog file.

        top_module:
            Top-level module name.

        netlist_file:
            Output synthesized netlist.

        Returns
        -------
        str
            Complete Yosys script.
        """

        return "\n".join(
            [
                f"read_verilog {rtl_file}",
                f"hierarchy -check -top {top_module}",
                "proc",
                "opt",
                "fsm",
                "memory",
                "opt",
                "techmap",
                "opt",
                "stat",
                f"write_verilog {netlist_file}",
            ]
        )
