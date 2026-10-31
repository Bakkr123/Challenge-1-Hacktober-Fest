from fastapi.testclient import TestClient

from app.main import app


def test_health_shape() -> None:
    client = TestClient(app)
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    body = response.json()
    assert body["error"] is None
    assert body["data"]["active_model"] in {"gemma4:e4b", "gemma-4-26b-a4b-it"}
    assert body["data"]["hosted_evaluation"]["status"] in {"READY", "NOT_CONFIGURED"}
    assert body["data"]["runtime_location"] in {"LOCAL", "HOSTED"}


def test_hosted_evaluation_rejects_non_synthetic_data() -> None:
    client = TestClient(app)
    response = client.post(
        "/api/v1/evaluation/gemini/analyze",
        json={"is_synthetic": False, "original_text": "Real report must not be sent"},
    )
    assert response.status_code == 422
    assert "synthetic" in response.json()["detail"].lower()
