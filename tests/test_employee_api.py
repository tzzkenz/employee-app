from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_endpoint_is_public():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["message"] == "App is healthy"
