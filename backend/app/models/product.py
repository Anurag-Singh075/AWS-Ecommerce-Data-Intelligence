
from sqlalchemy import Column, String, Integer, Numeric
from backend.app.database import Base


class Product(Base):
    __tablename__ = "products"

    product_id = Column(String(50), primary_key=True, index=True)
    product_category_name = Column(String(100), nullable=True)
    product_name_length = Column(Integer, nullable=True)
    product_description_length = Column(Integer, nullable=True)
    product_photos_qty = Column(Integer, nullable=True)
    product_weight_g = Column(Numeric(10, 2), nullable=True)
    product_length_cm = Column(Numeric(10, 2), nullable=True)
    product_height_cm = Column(Numeric(10, 2), nullable=True)
    product_width_cm = Column(Numeric(10, 2), nullable=True)
