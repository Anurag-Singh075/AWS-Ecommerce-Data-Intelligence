
from sqlalchemy import Column, String, Integer, Numeric, ForeignKey
from backend.app.database import Base


class Payment(Base):
    __tablename__ = "order_payments"

    order_id = Column(
        String(50),
        ForeignKey("orders.order_id"),
        primary_key=True
    )
    payment_sequential = Column(Integer, primary_key=True)
    payment_type = Column(String(30), nullable=False)
    payment_installments = Column(Integer, nullable=False)
    payment_value = Column(Numeric(10, 2), nullable=False)
