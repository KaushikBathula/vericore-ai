from backend.app.generators.formatter import VerilogFormatter
from backend.app.schemas.port import Port
from backend.app.schemas.signal import Signal, SignalType


def test_format_port():
    port = Port(
        signal_name="a",
        signal_width=8,
        direction="input",
    )

    assert (
        VerilogFormatter.format_port(port)
        == "input [7:0] a"
    )


def test_format_signal():
    signal = Signal(
        signal_name="carry",
        signal_width=1,
        signal_type=SignalType.WIRE,
    )

    assert (
        VerilogFormatter.format_signal(signal)
        == "wire carry;"
    )


def test_format_assign():
    assert (
        VerilogFormatter.format_assign(
            "sum",
            "a + b",
        )
        == "assign sum = a + b;"
    )