from pathlib import Path
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_pipeline_api_success():
    """Test successful pipeline execution."""

    fake_report = MagicMock()
    fake_report.success = True

    with patch(
        "backend.app.api.pipeline.PipelineService"
    ) as mock_service_class:

        mock_service = MagicMock()
        mock_service_class.return_value = mock_service

        mock_service.execute.return_value = fake_report

        response = client.post(
            "/api/pipeline/run",
            json={
                "requirement": (
                    "Design a synthesizable 2-bit adder. "
                    "Inputs are A and B, outputs are SUM and CARRY."
                )
            },
        )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["report_path"] == "generated_projects"
    assert data["message"] == "Pipeline executed successfully."

    mock_service_class.assert_called_once()

    mock_service.execute.assert_called_once_with(
        requirement_text=(
            "Design a synthesizable 2-bit adder. "
            "Inputs are A and B, outputs are SUM and CARRY."
        ),
        output_directory=Path("generated_projects"),
    )


def test_pipeline_api_failure():
    """Test pipeline API when pipeline execution fails."""

    with patch(
        "backend.app.api.pipeline.PipelineService"
    ) as mock_service_class:

        mock_service = MagicMock()
        mock_service_class.return_value = mock_service

        mock_service.execute.side_effect = RuntimeError(
            "Pipeline execution failed"
        )

        response = client.post(
            "/api/pipeline/run",
            json={
                "requirement": "Design a 2-bit adder."
            },
        )

    assert response.status_code == 500

    data = response.json()

    assert data["detail"] == "Pipeline execution failed"


def test_pipeline_api_invalid_request():
    """Test validation failure when requirement is missing."""

    response = client.post(
        "/api/pipeline/run",
        json={},
    )

    assert response.status_code == 422