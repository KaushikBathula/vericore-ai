"""
Documentation Service.

Coordinates generation and storage of project documentation.
"""

from __future__ import annotations

from pathlib import Path

from backend.app.documentation.documentation_generator import (
    DocumentationGenerator,
)
from backend.app.schemas.documentation_report import (
    DocumentationReport,
)


class DocumentationService:
    """
    Coordinates documentation generation.

    This service delegates Markdown generation to the
    DocumentationGenerator and manages saving the report.
    """

    def __init__(self) -> None:
        self.generator = DocumentationGenerator()

    def generate(
        self,
        report: DocumentationReport,
        output_directory: Path,
    ) -> Path:
        """
        Generate and save project documentation.

        Parameters
        ----------
        report:
            Complete documentation report.

        output_directory:
            Directory where the report will be stored.

        Returns
        -------
        Path
            Path to the generated Markdown report.
        """

        output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        markdown = self.generator.generate(
            report,
        )

        report_path = output_directory / "report.md"

        report_path.write_text(
            markdown,
            encoding="utf-8",
        )

        return report_path