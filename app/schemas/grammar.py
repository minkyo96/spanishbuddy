from pydantic import BaseModel
from typing import List, Optional

class Example(BaseModel):
    es: str
    ko: str

class GrammarSection(BaseModel):
    heading: str
    content: str
    examples: List[Example]

class GrammarLesson(BaseModel):
    id: str
    title: str
    level: str
    description: str
    sections: List[GrammarSection]
