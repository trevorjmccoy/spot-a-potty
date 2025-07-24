from fastapi import APIRouter, Body, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from schemas import RestroomForm
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import crud, schemas, os

# Create an API router
router = APIRouter()
# Mount Templates
templates = Jinja2Templates(directory="app/templates")

# Render map page
@router.get("/", response_class=HTMLResponse)
def index(request:Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Create a new restroom
@router.post("/restrooms/", response_model=schemas.RestroomRead)
def create_restroom(form_data: RestroomForm=Depends(), db: Session = Depends(get_db)):

    # Save uploaded file (if present)
    if form_data.image_file:
        with open(f"app/uploads/{form_data.image_file.filename}", "wb") as f:
            f.write(form_data.image_file.file.read())

    restroom = form_data.to_schema()
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
def delete_restroom_by_id(restroom_id: int, payload: dict = Body(...), db: Session = Depends(get_db)):
    # Delete image attached to restroom
    image_filename = payload.get("image_filename")
    if image_filename:
        safe_filename = os.path.basename(image_filename)
        image_path = os.path.join("app", "uploads", safe_filename)
        if os.path.exists(image_path):
            os.remove(image_path)
        else:
            print("File does not exist at path.")


    return crud.delete_restroom_by_id(db, restroom_id)

