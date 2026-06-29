"""
CRUD-операции для всех сущностей.
"""
from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from app import models, schemas


# ========== Organization ==========
def create_organization(db: Session, data: schemas.OrganizationCreate) -> models.Organization:
    obj = models.Organization(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_organizations(db: Session) -> List[models.Organization]:
    return db.query(models.Organization).all()


# ========== ObjectOkpo ==========
def create_object_okpo(db: Session, data: schemas.ObjectOkpoCreate) -> models.ObjectOkpo:
    obj = models.ObjectOkpo(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_objects_okpo(db: Session) -> List[models.ObjectOkpo]:
    return db.query(models.ObjectOkpo).all()


# ========== Employee ==========
def create_employee(db: Session, data: schemas.EmployeeCreate) -> models.Employee:
    obj = models.Employee(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_employees(db: Session, active_only: bool = True) -> List[models.Employee]:
    q = db.query(models.Employee)
    if active_only:
        q = q.filter(models.Employee.is_active == True)
    return q.all()


def get_employee(db: Session, employee_id: int) -> Optional[models.Employee]:
    return db.query(models.Employee).filter(models.Employee.id == employee_id).first()


# ========== PPE ==========
def create_ppe(db: Session, data: schemas.PpeCreate) -> models.Ppe:
    obj = models.Ppe(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_all_ppe(db: Session) -> List[models.Ppe]:
    return db.query(models.Ppe).all()


# ========== Equipment ==========
def create_equipment(db: Session, data: schemas.EquipmentCreate) -> models.Equipment:
    obj = models.Equipment(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_all_equipment(db: Session) -> List[models.Equipment]:
    return db.query(models.Equipment).all()


# ========== SafetySign ==========
def create_safety_sign(db: Session, data: schemas.SafetySignCreate) -> models.SafetySign:
    obj = models.SafetySign(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_all_safety_signs(db: Session) -> List[models.SafetySign]:
    return db.query(models.SafetySign).all()


# ========== ActivityType ==========
def create_activity_type(db: Session, data: schemas.ActivityTypeCreate) -> models.ActivityType:
    obj = models.ActivityType(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_all_activity_types(db: Session) -> List[models.ActivityType]:
    return db.query(models.ActivityType).all()


# ========== WorkPermit ==========
def create_work_permit(db: Session, data: schemas.WorkPermitCreate) -> models.WorkPermit:
    obj = models.WorkPermit(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_work_permits(db: Session, status: Optional[str] = None) -> List[models.WorkPermit]:
    q = db.query(models.WorkPermit)
    if status:
        q = q.filter(models.WorkPermit.status == status)
    return q.order_by(models.WorkPermit.created_at.desc()).all()


def get_work_permit(db: Session, permit_id: int) -> Optional[models.WorkPermit]:
    return db.query(models.WorkPermit).filter(models.WorkPermit.id == permit_id).first()


def update_work_permit(
    db: Session, permit_id: int, data: schemas.WorkPermitUpdate
) -> Optional[models.WorkPermit]:
    obj = get_work_permit(db, permit_id)
    if not obj:
        return None
    update_data = data.model_dump(exclude_unset=True)
    if update_data.get("status") == "closed" and obj.status != "closed":
        update_data["closed_at"] = datetime.utcnow()
    for key, value in update_data.items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


def close_work_permit(db: Session, permit_id: int) -> Optional[models.WorkPermit]:
    obj = get_work_permit(db, permit_id)
    if not obj or obj.status == "closed":
        return None
    obj.status = "closed"
    obj.closed_at = datetime.utcnow()
    db.commit()
    from app.services.risk_matrix import generate_risk_matrix_for_permit
    generate_risk_matrix_for_permit(db, permit_id)
    db.refresh(obj)
    return obj


# ========== Violation ==========
def create_violation(db: Session, data: schemas.ViolationCreate) -> models.Violation:
    risk_level = min(data.severity * data.probability, 25)
    obj = models.Violation(**data.model_dump(), risk_level=risk_level)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_violations(
    db: Session, permit_id: Optional[int] = None, status: Optional[str] = None
) -> List[models.Violation]:
    q = db.query(models.Violation)
    if permit_id:
        q = q.filter(models.Violation.permit_id == permit_id)
    if status:
        q = q.filter(models.Violation.status == status)
    return q.order_by(models.Violation.detected_at.desc()).all()


def resolve_violation(
    db: Session, violation_id: int, resolution_notes: str = ""
) -> Optional[models.Violation]:
    obj = db.query(models.Violation).filter(models.Violation.id == violation_id).first()
    if not obj:
        return None
    obj.status = "resolved"
    obj.resolved_at = datetime.utcnow()
    obj.resolution_notes = resolution_notes
    db.commit()
    db.refresh(obj)
    return obj


# ========== ChecklistItem ==========
def create_checklist_item(db: Session, data: schemas.ChecklistItemCreate) -> models.ChecklistItem:
    obj = models.ChecklistItem(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_checklist_items(db: Session) -> List[models.ChecklistItem]:
    return db.query(models.ChecklistItem).all()


# ========== PermitChecklist ==========
def create_permit_checklist(
    db: Session, permit_id: int, items: List[int]
) -> List[models.PermitChecklist]:
    results = []
    for item_id in items:
        obj = models.PermitChecklist(permit_id=permit_id, checklist_item_id=item_id)
        db.add(obj)
        results.append(obj)
    db.commit()
    return results


# ========== GasMonitor ==========
def create_gas_monitor(db: Session, data: schemas.GasMonitorCreate) -> models.GasMonitor:
    obj = models.GasMonitor(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_gas_monitors(db: Session, permit_id: int) -> List[models.GasMonitor]:
    return (
        db.query(models.GasMonitor)
        .filter(models.GasMonitor.permit_id == permit_id)
        .order_by(models.GasMonitor.monitor_time.desc())
        .all()
    )


# ========== Dashboard ==========
def get_dashboard_stats(db: Session) -> dict:
    total_permits = db.query(func.count(models.WorkPermit.id)).scalar()
    active_permits = (
        db.query(func.count(models.WorkPermit.id))
        .filter(models.WorkPermit.status == "active")
        .scalar()
    )
    total_violations = db.query(func.count(models.Violation.id)).scalar()

    v_types = (
        db.query(models.Violation.violation_type, func.count(models.Violation.id))
        .group_by(models.Violation.violation_type)
        .all()
    )
    violations_by_type = {t: c for t, c in v_types}

    v_sev = (
        db.query(models.Violation.severity, func.count(models.Violation.id))
        .group_by(models.Violation.severity)
        .all()
    )
    violations_by_severity = {str(s): c for s, c in v_sev}

    r_dist = (
        db.query(models.RiskMatrix.risk_category, func.count(models.RiskMatrix.id))
        .group_by(models.RiskMatrix.risk_category)
        .all()
    )
    risk_distribution = {cat: cnt for cat, cnt in r_dist}

    return {
        "total_permits": total_permits or 0,
        "active_permits": active_permits or 0,
        "total_violations": total_violations or 0,
        "violations_by_type": violations_by_type,
        "violations_by_severity": violations_by_severity,
        "risk_distribution": risk_distribution,
    }