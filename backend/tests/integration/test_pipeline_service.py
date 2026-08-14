from pathlib import Path
from unittest.mock import MagicMock

from backend.app.services.pipeline_service import PipelineService


def test_pipeline_service_execute(tmp_path: Path):
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

    synthesis_result = MagicMock()
    synthesis_result.synthesis_success = True

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

    synthesis_result.netlist_path = str(
        netlist_path
    )

    service.synthesis_service.synthesize = MagicMock(
        return_value=synthesis_result
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
    # Verify Final Report
    # ----------------------------------------

    assert report is fake_report

    service._build_report.assert_called_once()

    # ----------------------------------------
    # Verify Requirement Agent
    # ----------------------------------------

    service.requirement_agent.execute.assert_called_once()

    # ----------------------------------------
    # Verify RTL Agent
    # ----------------------------------------

    service.rtl_agent.execute.assert_called_once()

    # ----------------------------------------
    # Verify Verification Agent
    # ----------------------------------------

    service.verification_agent.execute.assert_called_once()

    # ----------------------------------------
    # Verify Code Generation
    # ----------------------------------------

    service.code_generation_service.generate.assert_called_once()

    # ----------------------------------------
    # Verify Simulation
    # ----------------------------------------

    # Two simulations are expected:
    #
    # 1. Generated RTL simulation
    # 2. Post-synthesis netlist simulation

    assert service.simulation_service.simulate.call_count == 2

    simulation_calls = (
        service.simulation_service.simulate.call_args_list
    )

    first_simulation = simulation_calls[0]
    second_simulation = simulation_calls[1]

    # ----------------------------------------
    # First Simulation: Generated RTL
    # ----------------------------------------

    first_rtl_file = first_simulation.kwargs["rtl_file"]
    first_testbench_file = (
        first_simulation.kwargs["testbench_file"]
    )

    assert first_rtl_file.exists()
    assert first_testbench_file.exists()

    # ----------------------------------------
    # Second Simulation: Synthesized Netlist
    # ----------------------------------------

    assert (
        second_simulation.kwargs["rtl_file"]
        == netlist_path
    )

    assert (
        second_simulation.kwargs["testbench_file"]
        == first_testbench_file
    )

    # ----------------------------------------
    # Verify Synthesis
    # ----------------------------------------

    service.synthesis_service.synthesize.assert_called_once()

    synthesis_call = (
        service.synthesis_service.synthesize.call_args
    )

    assert (
        synthesis_call.kwargs["top_module"]
        == "alu"
    )

    # ----------------------------------------
    # Verify Documentation
    # ----------------------------------------

    service.documentation_service.generate.assert_called_once()