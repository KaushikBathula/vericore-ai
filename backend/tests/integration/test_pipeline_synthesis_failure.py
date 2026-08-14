from pathlib import Path
from unittest.mock import MagicMock

from backend.app.services.pipeline_service import PipelineService


def test_pipeline_retries_when_synthesis_fails(tmp_path: Path):
    service = PipelineService()

    # ----------------------------------------
    # Mock Requirement Agent
    # ----------------------------------------

    requirement_spec = MagicMock()
    requirement_spec.module_name = "alu"

    service.requirement_agent.execute = MagicMock(
        return_value=requirement_spec
    )

    # ----------------------------------------
    # Mock RTL Agent
    # ----------------------------------------

    rtl_design = MagicMock()

    service.rtl_agent.execute = MagicMock(
        return_value=rtl_design
    )

    # ----------------------------------------
    # Mock Verification Agent
    # ----------------------------------------

    verification_plan = MagicMock()

    service.verification_agent.execute = MagicMock(
        return_value=verification_plan
    )

    # ----------------------------------------
    # Mock Code Generation
    # ----------------------------------------

    service.code_generation_service.generate = MagicMock(
        return_value=(
            "module alu; endmodule",
            "module tb_alu; endmodule",
        )
    )

    # ----------------------------------------
    # Mock Simulation
    # ----------------------------------------

    simulation_result = MagicMock()
    simulation_result.simulation_success = True

    service.simulation_service.simulate = MagicMock(
        return_value=simulation_result
    )

    # ----------------------------------------
    # Mock Synthesis
    # ----------------------------------------

    failed_synthesis = MagicMock()
    failed_synthesis.synthesis_success = False

    successful_synthesis = MagicMock()
    successful_synthesis.synthesis_success = True

    # Create a real synthesized netlist for the
    # successful synthesis attempt.
    netlist_path = (
        tmp_path
        / "synthesis"
        / "netlist.v"
    )

    netlist_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    netlist_path.write_text(
        "module alu; endmodule",
        encoding="utf-8",
    )

    successful_synthesis.netlist_path = str(
        netlist_path
    )

    service.synthesis_service.synthesize = MagicMock(
        side_effect=[
            failed_synthesis,
            successful_synthesis,
        ]
    )

    # ----------------------------------------
    # Mock Debug / Repair
    # ----------------------------------------

    debug_report = MagicMock()

    service.debug_agent.execute = MagicMock(
        return_value=debug_report
    )

    service.rtl_repair_service.repair = MagicMock(
        return_value=rtl_design
    )

    # ----------------------------------------
    # Mock Documentation
    # ----------------------------------------

    service.documentation_service.generate = MagicMock()

    fake_report = MagicMock()

    service._build_report = MagicMock(
        return_value=fake_report
    )

    # ----------------------------------------
    # Execute Pipeline
    # ----------------------------------------

    report = service.execute(
        requirement_text="Design an ALU",
        output_directory=tmp_path,
    )

    # ----------------------------------------
    # Final Report
    # ----------------------------------------

    assert report is fake_report

    # ----------------------------------------
    # Synthesis
    # ----------------------------------------

    # First synthesis fails.
    # Second synthesis succeeds.
    assert (
        service.synthesis_service.synthesize.call_count
        == 2
    )

    # ----------------------------------------
    # Debug
    # ----------------------------------------

    # Failed synthesis must trigger debugging.
    service.debug_agent.execute.assert_called_once()

    # ----------------------------------------
    # RTL Repair
    # ----------------------------------------

    # Failed synthesis must trigger RTL repair.
    service.rtl_repair_service.repair.assert_called_once()

    # ----------------------------------------
    # Code Generation
    # ----------------------------------------

    # Initial generation + generation after
    # synthesis failure.
    assert (
        service.code_generation_service.generate.call_count
        == 2
    )

    # ----------------------------------------
    # Simulation
    # ----------------------------------------

    # Simulation 1:
    #   Original RTL
    #
    # Simulation 2:
    #   RTL after synthesis failure repair
    #
    # Simulation 3:
    #   Successful synthesized netlist
    assert (
        service.simulation_service.simulate.call_count
        == 3
    )

    simulation_calls = (
        service.simulation_service.simulate.call_args_list
    )

    # Final simulation must use the synthesized netlist.
    assert (
        simulation_calls[-1].kwargs["rtl_file"]
        == netlist_path
    )

    # ----------------------------------------
    # Documentation
    # ----------------------------------------

    service.documentation_service.generate.assert_called_once()