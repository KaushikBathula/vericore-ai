import json

from backend.app.utils.json_repair import repair_json


def test_repair_json_valid_json():
    raw = """
    {
        "test_vectors": [],
        "assertions": [],
        "coverage_points": []
    }
    """

    repaired = repair_json(raw)

    data = json.loads(repaired)

    assert data["test_vectors"] == []
    assert data["assertions"] == []
    assert data["coverage_points"] == []


def test_repair_json_python_values():
    raw = """
    {
        "enabled": True,
        "disabled": False,
        "value": None
    }
    """

    repaired = repair_json(raw)

    data = json.loads(repaired)

    assert data["enabled"] is True
    assert data["disabled"] is False
    assert data["value"] is None


def test_repair_json_trailing_comma():
    raw = """
    {
        "test_vectors": [],
        "assertions": [],
        "coverage_points": [],
    }
    """

    repaired = repair_json(raw)

    data = json.loads(repaired)

    assert data["test_vectors"] == []


def test_repair_json_single_quotes():
    raw = """
    {
        'name': 'test',
        'value': 1
    }
    """

    repaired = repair_json(raw)

    data = json.loads(repaired)

    assert data["name"] == "test"
    assert data["value"] == 1