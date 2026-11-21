from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from backend.app.database import get_db
from backend.app.schemas.product import ProductCreate, ProductResponse
from backend.app.services.product_service import (
    get_all_products,
    get_product_by_id,
    create_product
)

router = APIRouter(
    prefix="/api/v1/products",
    tags=["Products"]
)


@router.get("/")
def list_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    category: str | None = None,
    db: Session = Depends(get_db)
):
    result = get_all_products(
        db=db,
        skip=skip,
        limit=limit,
        category=category
    )

    return {
        "total": result["total"],
        "skip": result["skip"],
        "limit": result["limit"],
        "products": [
            ProductResponse.model_validate(product)
            for product in result["products"]
        ]
    }


@router.get("/{product_id}", response_model=ProductResponse)
def product_detail(
    product_id: str,
    db: Session = Depends(get_db)
):
    product = get_product_by_id(db, product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product


@router.post(
    "/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED
)
def add_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db)
):
    try:
        return create_product(db, product_data)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Product ID already exists"
        )