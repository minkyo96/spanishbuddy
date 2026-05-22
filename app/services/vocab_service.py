
import json
import os
import random
from typing import List, Optional

class VocabService:
    def __init__(self, data_path: str = "data/vocab/words.json"):
        self.data_path = data_path

    def _load_words(self) -> List[dict]:
        with open(self.data_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_all_words(self) -> List[dict]:
        return self._load_words()

    def get_quiz_question(self, completed_groups: List[int] = None) -> dict:
        words = self._load_words()
        
        # Filter words based on completed groups
        if completed_groups is not None and len(completed_groups) > 0:
            filtered_words = []
            for group_idx in completed_groups:
                start = group_idx * 20
                end = start + 20
                filtered_words.extend(words[start:end])
            
            if not filtered_words:
                return {"error": "No words learned yet."}
            target_pool = filtered_words
        else:
            # If no groups completed, we can't generate a quiz based on learned words.
            # But for the first time, maybe we allow all or return error.
            # User request: "only within the range of learned words"
            return {"error": "Please mark at least one vocab group as completed to start the quiz!"}

        target = random.choice(target_pool)
        
        quiz_type = random.choice(["multiple_choice", "true_false", "spelling"])
        
        if quiz_type == "multiple_choice":
            others = [w for w in words if w['id'] != target['id']]
            wrong_options = random.sample(others, 3)
            options = wrong_options + [target]
            random.shuffle(options)
            return {
                "type": "multiple_choice",
                "question": target['es'],
                "correct_answer": target['ko'],
                "options": [opt['ko'] for opt in options],
                "example": target['example']
            }
        
        elif quiz_type == "true_false":
            is_correct = random.choice([True, False])
            display_ko = target['ko'] if is_correct else random.choice([w['ko'] for w in words if w['id'] != target['id']])
            return {
                "type": "true_false",
                "question": target['es'],
                "display_ko": display_ko,
                "correct_answer": "True" if is_correct else "False",
                "example": target['example']
            }
            
        elif quiz_type == "spelling":
            return {
                "type": "spelling",
                "question": target['ko'],
                "correct_answer": target['es'],
                "example": target['example']
            }

vocab_service_instance = VocabService()
