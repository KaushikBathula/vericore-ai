"""
Unit tests for DebugService.
"""

from __future__ import annotations

from unittest.mock import patch

from backend.app.schemas.debug_report import DebugReport
from backend.app.schemas.simulation_result import SimulationResult
from backend.app.services.debug_service import DebugService


@patch("backend.app.services.debug_service.DebugAgent.execute")
def test_debug_service_analyze(mock_execute) -> None:
    """
    DebugService should delegate analysis to DebugAgent and
    return the resulting DebugReport.
    """

    expected_report = DebugReport(
        success=True,
        summary="No issues detected.",
        issues=[],
        compiler_output="",
        simulation_output="",
        recommendations=[],
    )

    mock_execute.return_value = expected_report

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

    service = DebugService()

    report = service.analyze(simulation_result)

    mock_execute.assert_called_once_with(simulation_result)
    assert report == expected_report