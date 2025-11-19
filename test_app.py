import app

def test_health():
    client = app.app.test_client()
    response = client.get("/health")
    assert response.json["status"] == "healthy"

