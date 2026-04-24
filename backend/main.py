# FastAPI core framework and middleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database import engine, Base
import backend.models
from backend.routes.admin import router as admin_router

# OS for optional static file serving (not required but kept for flexibility)
import os

'''
Entry point of the Smart Seat Allocation Platform.
Responsible for:
- Initialising FastAPI app
- Configuring middleware (CORS)
- Creating database tables
- Exposing API entry point
'''

# Create FastAPI app instance
app = FastAPI(
    title="Smart Seat Allocation Platform",
    description="Automated training session seat allocation system",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow frontend access (JS/HTML)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {
        "message": "Smart Seat Allocation API is running"
    }