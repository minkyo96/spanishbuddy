
import json
import os
from typing import Optional
from app.schemas.curriculum import Curriculum

class CurriculumService:
    def __init__(self, data_dir: str = "data/curriculum"):
        self.data_dir = data_dir

    def get_curriculum(self, month: int = 1) -> Optional[Curriculum]:
        file_path = os.path.join(self.data_dir, f"month{month}.json")
        if not os.path.exists(file_path):
            return None
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return Curriculum(**data)

curriculum_service_instance = CurriculumService()
