"""
Documentation Generator.

Generates a Markdown engineering report summarizing the
complete VeriCore AI design flow.
"""

from __future__ import annotations

from backend.app.schemas.documentation_report import (
    DocumentationReport,
)


class DocumentationGenerator:
    """
    Generates project documentation.
    """

    def generate(
        self,
        report: DocumentationReport,
    ) -> str:
        """
        Generate a Markdown report.

        Parameters
        ----------
        report:
            Complete documentation report.

        Returns
        -------
        str
            Markdown document.
        """

        lines: list[str] = []

        # -------------------------------------------------
        # Title
        # -------------------------------------------------

        lines.append("# VeriCore AI Report")
        lines.append("")

        # -------------------------------------------------
        # Requirement
        # -------------------------------------------------

        lines.append("## Original Requirement")
        lines.append("")
        lines.append(report.requirement_text)
        lines.append("")

        # -------------------------------------------------
        # Requirement Specification
        # -------------------------------------------------

        lines.append("## Requirement Specification")
        lines.append("")
        lines.append(
            f"- Module: {report.requirement_spec.module_name}"
        )
        lines.append(
            f"- Description: {report.requirement_spec.description}"
        )
        lines.append("")

        # -------------------------------------------------
        # RTL
        # -------------------------------------------------

        lines.append("## RTL Design")
        lines.append("")

        lines.append("```verilog")
        lines.append(report.rtl_source)
        lines.append("```")
        lines.append("")

        # -------------------------------------------------
        # Testbench
        # -------------------------------------------------

        lines.append("## Testbench")
        lines.append("")

        lines.append("```verilog")
        lines.append(report.testbench_source)
        lines.append("```")
        lines.append("")

        # -------------------------------------------------
        # Simulation
        # -------------------------------------------------

        if report.simulation_result:

            sim = report.simulation_result

            lines.append("## Simulation")
            lines.append("")
            lines.append(
                f"- Compile Success: {sim.compile_success}"
            )
            lines.append(
                f"- Simulation Success: {sim.simulation_success}"
            )
            lines.append(
                f"- Execution Time: {sim.execution_time:.3f} s"
            )

            if sim.waveform_path:
                lines.append(
                    f"- Waveform: {sim.waveform_path}"
                )

            lines.append("")

        # -------------------------------------------------
        # Synthesis
        # -------------------------------------------------

        if report.synthesis_result:

            syn = report.synthesis_result

            lines.append("## Synthesis")
            lines.append("")
            lines.append(
                f"- Success: {syn.synthesis_success}"
            )
            lines.append(
                f"- Warnings: {syn.warning_count}"
            )

            if syn.cell_count is not None:
                lines.append(
                    f"- Cells: {syn.cell_count}"
                )

            lines.append("")

        # -------------------------------------------------
        # Debug
        # -------------------------------------------------

        if report.debug_report:

            lines.append("## Debug Report")
            lines.append("")
            lines.append(
                report.debug_report.summary
            )
            lines.append("")

        # -------------------------------------------------
        # Generated Files
        # -------------------------------------------------

        if report.generated_files:

            lines.append("## Generated Files")
            lines.append("")

            for name, path in report.generated_files.items():
                lines.append(
                    f"- **{name}**: `{path}`"
                )

            lines.append("")

        # -------------------------------------------------
        # Status
        # -------------------------------------------------

        lines.append("## Pipeline Status")
        lines.append("")
        lines.append(
            f"**Success:** {report.success}"
        )
        lines.append("")
        lines.append(
            f"Generated: {report.generated_at.isoformat()}"
        )

        return "\n".join(lines)