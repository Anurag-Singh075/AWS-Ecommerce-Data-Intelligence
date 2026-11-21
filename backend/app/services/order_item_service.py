from sqlalchemy.orm import Session
from backend.app.models.order_item import OrderItem


def get_all_order_items(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    order_id: str | None = None,
    product_id: str | None = None,
    seller_id: str | None = None
):
    query = db.query(OrderItem)

    if order_id:
        query = query.filter(OrderItem.order_id == order_id)

    if product_id:
        query = query.filter(OrderItem.product_id == product_id)

    if seller_id:
        query = query.filter(OrderItem.seller_id == seller_id)

    total = query.count()

    items = (
        query
        .order_by(OrderItem.order_id, OrderItem.order_item_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "items": items
    }


def get_order_item_by_id(
    db: Session,
    order_id: str,
    order_item_id: int
):
    return (
        db.query(OrderItem)
        .filter(
            OrderItem.order_id == order_id,
            OrderItem.order_item_id == order_item_id
        )
        .first()
    )


def create_order_item(db: Session, item_data):
    item = OrderItem(**item_data.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item