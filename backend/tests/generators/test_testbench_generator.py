import pytest

from backend.app.generators.testbench_generator import TestbenchGenerator
from backend.app.schemas.port import Port
from backend.app.schemas.requirement_spec import RequirementSpec
from backend.app.schemas.rtl_design import RTLDesign


def create_sample_rtl_design() -> RTLDesign:
    """
    Create a minimal RTLDesign instance for testing the
    TestbenchGenerator.
    """

    requirement = RequirementSpec(
        module_name="adder",
        description="Simple 8-bit adder",
        inputs=[
            Port(
                signal_name="a",
                signal_width=8,
                direction="input",
            ),
            Port(
                signal_name="b",
                signal_width=8,
                direction="input",
            ),
        ],
        outputs=[
            Port(
                signal_name="sum",
                signal_width=8,
                direction="output",
            ),
        ],
        operations=[],
        parameters={},
        verification_points=[],
    )

    return RTLDesign(
        requirement=requirement,
        internal_signals=[],
        implementation_strategy="",
        derived_operations=[],
        parameters={},
        metadata={},
    )


def test_generate_testbench_returns_string():
    generator = TestbenchGenerator()
    rtl = create_sample_rtl_design()

    tb_code = generator.generate(rtl)

    assert isinstance(tb_code, str)


def test_contains_testbench_module():
    generator = TestbenchGenerator()
    rtl = create_sample_rtl_design()

    tb_code = generator.generate(rtl)

    assert "module tb_adder;" in tb_code


def test_contains_dut_instantiation():
    generator = TestbenchGenerator()
    rtl = create_sample_rtl_design()

    tb_code = generator.generate(rtl)

    assert "adder dut" in tb_code


def test_contains_dumpfile():
    generator = TestbenchGenerator()
    rtl = create_sample_rtl_design()

    tb_code = generator.generate(rtl)

    assert "$dumpfile" in tb_code


def test_contains_dumpvars():
    generator = TestbenchGenerator()
    rtl = create_sample_rtl_design()

    tb_code = generator.generate(rtl)

    assert "$dumpvars" in tb_code


def test_contains_initial_block():
    generator = TestbenchGenerator()
    rtl = create_sample_rtl_design()

    tb_code = generator.generate(rtl)

    assert "initial begin" in tb_code


def test_contains_finish():
    generator = TestbenchGenerator()
    rtl = create_sample_rtl_design()

    tb_code = generator.generate(rtl)

    assert "$finish;" in tb_code
