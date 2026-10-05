import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database import engine, Base
from app.api.router import api_router
from seed_data import seed_database

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AI-powered multi-agent civic issue reporting, tracking, escalation, and resolution-verification platform."
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure upload directory exists & mount static files
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    seed_database()

@app.get("/")
def root():
    return {
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "demo_mode": settings.DEMO_MODE,
        "gateway": "CivicFix Demo Civic API — Simulation Only",
        "docs_url": "/docs"
    }

app.include_router(api_router, prefix=settings.API_V1_STR)
