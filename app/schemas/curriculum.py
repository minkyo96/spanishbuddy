
from pydantic import BaseModel
from typing import List, Optional

class DayLesson(BaseModel):
    day: int
    topic: str
    lesson_id: str
    is_completed: bool = False
    estimated_minutes: Optional[int] = None
    objective: Optional[str] = None
    practice: Optional[str] = None
    checkpoints: Optional[List[str]] = None

class Week(BaseModel):
    week: int
    theme: str
    days: List[DayLesson]

class Curriculum(BaseModel):
    month: int
    title: str
    weeks: List[Week]
