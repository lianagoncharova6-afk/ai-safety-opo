from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas

router = APIRouter()

@router.get("/", response_model=list[schemas.WorkPermitOut])
def list_permits(
    status: Optional[str] = Query(None, pattern=r"^(draft|active|suspended|closed)$"),
    db: Session = Depends(get_db),
):
    return crud.get_work_permits(db, status=status)

@router.get("/{permit_id}", response_model=schemas.WorkPermitOut)
def get_permit(permit_id: int, db: Session = Depends(get_db)):
    obj = crud.get_work_permit(db, permit_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Наряд-допуск не найден")
    return obj

@router.post("/", response_model=schemas.WorkPermitOut, status_code=201)
def create_permit(data: schemas.WorkPermitCreate, db: Session = Depends(get_db)):
    return crud.create_work_permit(db, data)

@router.patch("/{permit_id}", response_model=schemas.WorkPermitOut)
def update_permit(permit_id: int, data: schemas.WorkPermitUpdate, db: Session = Depends(get_db)):
    obj = crud.update_work_permit(db, permit_id, data)
    if not obj:
        raise HTTPException(status_code=404, detail="Наряд-допуск не найден")
    return obj

@router.post("/{permit_id}/activate", response_model=schemas.WorkPermitOut)
def activate_permit(permit_id: int, db: Session = Depends(get_db)):
    obj = crud.update_work_permit(db, permit_id, schemas.WorkPermitUpdate(status="active"))
    if not obj:
        raise HTTPException(status_code=404, detail="Наряд-допуск не найден")
    return obj

@router.post("/{permit_id}/close", response_model=schemas.WorkPermitOut)
def close_permit(permit_id: int, db: Session = Depends(get_db)):
    obj = crud.close_work_permit(db, permit_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Наряд-допуск не найден или уже закрыт")
    return obj
