
from fastapi import APIRouter, HTTPException
from typing import List
from app.services.grammar_service import grammar_service_instance
from app.schemas.grammar import GrammarLesson

router = APIRouter(prefix="/grammar", tags=["Grammar"])

@router.get("/topics", response_model=List[dict])
async def list_grammar_topics():
    return grammar_service_instance.get_all_topics()

@router.get("/lesson/{lesson_id}", response_model=GrammarLesson)
async def get_grammar_lesson(lesson_id: str):
    lesson = grammar_service_instance.get_lesson(lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Grammar lesson not found")
    return lesson
