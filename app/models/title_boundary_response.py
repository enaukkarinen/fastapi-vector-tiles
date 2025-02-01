from pydantic import BaseModel, field_validator
from typing import Optional
from geoalchemy2 import WKBElement
from geoalchemy2.shape import to_shape  

class TitleBoundaryResponse(BaseModel):
    id: str
    dataset: str
    end_date: Optional[str]
    entity: str
    entry_date: str
    name: Optional[str]
    organisation_entity: Optional[str]
    point: Optional[str]
    prefix: Optional[str]
    reference: Optional[str]
    start_date: Optional[str]
    typology: Optional[str]
    geometry: Optional[str]  # This will be the WKT string (Well-Known Text)

    class Config:
        orm_mode = True  # This tells Pydantic to read data from SQLAlchemy models

    @field_validator("geometry", mode="before")
    def convert_geometry_to_wkt(cls, v):
        # Check if the value is a WKBElement (PostGIS geometry)
        if isinstance(v, WKBElement):
            return to_shape(v).wkt  # Convert to WKT string
        return None