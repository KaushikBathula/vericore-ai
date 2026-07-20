"""
Unit tests for DebugAgent.
"""

from __future__ import annotations

from backend.app.agents.debug_agent import DebugAgent
from backend.app.schemas.simulation_result import SimulationResult


def test_debug_agent_success() -> None:
    """
    DebugAgent should return a successful DebugReport when
    no compiler errors are present.
    """

    simulation_result = SimulationResult(
        compile_success=True,
        simulation_success=True,
        stdout="",
        stderr="",
        execution_time=0.1,
        waveform_path=None,
        compiler_output="",
        simulation_output="",
    )

    agent = DebugAgent()

    report = agent.execute(simulation_result)

    assert report.success is True
    assert len(report.issues) == 0
    assert report.summary == "No issues detected."


def test_debug_agent_compilation_error() -> None:
    """
    DebugAgent should detect compiler errors.
    """

    simulation_result = SimulationResult(
        compile_success=False,
        simulation_success=False,
        stdout="",
        stderr="syntax error",
        execution_time=0.2,
        waveform_path=None,
        compiler_output="alu.v:17: syntax error",
        simulation_output="",
    )

    agent = DebugAgent()

    report = agent.execute(simulation_result)

    assert report.success is False
    assert len(report.issues) == 1

    issue = report.issues[0]

    assert issue.file == "alu.v"
    assert issue.line == 17
    assert "syntax error" in issue.message