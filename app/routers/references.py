from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas

router = APIRouter()

@router.post("/employees", response_model=schemas.EmployeeOut, status_code=201)
def add_employee(data: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    return crud.create_employee(db, data)

@router.get("/ppe", response_model=list[schemas.PpeOut])
def list_ppe(db: Session = Depends(get_db)):
    return crud.get_all_ppe(db)

@router.post("/ppe", response_model=schemas.PpeOut, status_code=201)
def add_ppe(data: schemas.PpeCreate, db: Session = Depends(get_db)):
    return crud.create_ppe(db, data)

@router.get("/equipment", response_model=list[schemas.EquipmentOut])
def list_equipment(db: Session = Depends(get_db)):
    return crud.get_all_equipment(db)

@router.post("/equipment", response_model=schemas.EquipmentOut, status_code=201)
def add_equipment(data: schemas.EquipmentCreate, db: Session = Depends(get_db)):
    return crud.create_equipment(db, data)

@router.get("/safety-signs", response_model=list[schemas.SafetySignOut])
def list_safety_signs(db: Session = Depends(get_db)):
    return crud.get_all_safety_signs(db)

@router.post("/safety-signs", response_model=schemas.SafetySignOut, status_code=201)
def add_safety_sign(data: schemas.SafetySignCreate, db: Session = Depends(get_db)):
    return crud.create_safety_sign(db, data)

@router.get("/activity-types", response_model=list[schemas.ActivityTypeOut])
def list_activity_types(db: Session = Depends(get_db)):
    return crud.get_all_activity_types(db)

@router.post("/activity-types", response_model=schemas.ActivityTypeOut, status_code=201)
def add_activity_type(data: schemas.ActivityTypeCreate, db: Session = Depends(get_db)):
    return crud.create_activity_type(db, data)

@router.get("/checklist-items", response_model=list[schemas.ChecklistItemOut])
def list_checklist_items(db: Session = Depends(get_db)):
    return crud.get_checklist_items(db)

@router.post("/checklist-items", response_model=schemas.ChecklistItemOut, status_code=201)
def add_checklist_item(data: schemas.ChecklistItemCreate, db: Session = Depends(get_db)):
    return crud.create_checklist_item(db, data)
