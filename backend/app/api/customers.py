
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from backend.app.database import get_db
from backend.app.schemas.customer import CustomerResponse, CustomerCreate
from backend.app.services.customer_service import (
    get_all_customers,
    get_customer_by_id,
    create_customer
)

router = APIRouter(
    prefix="/api/v1/customers",
    tags=["Customers"]
)


@router.get("/")
def list_customers(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    city: str | None = None,
    state: str | None = None,
    db: Session = Depends(get_db)
):
    result = get_all_customers(
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
        "customers": [
            CustomerResponse.model_validate(customer)
            for customer in result["customers"]
        ]
    }


@router.get("/{customer_id}", response_model=CustomerResponse)
def customer_detail(
    customer_id: str,
    db: Session = Depends(get_db)
):
    customer = get_customer_by_id(db, customer_id)

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return customer

@router.post("/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def add_customer(
    customer_data: CustomerCreate,
    db: Session = Depends(get_db)
):
    try:
        return create_customer(db, customer_data)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Customer ID already exists"
        )
