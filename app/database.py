from models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Note to self - For SQLite, the connect_args={"check_same_thread": False} is necessary because SQLite is not fully thread-safe by default. This option tells SQLite that it's OK for our app to share the connection.
engine = create_engine("sqlite:///restrooms.db", connect_args={"check_same_thread": False}, echo=True)
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)

# Set up dependency injection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()