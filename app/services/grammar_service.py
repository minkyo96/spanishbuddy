
import json
import os
from typing import List, Optional
from app.schemas.grammar import GrammarLesson

class GrammarService:
    def __init__(self, data_dir: str = "data/grammar"):
        self.data_dir = data_dir

    def get_all_topics(self) -> List[dict]:
        topics = []
        if not os.path.exists(self.data_dir):
            return topics
        for filename in os.listdir(self.data_dir):
            if filename.endswith(".json"):
                with open(os.path.join(self.data_dir, filename), "r", encoding="utf-8") as f:
                    data = json.load(f)
                    topics.append({"id": data["id"], "title": data["title"], "level": data["level"]})
        return topics

    def get_lesson(self, lesson_id: str) -> Optional[GrammarLesson]:
        if not os.path.exists(self.data_dir):
            return None
        for filename in os.listdir(self.data_dir):
            if filename.endswith(".json"):
                with open(os.path.join(self.data_dir, filename), "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if data["id"] == lesson_id:
                        return GrammarLesson(**data)
        return None

grammar_service_instance = GrammarService()
