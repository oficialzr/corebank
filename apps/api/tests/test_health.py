from fastapi.testclient import TestClient

from corebank_api.main import app


client = TestClient(app)


def test_health_check_returns_ok() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_version_returns_service_info() -> None:
    response = client.get("/version")

    assert response.status_code == 200
    assert response.json() == {
        "service": "corebank-api",
        "version": "0.1.0",
        "environment": "local",
    }