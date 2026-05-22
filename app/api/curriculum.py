
from fastapi import APIRouter, HTTPException
from app.services.curriculum_service import curriculum_service_instance
from app.schemas.curriculum import Curriculum

router = APIRouter(prefix="/curriculum", tags=["Curriculum"])

@router.get("/{month}", response_model=Curriculum)
async def get_month_curriculum(month: int):
    curriculum = curriculum_service_instance.get_curriculum(month)
    if not curriculum:
        raise HTTPException(status_code=404, detail="Curriculum for this month not found")
    return curriculum
