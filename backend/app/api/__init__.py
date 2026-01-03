"""API routes module"""
from fastapi import APIRouter
from app.api import risk

api_router = APIRouter()

# Include route modules
api_router.include_router(risk.router)

@api_router.get("/")
async def api_root():
    """API root endpoint"""
    return {"message": "FESE API v1"}
