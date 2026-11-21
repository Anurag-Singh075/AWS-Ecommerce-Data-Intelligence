from sqlalchemy.orm import Session
from backend.app.models.review import Review


def get_all_reviews(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    order_id: str | None = None,
    review_score: int | None = None
):
    query = db.query(Review)

    if order_id:
        query = query.filter(Review.order_id == order_id)

    if review_score:
        query = query.filter(Review.review_score == review_score)

    total = query.count()

    reviews = (
        query
        .order_by(Review.review_creation_date.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "reviews": reviews
    }


def get_review_by_id(
    db: Session,
    review_id: str,
    order_id: str
):
    return (
        db.query(Review)
        .filter(
            Review.review_id == review_id,
            Review.order_id == order_id
        )
        .first()
    )


def create_review(db: Session, review_data):
    review = Review(**review_data.model_dump())
    db.add(review)
    db.commit()
    db.refresh(review)
    return review