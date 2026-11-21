
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.services.analytics_service import (
    get_overview,
    get_order_status_distribution,
    get_payment_distribution,
    get_review_analysis,
    get_monthly_sales,
    get_top_selling_products,
    get_top_categories,
    get_customer_analytics,
    get_seller_performance
)

router = APIRouter(
    prefix="/api/v1/analytics",
    tags=["Analytics"]
)


@router.get("/overview")
def analytics_overview(db: Session = Depends(get_db)):
    return get_overview(db)


@router.get("/order-status")
def order_status_analytics(db: Session = Depends(get_db)):
    return get_order_status_distribution(db)


@router.get("/payments")
def payment_analytics(db: Session = Depends(get_db)):
    return get_payment_distribution(db)


@router.get("/reviews")
def review_analytics(db: Session = Depends(get_db)):
    return get_review_analysis(db)


@router.get("/monthly-sales")
def monthly_sales_analytics(db: Session = Depends(get_db)):
    return get_monthly_sales(db)


@router.get("/top-products")
def top_products_analytics(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    return get_top_selling_products(db, limit)


@router.get("/top-categories")
def top_categories_analytics(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    return get_top_categories(db, limit)


@router.get("/customers")
def customer_analytics(db: Session = Depends(get_db)):
    return get_customer_analytics(db)


@router.get("/seller-performance")
def seller_performance_analytics(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    return get_seller_performance(db, limit)
