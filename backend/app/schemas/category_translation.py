from pydantic import BaseModel, ConfigDict, Field


class CategoryTranslationResponse(BaseModel):
    product_category_name: str = Field(min_length=1, max_length=100)
    product_category_name_english: str = Field(min_length=1, max_length=100)

    model_config = ConfigDict(from_attributes=True)