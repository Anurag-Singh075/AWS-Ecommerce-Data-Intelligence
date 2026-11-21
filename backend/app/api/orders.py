from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from backend.app.database import get_db
from backend.app.schemas.order import OrderCreate, OrderResponse
from backend.app.services.order_service import (
    get_all_orders,
    get_order_by_id,
    create_order
)

router = APIRouter(prefix="/api/v1/orders",tags=["Orders"])

@router.get("/")
def list_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    order_status: str | None = None,
    customer_id: str | None = None,
    db: Session = Depends(get_db)
):
    result = get_all_orders(
        db=db,
        skip=skip,
        limit=limit,
        status=order_status,
        customer_id=customer_id
    )

    return {
        "total": result["total"],
        "skip": result["skip"],
        "limit": result["limit"],
        "orders": [
            OrderResponse.model_validate(order)
            for order in result["orders"]
        ]
    }

@router.get("/{order_id}", response_model=OrderResponse)
def order_detail(
    order_id: str,
    db: Session = Depends(get_db)
    ):
    order = get_order_by_id(db, order_id)
    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return order


@router.post(
    "/",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED
)
def add_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db)
):
    try:
        return create_order(db, order_data)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Order already exists or customer does not exist"
        )
