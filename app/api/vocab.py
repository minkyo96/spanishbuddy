
from fastapi import APIRouter, Query
from app.services.vocab_service import vocab_service_instance
from typing import List, Optional

router = APIRouter(prefix="/vocab", tags=["Vocabulary"])

@router.get("/list")
async def get_vocab_list():
    return vocab_service_instance.get_all_words()

@router.get("/quiz")
async def get_quiz_question(
    completed_groups: List[int] = Query(None),
    difficulty: Optional[str] = Query("medium")
):
    # FastAPI handles comma-separated lists in query params automatically if type is List[int]
    # Example: /vocab/quiz?completed_groups=0&completed_groups=1
    result = vocab_service_instance.get_quiz_question(completed_groups, difficulty)
    return result
