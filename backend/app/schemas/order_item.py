from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field


class OrderItemCreate(BaseModel):
    order_id: str = Field(min_length=1, max_length=50)
    order_item_id: int = Field(ge=1)
    product_id: str = Field(min_length=1, max_length=50)
    seller_id: str = Field(min_length=1, max_length=50)
    shipping_limit_date: datetime | None = None
    price: Decimal = Field(ge=0)
    freight_value: Decimal = Field(ge=0)


class OrderItemResponse(BaseModel):
    order_id: str
    order_item_id: int
    product_id: str
    seller_id: str
    shipping_limit_date: datetime | None = None
    price: Decimal
    freight_value: Decimal

    model_config = ConfigDict(from_attributes=True)