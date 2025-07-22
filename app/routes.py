from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import crud, schemas

# Create an API router
router = APIRouter()

# Create a new restroom
@router.post("/restrooms/", response_model=schemas.RestroomRead)
def create_restroom(restroom: schemas.RestroomCreate, db: Session = Depends(get_db)):
    return crud.create_restroom(db, restroom)

# Get all restrooms
@router.get("/restrooms/", response_model=List[schemas.RestroomRead])
def read_all_restrooms(db: Session = Depends(get_db)):
    return crud.read_all_restrooms(db)

# Get a restroom by its latitude and longitude
@router.get("/restrooms/by-location", response_model=schemas.RestroomRead)
def read_restroom_by_location(latitude: float, longitude: float, db: Session = Depends(get_db)):
    return crud.read_restroom_by_location(db, latitude, longitude)

# get a restroom by its ID
@router.get("/restrooms/{restroom_id}", response_model=schemas.RestroomRead)
def read_restroom_by_id(restroom_id: int, db: Session = Depends(get_db)):
    return crud.read_restroom_by_id(db, restroom_id)

# Update a restroom by its ID
@router.patch("/restrooms/{restroom_id}", response_model=schemas.RestroomRead)
def update_restroom_by_id(restroom_id: int, update_data: schemas.RestroomUpdate, db: Session = Depends(get_db)):
    return crud.update_restroom_by_id(db, restroom_id, update_data)

# Delete a restroom by its ID
@router.delete("/restrooms/{restroom_id}", response_model=schemas.RestroomRead)
def delete_restroom_by_id(restroom_id: int, db: Session = Depends(get_db)):
    return crud.delete_restroom_by_id(db, restroom_id)

