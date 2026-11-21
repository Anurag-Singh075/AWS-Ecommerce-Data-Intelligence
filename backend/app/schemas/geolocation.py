
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field


class GeolocationResponse(BaseModel):
    zip_code_prefix: str = Field(
        min_length=1,
        max_length=10,
        validation_alias="geolocation_zip_code_prefix"
    )
    lat: Decimal | None = Field(
        default=None,
        validation_alias="geolocation_lat"
    )
    lng: Decimal | None = Field(
        default=None,
        validation_alias="geolocation_lng"
    )
    city: str | None = Field(
        default=None,
        max_length=100,
        validation_alias="geolocation_city"
    )
    state: str | None = Field(
        default=None,
        max_length=5,
        validation_alias="geolocation_state"
    )

    model_config = ConfigDict(from_attributes=True)
