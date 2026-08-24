from pathlib import Path
from unittest.mock import MagicMock, patch

from backend.app.services.pipeline_service import PipelineService


def test_pipeline_retries_when_synthesis_fails(tmp_path: Path):
    service = PipelineService()

    fake_report = MagicMock()

    graph_result = {
        "report": fake_report,
        "current_stage": "documentation",
        "workflow_status": "completed",
        "error": None,
    }

    with patch(
        "backend.app.services.pipeline_service.design_graph.invoke",
        return_value=graph_result,
    ) as mock_invoke:

        report = service.execute(
            requirement_text="Design an ALU",
            output_directory=tmp_path,
        )

    assert report is fake_report

    mock_invoke.assert_called_once()

    initial_state = mock_invoke.call_args.args[0]

    assert initial_state["requirement_text"] == "Design an ALU"
    assert initial_state["debug_iteration"] == 0
    assert initial_state["max_debug_iterations"] == 3
    assert initial_state["current_stage"] == "starting"
    assert initial_state["workflow_status"] == "starting"
    assert initial_state["error"] is None