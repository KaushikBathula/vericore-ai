"""
Unit tests for SimulationRunner.
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from backend.app.services.simulation_runner import SimulationRunner


def test_missing_rtl_file(tmp_path: Path) -> None:
    """Runner should raise if RTL file is missing."""

    runner = SimulationRunner()

    tb = tmp_path / "tb.v"
    tb.write_text("// tb")

    with pytest.raises(FileNotFoundError):
        runner.run(
            rtl_file=tmp_path / "rtl.v",
            testbench_file=tb,
            output_file=tmp_path / "simulation.out",
            working_directory=tmp_path,
        )


def test_missing_testbench_file(tmp_path: Path) -> None:
    """Runner should raise if testbench is missing."""

    runner = SimulationRunner()

    rtl = tmp_path / "rtl.v"
    rtl.write_text("// rtl")

    with pytest.raises(FileNotFoundError):
        runner.run(
            rtl_file=rtl,
            testbench_file=tmp_path / "tb.v",
            output_file=tmp_path / "simulation.out",
            working_directory=tmp_path,
        )


@patch("backend.app.services.simulation_runner.subprocess.run")
def test_compile_failure(
    mock_run: Mock,
    tmp_path: Path,
) -> None:
    """Compilation failure should return a failed SimulationResult."""

    rtl = tmp_path / "rtl.v"
    tb = tmp_path / "tb.v"

    rtl.write_text("// rtl")
    tb.write_text("// tb")

    mock_run.return_value = subprocess.CompletedProcess(
        args=[],
        returncode=1,
        stdout="",
        stderr="compile error",
    )

    runner = SimulationRunner()

    result = runner.run(
        rtl_file=rtl,
        testbench_file=tb,
        output_file=tmp_path / "simulation.out",
        working_directory=tmp_path,
    )

    assert result.compile_success is False
    assert result.simulation_success is False
    assert "compile error" in result.stderr


@patch("backend.app.services.simulation_runner.subprocess.run")
def test_successful_simulation(
    mock_run: Mock,
    tmp_path: Path,
) -> None:
    """Successful compilation and simulation."""

    rtl = tmp_path / "rtl.v"
    tb = tmp_path / "tb.v"

    rtl.write_text("// rtl")
    tb.write_text("// tb")

    compile_process = subprocess.CompletedProcess(
        args=[],
        returncode=0,
        stdout="compiled",
        stderr="",
    )

    simulation_process = subprocess.CompletedProcess(
        args=[],
        returncode=0,
        stdout="simulation ok",
        stderr="",
    )

    mock_run.side_effect = [
        compile_process,
        simulation_process,
    ]

    runner = SimulationRunner()

    result = runner.run(
        rtl_file=rtl,
        testbench_file=tb,
        output_file=tmp_path / "simulation.out",
        working_directory=tmp_path,
    )

    assert result.compile_success is True
    assert result.simulation_success is True


@patch("backend.app.services.simulation_runner.subprocess.run")
def test_waveform_detection(
    mock_run: Mock,
    tmp_path: Path,
) -> None:
    """Waveform path should be detected."""

    rtl = tmp_path / "rtl.v"
    tb = tmp_path / "tb.v"

    rtl.write_text("// rtl")
    tb.write_text("// tb")

    waveform = tmp_path / "tb_example.vcd"
    waveform.write_text("dummy")

    compile_process = subprocess.CompletedProcess(
        args=[],
        returncode=0,
        stdout="compiled",
        stderr="",
    )

    simulation_process = subprocess.CompletedProcess(
        args=[],
        returncode=0,
        stdout="simulation ok",
        stderr="",
    )

    mock_run.side_effect = [
        compile_process,
        simulation_process,
    ]

    runner = SimulationRunner()

    result = runner.run(
        rtl_file=rtl,
        testbench_file=tb,
        output_file=tmp_path / "simulation.out",
        working_directory=tmp_path,
    )

    assert result.waveform_path is not None
    assert result.waveform_path.endswith(".vcd")