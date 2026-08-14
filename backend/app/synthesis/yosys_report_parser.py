"""
Yosys Report Parser.

Parses synthesis output produced by Yosys.
"""

from __future__ import annotations

import re


class YosysReportParser:
    """
    Parses Yosys synthesis output.
    """

    @staticmethod
    def parse_cell_count(report: str) -> int | None:
        """
        Extract the synthesized cell count from a Yosys report.

        Supports both common Yosys statistics formats:

            Number of cells: 4

        and:

            4 cells
            4   $_AND_

        Parameters
        ----------
        report:
            Raw synthesis output.

        Returns
        -------
        int | None
            Total synthesized cell count if found.
        """

        # Standard Yosys statistics summary format.
        match = re.search(
            r"^\s*Number of cells:\s*(\d+)\s*$",
            report,
            flags=re.MULTILINE,
        )

        if match:
            return int(match.group(1))

        # Yosys module statistics format.
        match = re.search(
            r"^\s*(\d+)\s+cells\s*$",
            report,
            flags=re.MULTILINE,
        )

        if match:
            return int(match.group(1))

        return None

    @staticmethod
    def parse_warning_count(report: str) -> int:
        """
        Count warnings in a synthesis report.

        Parameters
        ----------
        report:
            Raw synthesis output.

        Returns
        -------
        int
            Number of warning occurrences.
        """

        return len(
            re.findall(
                r"warning",
                report,
                flags=re.IGNORECASE,
            )
        )