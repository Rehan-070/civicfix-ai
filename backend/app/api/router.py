from fastapi import APIRouter
from app.api.endpoints import auth, issues, complaints, dashboard, map, admin, demo_api

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(issues.router, prefix="/issues", tags=["Issues"])
api_router.include_router(complaints.router, prefix="/complaints", tags=["Complaints"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
api_router.include_router(map.router, prefix="/map", tags=["Map"])
api_router.include_router(admin.router, prefix="/admin", tags=["Admin Control Panel"])

# Clearly separated Demo Civic API routes
api_router.include_router(demo_api.router, prefix="/demo", tags=["CivicFix Demo Civic API — Simulation Only"])
