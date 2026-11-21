from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.app.models.customer import Customer
from backend.app.models.order import Order
from backend.app.models.order_item import OrderItem
from backend.app.models.product import Product
from backend.app.models.seller import Seller
from backend.app.models.payment import Payment
from backend.app.models.review import Review


def get_overview(db: Session):

    total_customers = db.query(func.count(Customer.customer_id)).scalar()

    total_orders = db.query(func.count(Order.order_id)).scalar()

    total_products = db.query(func.count(Product.product_id)).scalar()

    total_sellers = db.query(func.count(Seller.seller_id)).scalar()

    total_order_items = db.query(func.count()).select_from(OrderItem).scalar()

    total_revenue = db.query(
        func.coalesce(func.sum(Payment.payment_value), 0)
    ).scalar()

    return {
        "total_customers": total_customers,
        "total_orders": total_orders,
        "total_products": total_products,
        "total_sellers": total_sellers,
        "total_order_items": total_order_items,
        "total_revenue": float(total_revenue)
    }


def get_order_status_distribution(db: Session):

    results = (
        db.query(
            Order.order_status,
            func.count(Order.order_id)
        )
        .group_by(Order.order_status)
        .all()
    )

    return [
        {
            "order_status": status,
            "total_orders": count
        }
        for status, count in results
    ]


def get_payment_distribution(db: Session):

    results = (
        db.query(
            Payment.payment_type,
            func.count(Payment.order_id),
            func.sum(Payment.payment_value)
        )
        .group_by(Payment.payment_type)
        .all()
    )

    return [
        {
            "payment_type": payment_type,
            "total_transactions": count,
            "total_amount": float(amount or 0)
        }
        for payment_type, count, amount in results
    ]


def get_review_analysis(db: Session):

    results = (
        db.query(
            Review.review_score,
            func.count(Review.review_id)
        )
        .group_by(Review.review_score)
        .order_by(Review.review_score)
        .all()
    )

    return [
        {
            "review_score": score,
            "total_reviews": count
        }
        for score, count in results
    ]

def get_monthly_sales(db: Session):

    results = (
        db.query(
            func.date_trunc(
                "month",
                Order.order_purchase_timestamp
            ).label("month"),
            func.count(func.distinct(Order.order_id)).label("total_orders"),
            func.coalesce(func.sum(Payment.payment_value), 0).label("revenue")
        )
        .join(Payment, Payment.order_id == Order.order_id)
        .group_by("month")
        .order_by("month")
        .all()
    )

    return [
        {
            "month": month.strftime("%Y-%m"),
            "total_orders": total_orders,
            "revenue": float(revenue)
        }
        for month, total_orders, revenue in results
    ]

def get_top_selling_products(db: Session, limit: int = 10):

    results = (
        db.query(
            OrderItem.product_id,
            Product.product_category_name,
            func.count(OrderItem.order_item_id).label("units_sold"),
            func.sum(OrderItem.price).label("total_sales")
        )
        .join(Product, Product.product_id == OrderItem.product_id)
        .group_by(
            OrderItem.product_id,
            Product.product_category_name
        )
        .order_by(func.count(OrderItem.order_item_id).desc())
        .limit(limit)
        .all()
    )

    return [
        {
            "product_id": product_id,
            "category": category,
            "units_sold": units_sold,
            "total_sales": float(total_sales or 0)
        }
        for product_id, category, units_sold, total_sales in results
    ]

def get_top_categories(db: Session, limit: int = 10):

    results = (
        db.query(
            Product.product_category_name,
            func.count(OrderItem.order_item_id).label("units_sold"),
            func.sum(OrderItem.price).label("total_sales")
        )
        .join(
            OrderItem,
            OrderItem.product_id == Product.product_id
        )
        .filter(Product.product_category_name.isnot(None))
        .group_by(Product.product_category_name)
        .order_by(func.count(OrderItem.order_item_id).desc())
        .limit(limit)
        .all()
    )

    return [
        {
            "category": category,
            "units_sold": units_sold,
            "total_sales": float(total_sales or 0)
        }
        for category, units_sold, total_sales in results
    ]

def get_customer_analytics(db: Session):

    total_customers = (
        db.query(
            func.count(func.distinct(Customer.customer_unique_id))
        ).scalar()
    )

    customer_order_counts = (
        db.query(
            Customer.customer_unique_id,
            func.count(Order.order_id).label("total_orders")
        )
        .join(Order, Order.customer_id == Customer.customer_id)
        .group_by(Customer.customer_unique_id)
        .subquery()
    )

    repeat_customers = (
        db.query(func.count())
        .select_from(customer_order_counts)
        .filter(customer_order_counts.c.total_orders > 1)
        .scalar()
    )

    total_customer_orders = (
        db.query(func.count(Order.order_id)).scalar()
    )

    return {
        "total_unique_customers": total_customers,
        "repeat_customers": repeat_customers,
        "one_time_customers": total_customers - repeat_customers,
        "total_orders": total_customer_orders
    }
def get_seller_performance(db: Session, limit: int = 10):

    results = (
        db.query(
            Seller.seller_id,
            Seller.seller_city,
            Seller.seller_state,
            func.count(OrderItem.order_item_id).label("total_items_sold"),
            func.count(func.distinct(OrderItem.order_id)).label("total_orders"),
            func.sum(OrderItem.price).label("total_sales")
        )
        .join(OrderItem, OrderItem.seller_id == Seller.seller_id)
        .group_by(
            Seller.seller_id,
            Seller.seller_city,
            Seller.seller_state
        )
        .order_by(func.sum(OrderItem.price).desc())
        .limit(limit)
        .all()
    )

    return [
        {
            "seller_id": seller_id,
            "city": city,
            "state": state,
            "total_items_sold": items_sold,
            "total_orders": total_orders,
            "total_sales": float(total_sales or 0)
        }
        for seller_id, city, state, items_sold, total_orders, total_sales in results
    ]