from geoalchemy2 import Geometry
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

from app.core.db.database import Base

Base = declarative_base()


class TitleBoundary(Base):
    """TitleBoundary model represents the boundary information of a title."""

    __tablename__ = "title_boundary"

    id = Column(String(255), primary_key=True)
    dataset = Column(String(255), nullable=False)
    end_date = Column(String(255), nullable=True)
    entity = Column(String(255), nullable=False)
    entry_date = Column(String(255), nullable=False)
    geometry = Column(
        Geometry(
            geometry_type="GEOMETRY",
            srid=4326,
            spatial_index=False,
            from_text="ST_GeomFromEWKT",
            name="geometry",
        ),
        nullable=True,
    )
    name = Column(String(255), nullable=True)
    organisation_entity = Column(String(255), nullable=True)
    point = Column(String, nullable=True)
    prefix = Column(String(255), nullable=True)
    reference = Column(String(255), nullable=True)
    start_date = Column(String(255), nullable=True)
    typology = Column(String(255), nullable=True)

    def as_dict(self) -> dict:
        """Convert the TitleBoundary instance to a dictionary."""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
