from fastapi import File, Form, UploadFile
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class RestroomCreate(BaseModel):
    name: str
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    rating: int = Field(ge=1, le=5)
    image_filename: Optional[str] = None

class RestroomRead(BaseModel):
    id: int
    name: str
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    rating: int = Field(ge=1, le=5)
    image_filename: Optional[str] = None

    # Enable ORM mode
    model_config = ConfigDict(from_attributes=True)

class RestroomUpdate(BaseModel):
    name: Optional[str] = None
    latitude: Optional[float] = Field(default=None, ge=-90, le=90)
    longitude: Optional[float] = Field(default=None, ge=-180, le=180)
    rating: Optional[int] = Field(default=None, ge=1, le=5)
    image_filename: Optional[str] = None


class RestroomForm:
    def __init__(
        self,
        name: str = Form(...),
        latitude: float = Form(...),
        longitude: float = Form(...),
        rating: int = Form(...),
        image_file: Optional[UploadFile] = File(None) # does this need Optional[...]?
    ):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.rating = rating
        self.image_file = image_file

    def to_schema(self):
        return RestroomCreate(
            name = self.name,
            latitude = self.latitude,
            longitude = self.longitude,
            rating = self.rating,
            image_filename = self.image_file.filename if self.image_file else None
        )
        