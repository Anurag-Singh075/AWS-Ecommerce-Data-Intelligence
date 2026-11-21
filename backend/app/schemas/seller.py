from pydantic import BaseModel, ConfigDict, Field


class SellerCreate(BaseModel):
    seller_id: str = Field(min_length=1, max_length=50)
    seller_zip_code_prefix: str | None = Field(default=None, max_length=10)
    seller_city: str | None = Field(default=None, max_length=100)
    seller_state: str | None = Field(default=None, max_length=5)


class SellerResponse(BaseModel):
    seller_id: str
    seller_zip_code_prefix: str | None = None
    seller_city: str | None = None
    seller_state: str | None = None

    model_config = ConfigDict(from_attributes=True)