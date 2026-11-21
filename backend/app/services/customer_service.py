from sqlalchemy.orm import Session
from backend.app.models.customer import Customer

def get_all_customers(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    city: str | None = None,
    state: str | None = None
):
    query = db.query(Customer)

    if city:
        query = query.filter(
            Customer.customer_city.ilike(f"%{city}%")
        )

    if state:
        query = query.filter(
            Customer.customer_state == state.upper()
        )

    total = query.count()

    customers = (
        query
        .order_by(Customer.customer_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "customers": customers
    }

def get_customer_by_id(db: Session, customer_id: str):
    return (
        db.query(Customer)
        .filter(Customer.customer_id == customer_id)
        .first()
    )

def create_customer(db: Session, customer_data):
    customer = Customer(**customer_data.model_dump())

    db.add(customer)
    db.commit()
    db.refresh(customer)

    return customer
