from pathlib import Path

from backend.app.generators.testbench_generator import TestbenchGenerator
from backend.app.schemas.rtl_design import RTLDesign
from backend.app.schemas.requirement_spec import RequirementSpec
from backend.app.schemas.port import Port
from backend.app.schemas.verification_plan import VerificationPlan
from backend.app.schemas.test_vector import TestVector
from backend.app.services.simulation_runner import SimulationRunner


def test_generated_testbench_simulation():
    working_directory = (
        Path.cwd()
        / "generated_projects"
        / "test_verification_simulation"
    )

    working_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    rtl_file = working_directory / "adder.v"
    testbench_file = working_directory / "tb_unsignedBinaryAdder.v"
    output_file = working_directory / "simulation"

    # --------------------------------------------------
    # Requirement
    # --------------------------------------------------

    requirement = RequirementSpec(
        module_name="unsignedBinaryAdder",
        description="Design a 2-bit unsigned binary adder.",
        inputs=[
            Port(
                signal_name="A",
                direction="input",
                signal_width=2,
            ),
            Port(
                signal_name="B",
                direction="input",
                signal_width=2,
            ),
        ],
        outputs=[
            Port(
                signal_name="SUM",
                direction="output",
                signal_width=2,
            ),
            Port(
                signal_name="CARRY",
                direction="output",
                signal_width=1,
            ),
        ],
    )

    # --------------------------------------------------
    # RTL Design
    # --------------------------------------------------

    rtl_design = RTLDesign(
        requirement=requirement,
        implementation_strategy="2-bit unsigned addition.",
    )

    # --------------------------------------------------
    # Verification Plan
    # --------------------------------------------------

    verification_plan = VerificationPlan(
        test_vectors=[
            TestVector(
                name="Zero Inputs",
                description="Verify zero plus zero.",
                inputs={
                    "A": 0,
                    "B": 0,
                },
                expected_outputs={
                    "SUM": 0,
                    "CARRY": 0,
                },
                delay=10,
            ),
            TestVector(
                name="Maximum Inputs",
                description="Verify maximum 2-bit addition.",
                inputs={
                    "A": 3,
                    "B": 3,
                },
                expected_outputs={
                    "SUM": 2,
                    "CARRY": 1,
                },
                delay=10,
            ),
        ]
    )

    # --------------------------------------------------
    # Write RTL
    # --------------------------------------------------

    rtl_file.write_text(
        """
module unsignedBinaryAdder (
    input  [1:0] A,
    input  [1:0] B,
    output [1:0] SUM,
    output       CARRY
);

assign {CARRY, SUM} = A + B;

endmodule
""".strip()
    )

    # --------------------------------------------------
    # Generate Testbench
    # --------------------------------------------------

    generator = TestbenchGenerator()

    testbench = generator.generate(
        rtl_design,
        verification_plan,
    )

    testbench_file.write_text(testbench)

    # --------------------------------------------------
    # Run Simulation
    # --------------------------------------------------

    runner = SimulationRunner()

    result = runner.run(
        rtl_file=rtl_file,
        testbench_file=testbench_file,
        output_file=output_file,
        working_directory=working_directory,
    )

    # --------------------------------------------------
    # Verify
    # --------------------------------------------------

    assert result.compile_success is True
    assert result.simulation_success is True