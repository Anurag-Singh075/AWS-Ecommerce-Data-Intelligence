
from sqlalchemy import Column, String, Integer, DateTime, Text, ForeignKey
from backend.app.database import Base


class Review(Base):
    __tablename__ = "order_reviews"

    review_id = Column(String(50), primary_key=True)
    order_id = Column(
        String(50),
        ForeignKey("orders.order_id"),
        primary_key=True
    )
    review_score = Column(Integer, nullable=False)
    review_comment_title = Column(Text, nullable=True)
    review_comment_message = Column(Text, nullable=True)
    review_creation_date = Column(DateTime, nullable=True)
    review_answer_timestamp = Column(DateTime, nullable=True)
