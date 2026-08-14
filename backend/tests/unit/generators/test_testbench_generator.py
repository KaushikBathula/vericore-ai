from backend.app.generators.testbench_generator import TestbenchGenerator
from backend.app.schemas.rtl_design import RTLDesign
from backend.app.schemas.requirement_spec import RequirementSpec
from backend.app.schemas.port import Port
from backend.app.schemas.verification_plan import VerificationPlan
from backend.app.schemas.test_vector import TestVector


def test_testbench_generator_with_verification_plan():
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

    rtl_design = RTLDesign(
        requirement=requirement,
        implementation_strategy="Addition of two unsigned inputs.",
    )

    verification_plan = VerificationPlan(
        test_vectors=[
            TestVector(
                name="Zero Inputs",
                description="Verify addition with both inputs zero.",
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
                description="Verify addition with maximum 2-bit inputs.",
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

    generator = TestbenchGenerator()

    testbench = generator.generate(
        rtl_design,
        verification_plan,
    )

    # Module header
    assert "module tb_unsignedBinaryAdder;" in testbench

    # Input declarations
    assert "reg [1:0] A;" in testbench
    assert "reg [1:0] B;" in testbench

    # Output declarations
    assert "wire [1:0] SUM;" in testbench
    assert "wire CARRY;" in testbench

    # DUT instantiation
    assert "unsignedBinaryAdder dut (" in testbench
    assert ".A(A)" in testbench
    assert ".B(B)" in testbench
    assert ".SUM(SUM)" in testbench
    assert ".CARRY(CARRY)" in testbench

    # Test vector stimulus
    assert "A = 0;" in testbench
    assert "B = 0;" in testbench
    assert "A = 3;" in testbench
    assert "B = 3;" in testbench

    # Result checking
    assert "if (SUM !== 0)" in testbench
    assert "if (CARRY !== 0)" in testbench
    assert "if (SUM !== 2)" in testbench
    assert "if (CARRY !== 1)" in testbench

    # Simulation termination
    assert "$finish;" in testbench