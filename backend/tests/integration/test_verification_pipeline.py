from pathlib import Path
from backend.app.generators.testbench_generator import (
    TestbenchGenerator as VericoreTestbenchGenerator,
)
from backend.app.services.generation_service import GenerationService
from backend.app.services.simulation_runner import SimulationRunner


def test_verification_pipeline():

    # -------------------------------------------------
    # 1. Generate requirement → RTL → verification plan
    # -------------------------------------------------

    service = GenerationService()

    requirement = """
    Design a 2-bit unsigned binary adder.

    Inputs:
    A[1:0]
    B[1:0]

    Outputs:
    SUM[1:0]
    CARRY

    Function:
    Perform A + B.
    """

    requirement_spec, rtl_design, verification_plan = service.generate(
        requirement
    )

    assert requirement_spec is not None
    assert rtl_design is not None
    assert verification_plan is not None

    assert verification_plan.test_vectors

    # -------------------------------------------------
    # 2. Generate testbench
    # -------------------------------------------------

    testbench_generator = VericoreTestbenchGenerator()

    testbench = testbench_generator.generate(
        rtl_design=rtl_design,
        verification_plan=verification_plan,
    )
    print("\n========== GENERATED TESTBENCH ==========\n")
    print(testbench)
    print("\n=========================================\n")

    assert testbench
    assert "module" in testbench
    assert "dut" in testbench
    assert "$finish" in testbench

    # -------------------------------------------------
    # 3. Create temporary project directory
    # -------------------------------------------------

    working_directory = Path(
        "generated_projects/test_verification_pipeline"
    )

    working_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    rtl_file = working_directory / "adder.v"
    testbench_file = working_directory / "tb_adder.v"
    output_file = working_directory / "simulation"

    # -------------------------------------------------
    # 4. Write RTL
    # -------------------------------------------------

    rtl_file.write_text(
        f"""
    module {requirement_spec.module_name} (
        input  [1:0] A,
        input  [1:0] B,
        output [1:0] SUM,
        output       CARRY
    );

    assign {{CARRY, SUM}} = {{1'b0, A}} + {{1'b0, B}};

    endmodule
    """.strip()
    )
    

    # -------------------------------------------------
    # 5. Write generated testbench
    # -------------------------------------------------
    print("\n========== GENERATED TESTBENCH ==========\n")
    print(testbench)
    print("\n==========================================\n")
    testbench_file.write_text(testbench)

    # -------------------------------------------------
    # 6. Run simulation
    # -------------------------------------------------

    runner = SimulationRunner()

    result = runner.run(
        rtl_file=rtl_file,
        testbench_file=testbench_file,
        output_file=output_file,
        working_directory=working_directory,
    )

    # -------------------------------------------------
    # 7. Verify compilation and simulation
    # -------------------------------------------------

    assert result.compile_success is True, result.compiler_output

    assert result.simulation_success is True, (
        result.simulation_output
    )