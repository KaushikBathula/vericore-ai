from pathlib import Path

from backend.app.services.synthesis_service import SynthesisService


def test_synthesis_service_invalid_rtl(tmp_path: Path):
    rtl_source = """
module broken_design (
    input wire A,
    output wire Y
);

assign Y = A ^ ;

endmodule
"""

    service = SynthesisService()

    result = service.synthesize(
        rtl_source=rtl_source,
        top_module="broken_design",
        output_directory=tmp_path,
    )

    assert result.synthesis_success is False

    assert result.report_path is not None
    assert Path(result.report_path).exists()

    assert result.netlist_path is None

    assert result.stdout is not None
    assert result.stderr is not None

    assert result.synthesis_output