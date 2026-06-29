def test_create_violation(client):
    resp = client.post("/api/violations/", json={
        "permit_id": 1, "violation_type": "no_helmet",
        "severity": 4, "probability": 3, "camera_id": "CAM-01",
    })
    assert resp.status_code == 201
    assert resp.json()["risk_level"] == 12

def test_list_violations(client):
    resp = client.get("/api/violations/")
    assert resp.status_code == 200

def test_resolve_violation(client):
    resp = client.post("/api/violations/1/resolve?notes=Устранено")
    assert resp.status_code == 200
    assert resp.json()["status"] == "resolved"

def test_ai_scan_no_active_permit(client):
    resp = client.post("/api/violations/ai-scan/1")
    assert resp.status_code in [200, 400]
