from sqlalchemy.orm import Session
from backend.app.models.payment import Payment


def get_all_payments(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    order_id: str | None = None,
    payment_type: str | None = None
):
    query = db.query(Payment)

    if order_id:
        query = query.filter(Payment.order_id == order_id)

    if payment_type:
        query = query.filter(
            Payment.payment_type == payment_type.lower()
        )

    total = query.count()

    payments = (
        query
        .order_by(Payment.order_id, Payment.payment_sequential)
        .offset(skip)
        .limit(limit)
        .all()
    )

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "payments": payments
    }


def get_payment_by_id(
    db: Session,
    order_id: str,
    payment_sequential: int
):
    return (
        db.query(Payment)
        .filter(
            Payment.order_id == order_id,
            Payment.payment_sequential == payment_sequential
        )
        .first()
    )


def create_payment(db: Session, payment_data):
    payment = Payment(**payment_data.model_dump())
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment