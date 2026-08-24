"""
Shared LangGraph state for the VeriCore AI design workflow.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, TypedDict


class DesignState(TypedDict, total=False):
    """
    Shared state carried through the complete VeriCore AI workflow.
    """

    # ---------------------------------------------------------
    # Request
    # ---------------------------------------------------------

    requirement_text: str
    output_directory: Path

    # ---------------------------------------------------------
    # Requirement analysis
    # ---------------------------------------------------------

    requirement_spec: Any

    # ---------------------------------------------------------
    # RTL design
    # ---------------------------------------------------------

    rtl_design: Any
    rtl_source: str
    testbench_source: str

    # ---------------------------------------------------------
    # Verification
    # ---------------------------------------------------------

    verification_plan: Any

    # ---------------------------------------------------------
    # Simulation
    # ---------------------------------------------------------

    simulation_result: Any
    post_synthesis_simulation_result: Any

    # ---------------------------------------------------------
    # Synthesis
    # ---------------------------------------------------------

    synthesis_result: Any

    # ---------------------------------------------------------
    # Debug / repair
    # ---------------------------------------------------------

    debug_report: Any
    debug_iteration: int
    max_debug_iterations: int

    # ---------------------------------------------------------
    # Project artifacts
    # ---------------------------------------------------------

    project_paths: dict[str, Path]
    rtl_file: Path | None
    testbench_file: Path | None
    netlist_file: Path | None

    # ---------------------------------------------------------
    # Workflow control
    # ---------------------------------------------------------

    current_stage: str
    active_agent: str
    workflow_status: str
    error: str | None

    # ---------------------------------------------------------
    # Final result
    # ---------------------------------------------------------

    report: Any