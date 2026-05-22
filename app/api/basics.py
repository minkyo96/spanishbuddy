
from fastapi import APIRouter
from app.services.basics_service import basics_service_instance

router = APIRouter(prefix="/basics", tags=["Basics"])

@router.get("/guide")
async def get_basics_guide():
    return basics_service_instance.get_guide()
