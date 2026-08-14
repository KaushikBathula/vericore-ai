from pathlib import Path

from backend.app.services.synthesis_service import SynthesisService


def test_synthesis_service_real_yosys(tmp_path: Path):
    rtl_source = """
module simple_adder (
    input  wire A,
    input  wire B,
    output wire SUM
);

assign SUM = A ^ B;

endmodule
"""

    service = SynthesisService()

    result = service.synthesize(
        rtl_source=rtl_source,
        top_module="simple_adder",
        output_directory=tmp_path,
    )

    assert result.synthesis_success is True

    assert result.stdout is not None
    assert result.stderr is not None

    assert result.report_path is not None
    assert Path(result.report_path).exists()

    assert result.netlist_path is not None
    assert Path(result.netlist_path).exists()

    assert result.cell_count is not None
    assert result.cell_count >= 1

    assert result.warning_count >= 0

    assert (tmp_path / "design.v").exists()
    assert (tmp_path / "design.ys").exists()
    assert (tmp_path / "yosys.log").exists()
    assert (tmp_path / "netlist.v").exists()