from sqlalchemy.orm import Session
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

def get_dashboard_data(db: Session):
    return {
        "overview": get_overview(db),
        "customer_analytics": get_customer_analytics(db),
        "order_status": get_order_status_distribution(db),
        "monthly_sales": get_monthly_sales(db),
        "payment_distribution": get_payment_distribution(db),
        "review_analysis": get_review_analysis(db),
        "top_products": get_top_selling_products(db, 10),
        "top_categories": get_top_categories(db, 10),
        "seller_performance": get_seller_performance(db, 10)
    }