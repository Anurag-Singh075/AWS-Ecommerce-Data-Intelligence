from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from backend.app.database import get_db
from backend.app.schemas.review import ReviewCreate, ReviewResponse
from backend.app.services.review_service import (
    get_all_reviews,
    get_review_by_id,
    create_review
)

router = APIRouter(
    prefix="/api/v1/reviews",
    tags=["Reviews"]
)


@router.get("/")
def list_reviews(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    order_id: str | None = None,
    review_score: int | None = Query(None, ge=1, le=5),
    db: Session = Depends(get_db)
):
    result = get_all_reviews(
        db=db,
        skip=skip,
        limit=limit,
        order_id=order_id,
        review_score=review_score
    )

    return {
        "total": result["total"],
        "skip": result["skip"],
        "limit": result["limit"],
        "reviews": [
            ReviewResponse.model_validate(review)
            for review in result["reviews"]
        ]
    }


@router.get("/{review_id}/{order_id}", response_model=ReviewResponse)
def review_detail(
    review_id: str,
    order_id: str,
    db: Session = Depends(get_db)
):
    review = get_review_by_id(db, review_id, order_id)

    if review is None:
        raise HTTPException(
            status_code=404,
            detail="Review not found"
        )

    return review


@router.post(
    "/",
    response_model=ReviewResponse,
    status_code=status.HTTP_201_CREATED
)
def add_review(
    review_data: ReviewCreate,
    db: Session = Depends(get_db)
):
    try:
        return create_review(db, review_data)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Review already exists or order does not exist"
        )