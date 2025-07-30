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
        name: Optional[str] = Form(None),
        latitude: Optional[float] = Form(None),
        longitude: Optional[float] = Form(None),
        rating: Optional[str] = Form(None),
        image_file: Optional[UploadFile] = File(None)
    ):
        # Convert blank strings from empty form data to None 
        self.name = name.strip() if name not in (None, "", "null") else None
        self.latitude = float(latitude) if latitude not in (None, "", "null") else None
        self.longitude = float(longitude) if longitude not in (None, "", "null") else None
        self.rating = int(rating) if rating and str(rating).strip().isdigit() else None
        self.image_file = image_file if image_file and image_file.filename else None

    def to_schema(self, filename_override: Optional[str] = None):
        return RestroomUpdate(
            name = self.name,
            latitude = self.latitude,
            longitude = self.longitude,
            rating = self.rating,
            image_filename = filename_override # Only set if a new image is uploaded
        )
        