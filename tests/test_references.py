def test_create_organization(client):
    resp = client.post("/api/references/organizations", json={
        "name": "АО ТестПром", "inn": "0987654321",
    })
    assert resp.status_code == 201
    assert resp.json()["name"] == "АО ТестПром"

def test_list_organizations(client):
    resp = client.get("/api/references/organizations")
    assert resp.status_code == 200

def test_create_ppe(client):
    resp = client.post("/api/references/ppe", json={
        "code": "PPE-001", "name": "Каска защитная",
        "type": "head_protection", "standard": "ГОСТ EN 397",
    })
    assert resp.status_code == 201

def test_create_equipment(client):
    resp = client.post("/api/references/equipment", json={
        "code": "EQ-001", "name": "Газоанализатор",
        "type": "gas_analyzer",
    })
    assert resp.status_code == 201

def test_create_checklist_item(client):
    resp = client.post("/api/references/checklist-items", json={
        "section": "Подготовка", "item_number": "1.1",
        "description": "Проведён инструктаж",
        "normative_ref": "п. 24 Приказа №528",
    })
    assert resp.status_code == 201
