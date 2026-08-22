import pytest

from backend.app.core.parsers.response_parser import ResponseParser


def test_parse_requirement_response_with_complete_ports():
    response = """
    {
        "module_name": "TwoBitAdder",
        "description": "2-bit adder",
        "inputs": [
            {
                "signal_name": "A",
                "signal_width": 2,
                "signal_type": "input",
                "direction": "input"
            },
            {
                "signal_name": "B",
                "signal_width": 2,
                "signal_type": "input",
                "direction": "input"
            }
        ],
        "outputs": [
            {
                "signal_name": "SUM",
                "signal_width": 2,
                "signal_type": "output",
                "direction": "output"
            },
            {
                "signal_name": "CARRY",
                "signal_width": 1,
                "signal_type": "output",
                "direction": "output"
            }
        ],
        "operations": [],
        "parameters": {},
        "verification_points": []
    }
    """

    result = ResponseParser.parse_requirement_response(response)

    assert result.module_name == "TwoBitAdder"

    assert len(result.inputs) == 2
    assert result.inputs[0].signal_name == "A"
    assert result.inputs[0].signal_width == 2
    assert result.inputs[0].direction == "input"

    assert len(result.outputs) == 2
    assert result.outputs[0].signal_name == "SUM"
    assert result.outputs[0].signal_width == 2
    assert result.outputs[0].direction == "output"


def test_parse_requirement_response_infers_input_direction():
    response = """
    {
        "module_name": "Adder",
        "description": "Simple adder",
        "inputs": [
            {
                "signal_name": "A",
                "signal_width": 2,
                "signal_type": "input"
            },
            {
                "signal_name": "B",
                "signal_width": 2,
                "signal_type": "input"
            }
        ],
        "outputs": [
            {
                "signal_name": "SUM",
                "signal_width": 2,
                "signal_type": "output"
            }
        ]
    }
    """

    result = ResponseParser.parse_requirement_response(response)

    assert result.inputs[0].direction == "input"
    assert result.inputs[1].direction == "input"
    assert result.outputs[0].direction == "output"


def test_parse_requirement_response_normalizes_short_directions():
    response = """
    {
        "module_name": "TestModule",
        "description": "Test",
        "inputs": [
            {
                "signal_name": "A",
                "signal_width": 1,
                "signal_type": "input",
                "direction": "in"
            }
        ],
        "outputs": [
            {
                "signal_name": "Y",
                "signal_width": 1,
                "signal_type": "output",
                "direction": "out"
            }
        ]
    }
    """

    result = ResponseParser.parse_requirement_response(response)

    assert result.inputs[0].direction == "input"
    assert result.outputs[0].direction == "output"


def test_parse_requirement_response_normalizes_signal_names():
    response = """
    {
        "module_name": "Adder",
        "description": "2-bit adder",
        "inputs": [
            {
                "signal_name": "A[1:0]",
                "signal_width": 2,
                "signal_type": "input"
            }
        ],
        "outputs": [
            {
                "signal_name": "SUM[1:0]",
                "signal_width": 2,
                "signal_type": "output"
            }
        ]
    }
    """

    result = ResponseParser.parse_requirement_response(response)

    assert result.inputs[0].signal_name == "A"
    assert result.outputs[0].signal_name == "SUM"


def test_parse_requirement_response_normalizes_verification_points():
    response = """
    {
        "module_name": "Adder",
        "description": "2-bit adder",
        "inputs": [],
        "outputs": [],
        "verification_points": [
            "Verify addition",
            {
                "point_name": "CarryCheck",
                "description": "Verify carry output"
            }
        ]
    }
    """

    result = ResponseParser.parse_requirement_response(response)

    assert len(result.verification_points) == 2

    assert result.verification_points[0].name == "Verify addition"
    assert result.verification_points[0].description == "Verify addition"

    assert result.verification_points[1].name == "CarryCheck"
    assert result.verification_points[1].description == (
        "Verify carry output"
    )


def test_parse_requirement_response_invalid_json():
    response = """
    {
        "module_name": "Adder",
        "inputs":
    """

    with pytest.raises(ValueError):
        ResponseParser.parse_requirement_response(response)


def test_parse_requirement_response_missing_module_name():
    response = """
    {
        "description": "2-bit adder",
        "inputs": [],
        "outputs": []
    }
    """

    with pytest.raises(ValueError, match="Requirement specification validation failed"):
        ResponseParser.parse_requirement_response(response)