from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas

router = APIRouter()

@router.get("/stats", response_model=schemas.DashboardStats)
def get_stats(db: Session = Depends(get_db)):
    data = crud.get_dashboard_stats(db)
    return schemas.DashboardStats(**data)

@router.get("/violations-by-date")
def violations_by_date(db: Session = Depends(get_db)):
    from sqlalchemy import func
    from app.models import Violation
    from datetime import datetime, timedelta
    cutoff = datetime.utcnow() - timedelta(days=30)
    results = (
        db.query(func.date(Violation.detected_at), func.count(Violation.id))
        .filter(Violation.detected_at >= cutoff)
        .group_by(func.date(Violation.detected_at))
        .order_by(func.date(Violation.detected_at))
        .all()
    )
    return [{"date": str(d), "count": c} for d, c in results]
