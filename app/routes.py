from fastapi import APIRouter, Depends, Request
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
def create_restroom(form_data: RestroomForm = Depends(), db: Session = Depends(get_db)):
    # Convert form to Pydantic schema
    restroom_data = form_data.to_schema(filename_override=None)
    # Create restroom without image_filename
    created_restroom = crud.create_restroom(db, restroom_data)

    # Save image file (if present) with restroom id as its prefix
    if form_data.image_file:
        safe_filename = f"{created_restroom.id}_{os.path.basename(form_data.image_file.filename)}"
        image_path = os.path.join("app", "uploads", safe_filename)

        with open(image_path, "wb") as f:
            f.write(form_data.image_file.file.read())

        # Update just the image filename in the database
        crud.update_restroom_image_filename(db, created_restroom.id, safe_filename)

        # Update local return with image filename
        created_restroom.image_filename = safe_filename

    return created_restroom

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
def update_restroom_by_id(restroom_id: int, form_data: RestroomForm = Depends(), db: Session = Depends(get_db)):
    # Get current restroom record to access the image being replaced
    existing_restroom = crud.read_restroom_by_id(db, restroom_id)
    filename_override = None
    # If a new image is uploaded, delete the old one and save the new one
    if form_data.image_file:
        # Delete old image if it exists
        if existing_restroom.image_filename:
            safe_old_filename = os.path.basename(existing_restroom.image_filename)
            old_image_path = os.path.join("app", "uploads", safe_old_filename)
            if os.path.exists(old_image_path):
                os.remove(old_image_path)
            else:
                print("Old image file not found for deletion")

        # Save replacement image file
        safe_new_filename = f"{restroom_id}_{os.path.basename(form_data.image_file.filename)}"
        new_image_path = os.path.join("app", "uploads", safe_new_filename)
        with open(new_image_path, "wb") as f:
            f.write(form_data.image_file.file.read())

        filename_override = safe_new_filename
    # Build updated data
    restroom_data = form_data.to_schema(filename_override=filename_override)
    # Keep old image if no new one was uploaded
    if not filename_override:
        restroom_data.image_filename = existing_restroom.image_filename

    print("Final image_filename:", restroom_data.image_filename)

    return crud.update_restroom_by_id(db, restroom_id, restroom_data)

# Delete a restroom by its ID
@router.delete("/restrooms/{restroom_id}", response_model=schemas.RestroomRead)
def delete_restroom_by_id(restroom_id: int, db: Session = Depends(get_db)):
    restroom = crud.read_restroom_by_id(db, restroom_id)
    # Delete image file attached to restroom (if present)
    if restroom.image_filename:
        safe_filename = os.path.basename(restroom.image_filename)
        image_path = os.path.join("app", "uploads", safe_filename)
        if os.path.exists(image_path):
            os.remove(image_path)
        else:
            print("File does not exist at path.")

    return crud.delete_restroom_by_id(db, restroom_id)

