"""
Модуль AI-видеоаналитики: симуляция обнаружения нарушений
с помощью камер компьютерного зрения.
"""
import random
from typing import List, Dict
from sqlalchemy.orm import Session
from app import crud, schemas

VIOLATION_TYPES_POOL = [
    "no_helmet", "no_vest", "no_mask", "danger_zone_entry",
    "smoke_detected", "fire_detected", "spill_detected", "equipment_failure"
]

VIOLATION_LABELS = {
    "no_helmet": "Отсутствие каски",
    "no_vest": "Отсутствие сигнального жилета",
    "no_mask": "Отсутствие противогаза",
    "danger_zone_entry": "Вход в опасную зону",
    "smoke_detected": "Задымление",
    "fire_detected": "Возгорание",
    "spill_detected": "Разлив нефтепродуктов",
    "equipment_failure": "Отказ оборудования",
}

def simulate_ai_scan(db: Session, permit_id: int) -> List[Dict]:
    violations_found = []
    if random.random() < 0.3:
        return violations_found
    num_violations = random.randint(1, 3)
    selected_types = random.sample(
        VIOLATION_TYPES_POOL, min(num_violations, len(VIOLATION_TYPES_POOL))
    )
    camera_ids = ["CAM-01", "CAM-02", "CAM-03", "CAM-04"]
    for v_type in selected_types:
        severity = random.randint(1, 5)
        probability = random.randint(1, 5)
        data = schemas.ViolationCreate(
            permit_id=permit_id,
            violation_type=v_type,
            severity=severity,
            probability=probability,
            detected_by_ai=True,
            camera_id=random.choice(camera_ids),
            image_snapshot_url=f"/snapshots/{permit_id}/{v_type}_{random.randint(1000,9999)}.jpg",
        )
        violation = crud.create_violation(db, data)
        violations_found.append({
            "id": violation.id,
            "type": v_type,
            "label": VIOLATION_LABELS.get(v_type, v_type),
            "severity": severity,
            "probability": probability,
            "risk_level": violation.risk_level,
            "camera_id": violation.camera_id,
        })
    return violations_found

def simulate_continuous_monitoring(db: Session, permit_id: int, cycles: int = 10):
    all_violations = []
    for _ in range(cycles):
        result = simulate_ai_scan(db, permit_id)
        all_violations.extend(result)
    return all_violations

