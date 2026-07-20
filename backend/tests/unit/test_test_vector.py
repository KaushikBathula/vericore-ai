from backend.app.schemas.test_vector import TestVector


def test_create_test_vector():
    vector = TestVector(
        name="Addition",
        description="Verify addition",
        inputs={
            "a": 10,
            "b": 20,
            "operation": 0,
        },
        expected_outputs={
            "result": 30,
            "carry_out": 0,
        },
        delay=10,
    )

    assert vector.name == "Addition"
    assert vector.description == "Verify addition"
    assert vector.inputs["a"] == 10
    assert vector.inputs["b"] == 20
    assert vector.expected_outputs["result"] == 30
    assert vector.delay == 10