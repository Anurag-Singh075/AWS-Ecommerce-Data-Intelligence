from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class OrderCreate(BaseModel):
    order_id: str = Field(min_length=1, max_length=50)
    customer_id: str = Field(min_length=1, max_length=50)
    order_status: str = Field(min_length=1, max_length=30)

    order_purchase_timestamp: datetime
    order_approved_at: datetime | None = None
    order_delivered_carrier_date: datetime | None = None
    order_delivered_customer_date: datetime | None = None
    order_estimated_delivery_date: datetime | None = None


class OrderResponse(BaseModel):
    order_id: str
    customer_id: str
    order_status: str
    order_purchase_timestamp: datetime
    order_approved_at: datetime | None = None
    order_delivered_carrier_date: datetime | None = None
    order_delivered_customer_date: datetime | None = None
    order_estimated_delivery_date: datetime | None = None

    model_config = ConfigDict(from_attributes=True)