from fastapi.testclient import TestClient


def test_health_endpoint_returns_ok(client: TestClient) -> None:
    """Health endpoint reports API version and database connectivity."""
    response = client.get("/api/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["version"] == "0.1.0"
    assert body["database_connectivity"] is True
