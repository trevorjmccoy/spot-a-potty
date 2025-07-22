from sqlalchemy import CheckConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import Optional
    
class Base(DeclarativeBase):
    pass

class Restroom(Base):
    __tablename__ = 'restrooms'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    latitude: Mapped[float]
    longitude: Mapped[float]
    rating: Mapped[int]
    image_filename: Mapped[Optional[str]] = mapped_column(nullable=True, default=None)

    __table_args__ = (
        CheckConstraint("latitude BETWEEN -90 AND 90", name="check_latitude_range"),
        CheckConstraint("longitude BETWEEN -180 AND 180", name="check_longitude_range"),
        CheckConstraint("rating BETWEEN 1 AND 5", name="check_rating_range")
    )

    def __repr__(self):
        return (f"<Restroom id={self.id}, name={self.name}, "
                f"latitude={self.latitude}, longitude={self.longitude}, "
                f"rating={self.rating}, image filename={self.image_filename}>")