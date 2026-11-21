
from sqlalchemy import Column, Integer, String, Numeric
from backend.app.database import Base


class Geolocation(Base):
    __tablename__ = "geolocation"

    id = Column(Integer, primary_key=True, autoincrement=True)
    geolocation_zip_code_prefix = Column(String(10), index=True)
    geolocation_lat = Column(Numeric(10, 7))
    geolocation_lng = Column(Numeric(10, 7))
    geolocation_city = Column(String(100))
    geolocation_state = Column(String(2))
