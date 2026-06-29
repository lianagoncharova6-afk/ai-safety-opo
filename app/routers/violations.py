from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas

router = APIRouter()

@router.get("/", response_model=list[schemas.ViolationOut])
def list_violations(
    permit_id: Optional[int] = None,
    status: Optional[str] = Query(None, pattern=r"^(new|acknowledged|resolved|false_alarm)$"),
    db: Session = Depends(get_db),
):
    return crud.get_violations(db, permit_id=permit_id, status=status)

@router.post("/", response_model=schemas.ViolationOut, status_code=201)
def report_violation(data: schemas.ViolationCreate, db: Session = Depends(get_db)):
    return crud.create_violation(db, data)

@router.post("/{violation_id}/resolve", response_model=schemas.ViolationOut)
def resolve_violation(violation_id: int, notes: str = "", db: Session = Depends(get_db)):
    obj = crud.resolve_violation(db, violation_id, notes)
    if not obj:
        raise HTTPException(status_code=404, detail="Нарушение не найдено")
    return obj

@router.post("/ai-scan/{permit_id}")
def ai_scan_permit(permit_id: int, db: Session = Depends(get_db)):
    permit = crud.get_work_permit(db, permit_id)
    if not permit:
        raise HTTPException(status_code=404, detail="Наряд-допуск не найден")
    if permit.status != "active":
        raise HTTPException(status_code=400, detail="Наряд-допуск не активен")
    from app.services.ai_vision import simulate_ai_scan
    violations_found = simulate_ai_scan(db, permit_id)
    return {
        "message": f"AI-сканирование завершено. Обнаружено нарушений: {len(violations_found)}",
        "violations": violations_found,
    }
