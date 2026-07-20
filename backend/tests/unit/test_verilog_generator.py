from backend.app.generators.verilog_generator import VerilogGenerator
from backend.app.schemas.operation import Operation
from backend.app.schemas.port import Port
from backend.app.schemas.requirement_spec import RequirementSpec
from backend.app.schemas.rtl_design import RTLDesign
from backend.app.schemas.signal import Signal, SignalType


def create_rtl(parameters=None):
    requirement = RequirementSpec(
        module_name="adder4",
        description="4-bit adder",
        inputs=[
            Port(
                signal_name="a",
                signal_width=4,
                direction="input",
            ),
            Port(
                signal_name="b",
                signal_width=4,
                direction="input",
            ),
        ],
        outputs=[
            Port(
                signal_name="sum",
                signal_width=4,
                direction="output",
            )
        ],
        operations=[
            Operation(
                operation_name="Addition",
                description="Add two inputs",
            )
        ],
    )

    return RTLDesign(
        requirement=requirement,
        internal_signals=[
            Signal(
                signal_name="carry",
                signal_width=1,
                signal_type=SignalType.WIRE,
            )
        ],
        implementation_strategy="Ripple Carry",
        parameters=parameters or {},
    )


def test_generate_parameterized_verilog():

    generator = VerilogGenerator()

    rtl = create_rtl()

    verilog = generator.generate(rtl)

    assert "parameter WIDTH = 4" in verilog
    assert "input [WIDTH-1:0] a" in verilog
    assert "output [WIDTH-1:0] sum" in verilog


def test_generate_multiple_parameters():

    generator = VerilogGenerator()

    rtl = create_rtl(
        parameters={
            "WIDTH": 32,
            "DEPTH": 256,
            "ADDR_WIDTH": 8,
        }
    )

    verilog = generator.generate(rtl)

    assert "parameter WIDTH = 32" in verilog
    assert "parameter DEPTH = 256" in verilog
    assert "parameter ADDR_WIDTH = 8" in verilog

    assert "assign sum = a + b;" in verilog