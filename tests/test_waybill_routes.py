BASE = "/v3/dcapi-waybill-document-public"


def test_get_cost_centers(client, snapshot):
    response = client.get(f"{BASE}/cost-centers")

    assert response.status_code == 200
    assert response.json() == snapshot


def test_get_delivery_lead_times(client, snapshot):
    response = client.get(
        f"{BASE}/delivery/lead-times",
        params={"receiverCountryIso": "DE", "product": "DOCUMENTS_URGENT"},
    )

    assert response.status_code == 200
    assert response.json() == snapshot


def test_post_waybill_documents(client, snapshot):
    response = client.post(f"{BASE}/waybill/documents", data={"documentType": "OTHER"})

    assert response.status_code == 201
    assert response.json() == snapshot


def test_post_waybill_signatures(client, snapshot):
    response = client.post(f"{BASE}/waybill/signatures", data={})

    assert response.status_code == 201
    assert response.json() == snapshot


def test_create_waybill(client, snapshot):
    response = client.post(f"{BASE}/waybills", json={})

    assert response.status_code == 201
    assert response.json() == snapshot


def test_delete_waybill(client):
    response = client.delete(f"{BASE}/waybills/TT790123783CH")

    assert response.status_code == 204


def test_reprint_waybill(client, snapshot):
    response = client.get(f"{BASE}/waybills/TT790123783CH/default")

    assert response.status_code == 200
    assert response.json() == snapshot


def test_unmatched_waybill_path_returns_stub_not_found(client, snapshot):
    response = client.get(f"{BASE}/nonexistent-endpoint")

    assert response.status_code == 200
    assert response.json() == snapshot
