from fastapi.testclient import TestClient


def test_read_root(client: TestClient):
    """Test de l'endpoint racine"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "endpoints" in data
    assert "version" in data
    assert data["version"] == "2.0.0"


def test_health_check(client: TestClient):
    """Test de l'endpoint de santé"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["version"] == "2.0.0"
