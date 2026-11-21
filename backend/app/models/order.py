from sqlalchemy import Column, String, DateTime, ForeignKey
from backend.app.database import Base
class Order(Base):
    __tablename__ = "orders"
    order_id = Column(String(50), primary_key=True, index=True)
    customer_id = Column(String(50),ForeignKey("customers.customer_id"),nullable=False,index=True)
    order_status = Column(String(30), nullable=False)
    order_purchase_timestamp = Column(DateTime, nullable=False)
    order_approved_at = Column(DateTime, nullable=True)
    order_delivered_carrier_date = Column(DateTime, nullable=True)
    order_delivered_customer_date = Column(DateTime, nullable=True)
    order_estimated_delivery_date = Column(DateTime, nullable=True)
