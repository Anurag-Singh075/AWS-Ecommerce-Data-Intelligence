from sqlalchemy.orm import Session
from backend.app.models.category_translation import CategoryTranslation


def get_all_categories(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    search: str | None = None
):
    query = db.query(CategoryTranslation)

    if search:
        query = query.filter(
            CategoryTranslation.product_category_name_english.ilike(
                f"%{search}%"
            )
        )

    total = query.count()

    categories = (
        query
        .order_by(CategoryTranslation.product_category_name_english)
        .offset(skip)
        .limit(limit)
        .all()
    )

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "categories": categories
    }