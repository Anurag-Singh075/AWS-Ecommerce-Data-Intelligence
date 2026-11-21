from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from backend.app.database import get_db
from backend.app.schemas.order_item import OrderItemCreate, OrderItemResponse
from backend.app.services.order_item_service import (
    get_all_order_items,
    get_order_item_by_id,
    create_order_item
)

router = APIRouter(
    prefix="/api/v1/order-items",
    tags=["Order Items"]
)


@router.get("/")
def list_order_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    order_id: str | None = None,
    product_id: str | None = None,
    seller_id: str | None = None,
    db: Session = Depends(get_db)
):
    result = get_all_order_items(
        db=db,
        skip=skip,
        limit=limit,
        order_id=order_id,
        product_id=product_id,
        seller_id=seller_id
    )

    return {
        "total": result["total"],
        "skip": result["skip"],
        "limit": result["limit"],
        "order_items": [
            OrderItemResponse.model_validate(item)
            for item in result["items"]
        ]
    }


@router.get("/{order_id}/{order_item_id}", response_model=OrderItemResponse)
def order_item_detail(
    order_id: str,
    order_item_id: int,
    db: Session = Depends(get_db)
):
    item = get_order_item_by_id(db, order_id, order_item_id)

    if item is None:
        raise HTTPException(
            status_code=404,
            detail="Order item not found"
        )

    return item


@router.post(
    "/",
    response_model=OrderItemResponse,
    status_code=status.HTTP_201_CREATED
)
def add_order_item(
    item_data: OrderItemCreate,
    db: Session = Depends(get_db)
):
    try:
        return create_order_item(db, item_data)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Order item already exists or order does not exist"
        )