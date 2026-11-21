from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field


class PaymentCreate(BaseModel):
    order_id: str = Field(min_length=1, max_length=50)
    payment_sequential: int = Field(ge=1)
    payment_type: str = Field(min_length=1, max_length=30)
    payment_installments: int = Field(ge=0)
    payment_value: Decimal = Field(ge=0)


class PaymentResponse(BaseModel):
    order_id: str
    payment_sequential: int
    payment_type: str
    payment_installments: int
    payment_value: Decimal

    model_config = ConfigDict(from_attributes=True)