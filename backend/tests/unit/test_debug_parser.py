"""
Unit tests for DebugParser.
"""

from __future__ import annotations

from backend.app.core.parsers.debug_parser import DebugParser


def test_parse_no_errors() -> None:
    """
    Parser should report success when no compiler errors exist.
    """

    report = DebugParser.parse(
        compiler_output="",
        simulation_output="",
    )

    assert report.success is True
    assert report.summary == "No issues detected."
    assert len(report.issues) == 0
    assert report.recommendations == []


def test_parse_single_error() -> None:
    """
    Parser should detect a single compiler error.
    """

    report = DebugParser.parse(
        compiler_output="alu.v:27: syntax error",
        simulation_output="",
    )

    assert report.success is False
    assert len(report.issues) == 1

    issue = report.issues[0]

    assert issue.file == "alu.v"
    assert issue.line == 27
    assert issue.category == "Compilation Error"
    assert issue.severity == "High"
    assert "syntax error" in issue.message

    assert len(report.recommendations) == 1
    assert "Resolve" in report.recommendations[0]


def test_parse_multiple_errors() -> None:
    """
    Parser should detect multiple compiler errors.
    """

    compiler_output = (
        "alu.v:12: syntax error\n"
        "alu.v:28: invalid module instantiation"
    )

    report = DebugParser.parse(
        compiler_output=compiler_output,
        simulation_output="",
    )

    assert report.success is False
    assert len(report.issues) == 2

    assert report.issues[0].line == 12
    assert report.issues[1].line == 28


def test_parse_preserves_outputs() -> None:
    """
    Parser should preserve compiler and simulation outputs.
    """

    compiler_output = "alu.v:10: syntax error"
    simulation_output = "Simulation stopped."

    report = DebugParser.parse(
        compiler_output=compiler_output,
        simulation_output=simulation_output,
    )

    assert report.compiler_output == compiler_output
    assert report.simulation_output == simulation_output