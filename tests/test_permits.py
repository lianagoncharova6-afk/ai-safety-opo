def test_create_permit(client):
    client.post("/api/references/organizations", json={
        "name": "ООО ТестНефтеГаз", "inn": "1234567890",
    })
    client.post("/api/references/objects", json={
        "okpo_code": "12345678", "name": "Тестовый ОПО",
        "danger_class": "III", "organization_id": 1,
    })
    client.post("/api/references/employees", json={
        "full_name": "Иванов И.И.", "position": "Начальник цеха",
    })
    client.post("/api/references/employees", json={
        "full_name": "Петров П.П.", "position": "Мастер",
    })

    resp = client.post("/api/permits/", json={
        "permit_number": "ND-2026-001",
        "permit_type": "gas_hazard",
        "object_okpo_id": 1,
        "responsible_person_id": 1,
        "work_manager_id": 2,
        "work_description": "Зачистка резервуара РВС-5000",
        "work_start_date": "2026-06-28T08:00:00",
        "work_end_date": "2026-06-28T17:00:00",
    })
    assert resp.status_code == 201
    assert resp.json()["permit_number"] == "ND-2026-001"
    assert resp.json()["status"] == "draft"

def test_list_permits(client):
    resp = client.get("/api/permits/")
    assert resp.status_code == 200

def test_activate_permit(client):
    resp = client.post("/api/permits/1/activate")
    assert resp.status_code == 200
    assert resp.json()["status"] == "active"

def test_close_permit(client):
    resp = client.post("/api/permits/1/close")
    assert resp.status_code == 200
    assert resp.json()["status"] == "closed"

def test_get_nonexistent_permit(client):
    resp = client.get("/api/permits/9999")
    assert resp.status_code == 404

