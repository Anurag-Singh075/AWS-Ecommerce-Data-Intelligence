from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.schemas.category_translation import CategoryTranslationResponse
from backend.app.services.category_translation_service import get_all_categories

router = APIRouter(
    prefix="/api/v1/categories",
    tags=["Categories"]
)


@router.get("/")
def list_categories(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    search: str | None = None,
    db: Session = Depends(get_db)
):
    result = get_all_categories(
        db=db,
        skip=skip,
        limit=limit,
        search=search
    )

    return {
        "total": result["total"],
        "skip": result["skip"],
        "limit": result["limit"],
        "categories": [
            CategoryTranslationResponse.model_validate(category)
            for category in result["categories"]
        ]
    }