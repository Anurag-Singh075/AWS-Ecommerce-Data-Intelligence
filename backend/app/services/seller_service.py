from sqlalchemy.orm import Session
from backend.app.models.seller import Seller


def get_all_sellers(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    city: str | None = None,
    state: str | None = None
):
    query = db.query(Seller)

    if city:
        query = query.filter(
            Seller.seller_city.ilike(f"%{city}%")
        )

    if state:
        query = query.filter(
            Seller.seller_state == state.upper()
        )

    total = query.count()

    sellers = (
        query
        .order_by(Seller.seller_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "sellers": sellers
    }


def get_seller_by_id(db: Session, seller_id: str):
    return (
        db.query(Seller)
        .filter(Seller.seller_id == seller_id)
        .first()
    )


def create_seller(db: Session, seller_data):
    seller = Seller(**seller_data.model_dump())
    db.add(seller)
    db.commit()
    db.refresh(seller)
    return seller