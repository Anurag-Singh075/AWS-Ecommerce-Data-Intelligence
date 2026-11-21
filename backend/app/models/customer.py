from sqlalchemy import Column, String
from backend.app.database import Base
class Customer(Base):
    __tablename__ = "customers"
    customer_id = Column(String(50), primary_key=True, index=True)
    customer_unique_id = Column(String(50), nullable=False, index=True)
    customer_zip_code_prefix = Column(String(10))
    customer_city = Column(String(100))
    customer_state = Column(String(2))
