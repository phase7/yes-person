def test_health_returns_ok(client, snapshot):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == snapshot
