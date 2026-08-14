from pathlib import Path

from backend.app.services.simulation_runner import SimulationRunner


def test_simulation_runner():
    working_directory = (
        Path.cwd() / "generated_projects" / "test_simulation"
    ) 
    working_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    rtl_file = working_directory / "adder.v"
    testbench_file = working_directory / "tb_adder.v"
    output_file = working_directory / "simulation"

    rtl_file.write_text(
        """
module adder (
    input  [1:0] A,
    input  [1:0] B,
    output [1:0] SUM,
    output       CARRY
);

assign {CARRY, SUM} = A + B;

endmodule
""".strip()
    )

    testbench_file.write_text(
        """
module tb_adder;

reg [1:0] A;
reg [1:0] B;

wire [1:0] SUM;
wire CARRY;

adder dut (
    .A(A),
    .B(B),
    .SUM(SUM),
    .CARRY(CARRY)
);

initial begin

    A = 0;
    B = 0;

    #10;

    if (SUM !== 0) begin
        $display("FAIL: SUM expected=0, got=%0d", SUM);
        $fatal;
    end

    if (CARRY !== 0) begin
        $display("FAIL: CARRY expected=0, got=%0d", CARRY);
        $fatal;
    end

    A = 3;
    B = 3;

    #10;

    if (SUM !== 2) begin
        $display("FAIL: SUM expected=2, got=%0d", SUM);
        $fatal;
    end

    if (CARRY !== 1) begin
        $display("FAIL: CARRY expected=1, got=%0d", CARRY);
        $fatal;
    end

    $finish;

end

endmodule
""".strip()
    )

    runner = SimulationRunner()

    result = runner.run(
        rtl_file=rtl_file,
        testbench_file=testbench_file,
        output_file=output_file,
        working_directory=working_directory,
    )

    assert result.compile_success is True
    assert result.simulation_success is True