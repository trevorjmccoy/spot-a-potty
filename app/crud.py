from models import Restroom
from schemas import RestroomCreate, RestroomUpdate
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session


def create_restroom(db: Session, restroom: RestroomCreate):
    # Convert from Pydantic to SQLAlchemy
    new_restroom = Restroom(**restroom.model_dump())

    db.add(new_restroom)
    db.commit()
    # Updates restroom with auto-generated id
    db.refresh(new_restroom)

    return new_restroom


def read_all_restrooms(db: Session):
    
    return db.execute(select(Restroom)).scalars().all()


def read_restroom_by_id(db: Session, restroom_id: int):
    # Retrieve restroom by its id
    restroom = db.execute(select(Restroom).where(Restroom.id == restroom_id)).scalars().first()

    if not restroom:
        raise HTTPException(status_code=404, detail="Restroom not found")
    
    return restroom


def read_restroom_by_location(db: Session, longitude: float, latitude: float):
    # Retrieve restroom by its location (latitude and longitude)
    restroom = db.execute(select(Restroom).where(Restroom.longitude == longitude, Restroom.latitude == latitude)).scalars().first()

    if not restroom:
        raise HTTPException(status_code=404, detail="Restroom not found")
    
    return restroom


def update_restroom_by_id(db: Session, restroom_id: int, update_data: RestroomUpdate):
    # Retrieve restroom by its id
    restroom = db.execute(select(Restroom).where(Restroom.id == restroom_id)).scalars().first()

    if not restroom:
        raise HTTPException(status_code=404, detail="Restroom not found")
    
    # Update only the included fields (fields that are not None)
    update_fields = {
        attr: value for attr, value in update_data.model_dump(exclude_unset=True).items()
        if value is not None
    }

    for attr, value in update_fields.items():
        setattr(restroom, attr, value)

    db.commit()
    db.refresh(restroom)

    return restroom

# Add restroom id before image filename to decrease risk of multiples
def update_restroom_image_filename(db: Session, restroom_id: int, filename: str):
    restroom = db.get(Restroom, restroom_id)
    if not restroom:
        raise ValueError(f"Restroom with ID {restroom_id} not found")
    restroom.image_filename = filename
    db.commit()
    db.refresh(restroom)
    return restroom


def delete_restroom_by_id(db: Session, restroom_id: int):
    # Retrieve restroom by its id
    restroom = db.execute(select(Restroom).where(Restroom.id == restroom_id)).scalars().first()

    if not restroom:
        raise HTTPException(status_code=404, detail="Restroom not found")

    # Delete the record from the session
    db.delete(restroom)
    db.commit()


    return restroom