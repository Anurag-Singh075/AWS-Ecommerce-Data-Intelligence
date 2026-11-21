from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field


class ProductCreate(BaseModel):
    product_id: str = Field(min_length=1, max_length=50)
    product_category_name: str | None = Field(default=None, max_length=100)
    product_name_length: int | None = Field(default=None, ge=0)
    product_description_length: int | None = Field(default=None, ge=0)
    product_photos_qty: int | None = Field(default=None, ge=0)
    product_weight_g: Decimal | None = Field(default=None, ge=0)
    product_length_cm: Decimal | None = Field(default=None, ge=0)
    product_height_cm: Decimal | None = Field(default=None, ge=0)
    product_width_cm: Decimal | None = Field(default=None, ge=0)


class ProductResponse(BaseModel):
    product_id: str
    product_category_name: str | None = None
    product_name_length: int | None = None
    product_description_length: int | None = None
    product_photos_qty: int | None = None
    product_weight_g: Decimal | None = None
    product_length_cm: Decimal | None = None
    product_height_cm: Decimal | None = None
    product_width_cm: Decimal | None = None

    model_config = ConfigDict(from_attributes=True)