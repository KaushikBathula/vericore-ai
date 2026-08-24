"""
LangGraph workflow for the VeriCore AI design pipeline.
"""

from __future__ import annotations

from langgraph.graph import END, START, StateGraph

from workflow.edges.decision import (
    post_synthesis_decision,
    simulation_decision,
    synthesis_decision,
)

from workflow.nodes.debug_node import debug_node
from workflow.nodes.documentation_node import documentation_node
from workflow.nodes.post_synthesis_simulation_node import (
    post_synthesis_simulation_node,
)
from workflow.nodes.requirement_node import requirement_node
from workflow.nodes.rtl_node import rtl_node
from workflow.nodes.simulation_node import simulation_node
from workflow.nodes.synthesis_node import synthesis_node
from workflow.nodes.verification_node import verification_node

from workflow.state.design_state import DesignState


def build_design_graph():
    """
    Build and compile the complete VeriCore AI LangGraph workflow.

    Workflow:

        START
          ↓
        Requirement
          ↓
        RTL
          ↓
        Verification
          ↓
        Simulation
          ↓
        ┌─────────────────────┐
        │ simulation_decision │
        └─────────────────────┘
             ↓          ↓
          debug      synthesis
             ↓          ↓
            RTL      synthesis_decision
                         ↓
                    ┌────┴────┐
                    ↓         ↓
          post-synthesis     debug
             simulation       ↓
                    ↓         RTL
                    ↓
             post_synthesis_decision
                    ↓
             Documentation
                    ↓
                   END
    """

    workflow = StateGraph(DesignState)

    # =========================================================
    # REGISTER NODES
    # =========================================================

    workflow.add_node(
        "requirement",
        requirement_node,
    )

    workflow.add_node(
        "rtl",
        rtl_node,
    )

    workflow.add_node(
        "verification",
        verification_node,
    )

    workflow.add_node(
        "simulation",
        simulation_node,
    )

    workflow.add_node(
        "debug",
        debug_node,
    )

    workflow.add_node(
        "synthesis",
        synthesis_node,
    )

    workflow.add_node(
        "post_synthesis_simulation",
        post_synthesis_simulation_node,
    )

    workflow.add_node(
        "documentation",
        documentation_node,
    )

    # =========================================================
    # MAIN FORWARD PATH
    # =========================================================

    workflow.add_edge(
        START,
        "requirement",
    )

    workflow.add_edge(
        "requirement",
        "rtl",
    )

    workflow.add_edge(
        "rtl",
        "verification",
    )

    workflow.add_edge(
        "verification",
        "simulation",
    )

    # =========================================================
    # RTL SIMULATION DECISION
    # =========================================================

    workflow.add_conditional_edges(
        "simulation",
        simulation_decision,
        {
            "synthesis": "synthesis",
            "debug": "debug",
            "documentation": "documentation",
        },
    )

    # =========================================================
    # DEBUG → RTL
    #
    # After repair, the workflow automatically continues:
    #
    # RTL → Verification → Simulation
    # =========================================================

    workflow.add_edge(
        "debug",
        "rtl",
    )

    # =========================================================
    # SYNTHESIS DECISION
    # =========================================================

    workflow.add_conditional_edges(
        "synthesis",
        synthesis_decision,
        {
            "post_synthesis_simulation": (
                "post_synthesis_simulation"
            ),
            "debug": "debug",
            "documentation": "documentation",
        },
    )

    # =========================================================
    # POST-SYNTHESIS SIMULATION DECISION
    # =========================================================

    workflow.add_conditional_edges(
        "post_synthesis_simulation",
        post_synthesis_decision,
        {
            "documentation": "documentation",
        },
    )

    # =========================================================
    # DOCUMENTATION → END
    # =========================================================

    workflow.add_edge(
        "documentation",
        END,
    )

    return workflow.compile()


# =============================================================
# COMPILED WORKFLOW INSTANCE
# =============================================================

design_graph = build_design_graph()