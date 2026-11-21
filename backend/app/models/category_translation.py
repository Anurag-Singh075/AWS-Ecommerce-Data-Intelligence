from sqlalchemy import Column, String
from backend.app.database import Base
class CategoryTranslation(Base):
    __tablename__ = "category_translations"
    product_category_name = Column(String(100), primary_key=True)
    product_category_name_english = Column(String(100), nullable=False)
