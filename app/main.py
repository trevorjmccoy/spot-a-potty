import uvicorn
from routes import router
from fastapi import FastAPI


# Create the FastAPI application
app = FastAPI()

# Register the API routes from routes.py
app.include_router(router)

if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)