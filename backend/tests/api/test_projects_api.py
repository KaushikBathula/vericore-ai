from fastapi.testclient import TestClient


def test_project_crud_endpoints(client: TestClient) -> None:
    """Project endpoints create, list, fetch, and delete metadata."""
    create_response = client.post(
        "/projects",
        json={
            "project_name": "alu-demo",
            "description": "Metadata only project for Milestone 1.",
        },
    )

    assert create_response.status_code == 201
    created = create_response.json()
    assert created["id"] == 1
    assert created["project_name"] == "alu-demo"
    assert created["status"] == "created"

    list_response = client.get("/projects")
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    get_response = client.get("/projects/1")
    assert get_response.status_code == 200
    assert get_response.json()["project_name"] == "alu-demo"

    delete_response = client.delete("/projects/1")
    assert delete_response.status_code == 200
    assert delete_response.json() == {
        "success": True,
        "message": "Project deleted successfully.",
    }

    missing_response = client.get("/projects/1")
    assert missing_response.status_code == 404
