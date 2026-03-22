def test_unmatched_get_returns_200_with_stub_payload(client, snapshot):
    response = client.get("/api/does-not-exist")

    assert response.status_code == 200
    assert response.json() == snapshot


def test_unmatched_post_returns_200_with_stub_payload(client, snapshot):
    response = client.post("/api/payments/submit")

    assert response.status_code == 200
    assert response.json() == snapshot


def test_unmatched_delete_returns_200_with_stub_payload(client, snapshot):
    response = client.delete("/api/users/42")

    assert response.status_code == 200
    assert response.json() == snapshot


def test_unmatched_put_returns_200_with_stub_payload(client, snapshot):
    response = client.put("/api/users/42")

    assert response.status_code == 200
    assert response.json() == snapshot


def test_unmatched_patch_returns_200_with_stub_payload(client, snapshot):
    response = client.patch("/api/users/42/status")

    assert response.status_code == 200
    assert response.json() == snapshot
