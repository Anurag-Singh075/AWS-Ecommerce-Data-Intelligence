from sqlalchemy.orm import Session
from backend.app.models.geolocation import Geolocation


def get_all_geolocations(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    zip_code: str | None = None,
    state: str | None = None
):
    query = db.query(Geolocation)

    if zip_code:
        query = query.filter(
            Geolocation.zip_code_prefix == zip_code
        )

    if state:
        query = query.filter(
            Geolocation.state == state.upper()
        )

    total = query.count()

    locations = (
        query
        .order_by(Geolocation.id)
        .offset(skip)
        .limit(limit)
        .all()
    )

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "locations": locations
    }