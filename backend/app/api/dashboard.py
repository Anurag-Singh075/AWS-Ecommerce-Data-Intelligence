from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.services.dashboard_service import get_dashboard_data

router = APIRouter(
    prefix="/api/v1/dashboard",
    tags=["Dashboard"]
)


@router.get("/")
def dashboard_overview(db: Session = Depends(get_db)):
    return get_dashboard_data(db)