
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from backend.app.database import get_db

router = APIRouter(
    prefix="/api/v1/health",
    tags=["Health"]
)


@router.get("/database")
def database_health(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected",
            "message": "PostgreSQL connection is working"
        }

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Database connection failed"
        )
