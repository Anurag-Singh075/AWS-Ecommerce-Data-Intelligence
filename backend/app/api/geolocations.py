from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.schemas.geolocation import GeolocationResponse
from backend.app.services.geolocation_service import get_all_geolocations

router = APIRouter(
    prefix="/api/v1/geolocations",
    tags=["Geolocation"]
)


@router.get("/")
def list_geolocations(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    zip_code: str | None = None,
    state: str | None = None,
    db: Session = Depends(get_db)
):
    result = get_all_geolocations(
        db=db,
        skip=skip,
        limit=limit,
        zip_code=zip_code,
        state=state
    )

    return {
        "total": result["total"],
        "skip": result["skip"],
        "limit": result["limit"],
        "locations": [
            GeolocationResponse.model_validate(location)
            for location in result["locations"]
        ]
    }