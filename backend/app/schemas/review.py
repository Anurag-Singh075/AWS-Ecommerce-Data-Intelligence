from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class ReviewCreate(BaseModel):
    review_id: str = Field(min_length=1, max_length=50)
    order_id: str = Field(min_length=1, max_length=50)
    review_score: int = Field(ge=1, le=5)
    title: str | None = None
    message: str | None = None
    review_creation_date: datetime | None = None
    review_answer_timestamp: datetime | None = None


class ReviewResponse(BaseModel):
    review_id: str
    order_id: str
    review_score: int
    title: str | None = None
    message: str | None = None
    review_creation_date: datetime | None = None
    review_answer_timestamp: datetime | None = None

    model_config = ConfigDict(from_attributes=True)