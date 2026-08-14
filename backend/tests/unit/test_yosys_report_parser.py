from backend.app.synthesis.yosys_report_parser import YosysReportParser


def test_parse_cell_count():
    report = """
    === design hierarchy ===

    Number of wires: 3
    Number of wire bits: 5
    Number of public wires: 3
    Number of public wire bits: 5
    Number of memories: 0
    Number of memory bits: 0
    Number of processes: 0
    Number of cells: 4
    """

    assert YosysReportParser.parse_cell_count(report) == 4


def test_parse_cell_count_missing():
    report = """
    === design hierarchy ===
    Number of wires: 3
    Number of cells: 0
    """

    assert YosysReportParser.parse_cell_count(report) == 0


def test_parse_cell_count_not_found():
    report = """
    === design hierarchy ===
    Number of wires: 3
    Number of wire bits: 5
    """

    assert YosysReportParser.parse_cell_count(report) is None


def test_parse_cell_count_multiple_matches():
    report = """
    === design hierarchy ===
    Number of cells: 2

    === design hierarchy ===
    Number of cells: 5
    """

    assert YosysReportParser.parse_cell_count(report) == 2


def test_parse_warning_count():
    report = """
    Warning: signal is unused.
    WARNING: wire has no driver.
    warning: optimization skipped.
    """

    assert YosysReportParser.parse_warning_count(report) == 3


def test_parse_warning_count_none():
    report = """
    Yosys 0.50
    Number of cells: 4
    Synthesis completed successfully.
    """

    assert YosysReportParser.parse_warning_count(report) == 0