"""
Debug Parser.

Converts compiler and simulator output into a validated
DebugReport object.
"""

from __future__ import annotations

import re

from backend.app.schemas.debug_issue import DebugIssue
from backend.app.schemas.debug_report import DebugReport


class DebugParser:
    """
    Converts compiler/simulator output into a DebugReport.
    """

    _ERROR_PATTERN = re.compile(
        r"(?P<file>.+?):(?P<line>\d+):\s*(?P<message>.+)"
    )

    @staticmethod
    def parse(
        compiler_output: str,
        simulation_output: str = "",
    ) -> DebugReport:
        """
        Parse compiler and simulation output.
        """

        issues: list[DebugIssue] = []

        for line in compiler_output.splitlines():

            match = DebugParser._ERROR_PATTERN.match(line)

            if match:

                issues.append(
                    DebugIssue(
                        category="Compilation Error",
                        severity="High",
                        message=match.group("message"),
                        file=match.group("file"),
                        line=int(match.group("line")),
                        suggestion=(
                            "Review the reported source line "
                            "and correct the RTL."
                        ),
                    )
                )

        success = len(issues) == 0

        recommendations: list[str] = []

        if not success:
            recommendations.append(
                "Resolve all compilation errors before rerunning simulation."
            )

        return DebugReport(
            success=success,
            summary=(
                "No issues detected."
                if success
                else f"{len(issues)} issue(s) detected."
            ),
            issues=issues,
            compiler_output=compiler_output,
            simulation_output=simulation_output,
            recommendations=recommendations,
        )