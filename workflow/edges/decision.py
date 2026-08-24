"""
Conditional routing logic for the VeriCore AI LangGraph workflow.
"""

from __future__ import annotations

from workflow.state.design_state import DesignState


def simulation_decision(
    state: DesignState,
) -> str:
    """
    Decide what to do after RTL simulation.

    Returns:

        "synthesis"
            RTL simulation succeeded.

        "debug"
            RTL simulation failed and retries remain.

        "documentation"
            Retries are exhausted.
    """

    simulation_result = state.get(
        "simulation_result"
    )

    if simulation_result is None:
        return "debug"

    if simulation_result.simulation_success:
        return "synthesis"

    debug_iteration = state.get(
        "debug_iteration",
        0,
    )

    max_debug_iterations = state.get(
        "max_debug_iterations",
        3,
    )

    if debug_iteration < max_debug_iterations:
        return "debug"

    return "documentation"


def synthesis_decision(
    state: DesignState,
) -> str:
    """
    Decide what to do after RTL synthesis.

    Returns:

        "post_synthesis_simulation"
            Synthesis succeeded.

        "debug"
            Synthesis failed and retries remain.

        "documentation"
            Retries are exhausted.
    """

    synthesis_result = state.get(
        "synthesis_result"
    )

    if synthesis_result is None:
        return "debug"

    if synthesis_result.synthesis_success:
        return "post_synthesis_simulation"

    debug_iteration = state.get(
        "debug_iteration",
        0,
    )

    max_debug_iterations = state.get(
        "max_debug_iterations",
        3,
    )

    if debug_iteration < max_debug_iterations:
        return "debug"

    return "documentation"


def post_synthesis_decision(
    state: DesignState,
) -> str:
    """
    Decide what to do after post-synthesis simulation.

    Returns:

        "documentation"
            Post-synthesis simulation succeeded.

        "debug"
            Post-synthesis simulation failed and
            retries remain.

        "documentation"
            Retries are exhausted.
    """

    result = state.get(
        "post_synthesis_simulation_result"
    )

    if result is None:
        return "debug"

    if result.simulation_success:
        return "documentation"

    debug_iteration = state.get(
        "debug_iteration",
        0,
    )

    max_debug_iterations = state.get(
        "max_debug_iterations",
        3,
    )

    if debug_iteration < max_debug_iterations:
        return "debug"

    return "documentation"