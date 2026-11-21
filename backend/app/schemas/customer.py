from pydantic import BaseModel, ConfigDict, Field


class CustomerCreate(BaseModel):
    customer_id: str = Field(min_length=1, max_length=50)
    customer_unique_id: str = Field(min_length=1, max_length=50)
    customer_zip_code_prefix: str | None = Field(default=None, max_length=10)
    customer_city: str | None = Field(default=None, max_length=100)
    customer_state: str | None = Field(default=None, max_length=5)


class CustomerResponse(BaseModel):
    customer_id: str
    customer_unique_id: str
    customer_zip_code_prefix: str | None = None
    customer_city: str | None = None
    customer_state: str | None = None

    model_config = ConfigDict(from_attributes=True)