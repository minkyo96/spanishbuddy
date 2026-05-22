
from pydantic import BaseModel
from typing import List

class DayLesson(BaseModel):
    day: int
    topic: str
    lesson_id: str
    is_completed: bool = False

class Week(BaseModel):
    week: int
    theme: str
    days: List[DayLesson]

class Curriculum(BaseModel):
    month: int
    title: str
    weeks: List[Week]
