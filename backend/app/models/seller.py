
from sqlalchemy import Column, String
from backend.app.database import Base
class Seller(Base):
    __tablename__ = "sellers"

    seller_id = Column(String(50), primary_key=True, index=True)
    seller_zip_code_prefix = Column(String(10))
    seller_city = Column(String(100))
    seller_state = Column(String(2))
