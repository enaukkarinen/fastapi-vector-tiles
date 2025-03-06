from geoalchemy2 import WKBElement
from geoalchemy2.shape import to_shape
from pydantic import BaseModel, field_validator


class TitleBoundaryResponse(BaseModel):
    """TitleBoundaryResponse is a Pydantic model representing the response structure for title boundaries."""

    id: str
    dataset: str
    end_date: str | None
    entity: str
    entry_date: str
    name: str | None
    organisation_entity: str | None
    point: str | None
    prefix: str | None
    reference: str | None
    start_date: str | None
    typology: str | None
    geometry: str | None  # This will be the WKT string (Well-Known Text)

    class Config:
        """Enables compatibility with SQLAlchemy ORM models, allowing Pydantic to read data directly from them."""

        orm_mode = True  # Tells Pydantic to read data from SQLAlchemy models

    @field_validator("geometry", mode="before")
    def convert_geometry_to_wkt(cls, v: WKBElement | None) -> str | None:
        """Convert a WKBElement to a WKT string."""
        if isinstance(v, WKBElement):
            return to_shape(v).wkt
        return None
