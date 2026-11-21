from sqlalchemy.orm import Session
from backend.app.models.order import Order

def get_all_orders(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    status: str | None = None,
    customer_id: str | None = None):
    query = db.query(Order)

    if status:
        query = query.filter(Order.order_status == status.lower())
    if customer_id:
        query = query.filter(Order.customer_id == customer_id)
    total = query.count()
    orders = (
        query
        .order_by(Order.order_purchase_timestamp.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "orders": orders
    }

def get_order_by_id(db: Session, order_id: str):
    return (
        db.query(Order)
        .filter(Order.order_id == order_id)
        .first()
    )

def create_order(db: Session, order_data):
    order = Order(**order_data.model_dump())
    db.add(order)
    db.commit()
    db.refresh(order)
    return order
