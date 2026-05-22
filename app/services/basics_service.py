
import json
import os
from typing import Optional

class BasicsService:
    def __init__(self, data_dir: str = "data/basics"):
        self.data_dir = data_dir

    def get_guide(self) -> Optional[dict]:
        file_path = os.path.join(self.data_dir, "guide.json")
        if not os.path.exists(file_path):
            return None
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

basics_service_instance = BasicsService()
