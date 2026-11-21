from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from backend.app.database import get_db
from backend.app.schemas.seller import SellerCreate, SellerResponse
from backend.app.services.seller_service import (
    get_all_sellers,
    get_seller_by_id,
    create_seller
)

router = APIRouter(
    prefix="/api/v1/sellers",
    tags=["Sellers"]
)


@router.get("/")
def list_sellers(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    city: str | None = None,
    state: str | None = None,
    db: Session = Depends(get_db)
):
    result = get_all_sellers(
        db=db,
        skip=skip,
        limit=limit,
        city=city,
        state=state
    )

    return {
        "total": result["total"],
        "skip": result["skip"],
        "limit": result["limit"],
        "sellers": [
            SellerResponse.model_validate(seller)
            for seller in result["sellers"]
        ]
    }


@router.get("/{seller_id}", response_model=SellerResponse)
def seller_detail(
    seller_id: str,
    db: Session = Depends(get_db)
):
    seller = get_seller_by_id(db, seller_id)

    if seller is None:
        raise HTTPException(
            status_code=404,
            detail="Seller not found"
        )

    return seller


@router.post(
    "/",
    response_model=SellerResponse,
    status_code=status.HTTP_201_CREATED
)
def add_seller(
    seller_data: SellerCreate,
    db: Session = Depends(get_db)
):
    try:
        return create_seller(db, seller_data)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Seller ID already exists"
        )