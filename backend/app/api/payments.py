from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from backend.app.database import get_db
from backend.app.schemas.payment import PaymentCreate, PaymentResponse
from backend.app.services.payment_service import (
    get_all_payments,
    get_payment_by_id,
    create_payment
)

router = APIRouter(
    prefix="/api/v1/payments",
    tags=["Payments"]
)


@router.get("/")
def list_payments(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    order_id: str | None = None,
    payment_type: str | None = None,
    db: Session = Depends(get_db)
):
    result = get_all_payments(
        db=db,
        skip=skip,
        limit=limit,
        order_id=order_id,
        payment_type=payment_type
    )

    return {
        "total": result["total"],
        "skip": result["skip"],
        "limit": result["limit"],
        "payments": [
            PaymentResponse.model_validate(payment)
            for payment in result["payments"]
        ]
    }


@router.get("/{order_id}/{payment_sequential}", response_model=PaymentResponse)
def payment_detail(
    order_id: str,
    payment_sequential: int,
    db: Session = Depends(get_db)
):
    payment = get_payment_by_id(
        db,
        order_id,
        payment_sequential
    )

    if payment is None:
        raise HTTPException(
            status_code=404,
            detail="Payment not found"
        )

    return payment


@router.post(
    "/",
    response_model=PaymentResponse,
    status_code=status.HTTP_201_CREATED
)
def add_payment(
    payment_data: PaymentCreate,
    db: Session = Depends(get_db)
):
    try:
        return create_payment(db, payment_data)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Payment already exists or order does not exist"
        )