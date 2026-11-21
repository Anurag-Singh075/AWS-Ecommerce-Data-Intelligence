from sqlalchemy.orm import Session
from backend.app.models.product import Product


def get_all_products(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    category: str | None = None
):
    query = db.query(Product)

    if category:
        query = query.filter(
            Product.product_category_name.ilike(f"%{category}%")
        )

    total = query.count()

    products = (
        query
        .order_by(Product.product_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "products": products
    }


def get_product_by_id(db: Session, product_id: str):
    return (
        db.query(Product)
        .filter(Product.product_id == product_id)
        .first()
    )


def create_product(db: Session, product_data):
    product = Product(**product_data.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product