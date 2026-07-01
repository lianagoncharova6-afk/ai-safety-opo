"""
Расчёт матрицы рисков (5×5) согласно методологии Risk Assessment Matrix.
"""

from sqlalchemy.orm import Session
from app.models import RiskMatrix, Violation


def classify_risk(risk_score: int) -> str:
    if risk_score <= 4:
        return "low"
    elif risk_score <= 9:
        return "medium"
    elif risk_score <= 16:
        return "high"
    else:
        return "critical"


MITIGATION_TEMPLATES = {
    "no_helmet": "Обязать использование защитных касок. Провести внеплановый инструктаж.",
    "no_vest": "Проверить наличие сигнальных жилетов у всех членов бригады.",
    "no_mask": "Выдать противогазы. Провести замеры воздуха перед допуском.",
    "danger_zone_entry": "Установить дополнительные ограждения. Усилить контроль доступа.",
    "smoke_detected": "Остановить работы. Вызвать пожарную службу. Эвакуировать персонал.",
    "fire_detected": "Немедленная эвакуация. Активировать систему пожаротушения.",
    "spill_detected": "Локализовать разлив. Вызвать аварийную бригаду.",
    "equipment_failure": "Остановить использование оборудования. Провести дефектовку.",
}


def generate_risk_matrix_for_permit(db: Session, permit_id: int):
    violations = db.query(Violation).filter(Violation.permit_id == permit_id).all()
    grouped = {}
    for v in violations:
        if v.violation_type not in grouped:
            grouped[v.violation_type] = {"severity": v.severity, "probability": v.probability}
        else:
            grouped[v.violation_type]["severity"] = max(
                grouped[v.violation_type]["severity"], v.severity
            )
            grouped[v.violation_type]["probability"] = max(
                grouped[v.violation_type]["probability"], v.probability
            )
    for v_type, values in grouped.items():
        severity = values["severity"]
        probability = values["probability"]
        risk_score = min(severity * probability, 25)
        risk_category = classify_risk(risk_score)
        from app.services.ai_vision import VIOLATION_LABELS

        label = VIOLATION_LABELS.get(v_type, v_type)
        mitigation = MITIGATION_TEMPLATES.get(v_type, "Разработать меры по снижению риска.")
        entry = RiskMatrix(
            permit_id=permit_id,
            hazard_description=f"{label} (обнаружено AI-камерами в ходе работ)",
            probability=probability,
            severity=severity,
            risk_score=risk_score,
            risk_category=risk_category,
            mitigation_measures=mitigation,
        )
        db.add(entry)
    db.commit()
