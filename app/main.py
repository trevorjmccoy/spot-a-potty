import uvicorn
from routes import router
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


# Create the FastAPI application
app = FastAPI()

# Mount uploads directory
app.mount("/uploads", StaticFiles(directory="app/uploads"), name="uploads")
# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Register the API routes from routes.py
app.include_router(router)

if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)