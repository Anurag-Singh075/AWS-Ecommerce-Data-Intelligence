
from sqlalchemy import Column, String, Integer, DateTime, Numeric, ForeignKey
from backend.app.database import Base


class OrderItem(Base):
    __tablename__ = "order_items"

    order_id = Column(
        String(50),
        ForeignKey("orders.order_id"),
        primary_key=True
    )
    order_item_id = Column(Integer, primary_key=True)
    product_id = Column(String(50), nullable=False, index=True)
    seller_id = Column(String(50), nullable=False, index=True)
    shipping_limit_date = Column(DateTime, nullable=True)
    price = Column(Numeric(10, 2), nullable=False)
    freight_value = Column(Numeric(10, 2), nullable=False)
