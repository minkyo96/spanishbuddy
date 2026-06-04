
import json
import os
import random
import re
from typing import List, Optional

class VocabService:
    def __init__(self, data_path: str = "data/vocab/words.json"):
        self.data_path = data_path

    def _normalize_difficulty(self, difficulty: Optional[str]) -> str:
        if difficulty in {"easy", "medium", "hard"}:
            return difficulty
        return "medium"

    def _rank_distractors(self, candidates: List[dict], target: dict, difficulty: str) -> List[dict]:
        if difficulty == "easy":
            shuffled = candidates[:]
            random.shuffle(shuffled)
            return shuffled

        target_category = target.get("category")
        target_len = len(target.get("es", ""))
        target_prefix = target.get("es", "")[:1].lower()

        def sort_key(word: dict):
            same_category = 0 if word.get("category") == target_category else 1
            length_diff = abs(len(word.get("es", "")) - target_len)
            same_prefix = 0 if word.get("es", "")[:1].lower() == target_prefix else 1

            if difficulty == "medium":
                return (same_category, length_diff, random.random())

            # hard
            return (same_category, length_diff, same_prefix, random.random())

        ranked = sorted(candidates, key=sort_key)
        # Keep the pool plausible but still varied.
        return ranked[: min(len(ranked), 12 if difficulty == "medium" else 8)]

    def _pick_wrong_options(self, words: List[dict], target: dict, difficulty: str, count: int = 3) -> List[dict]:
        candidates = [w for w in words if w["id"] != target["id"]]
        difficulty = self._normalize_difficulty(difficulty)

        if difficulty == "easy":
            pool = candidates
        else:
            same_category = [w for w in candidates if w.get("category") == target.get("category")]
            pool = same_category if len(same_category) >= count else candidates
            pool = self._rank_distractors(pool, target, difficulty)

        if len(pool) < count:
            pool = candidates

        return random.sample(pool, count)

    def _load_words(self) -> List[dict]:
        with open(self.data_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _tokenize_sentence(self, sentence: str) -> List[str]:
        return [token for token in sentence.split() if token]

    def _blank_target_in_sentence(self, sentence: str, target: str) -> str:
        pattern = re.compile(re.escape(target), re.IGNORECASE)
        blanked = pattern.sub("____", sentence, count=1)
        if blanked == sentence:
            tokens = self._tokenize_sentence(sentence)
            if tokens:
                tokens[0] = "____"
                return " ".join(tokens)
        return blanked

    def _build_fill_blank_quiz(self, target: dict, difficulty: str) -> dict:
        sentence = target.get("example", "").strip()
        answer = target.get("es", "").strip()
        return {
            "type": "fill_blank",
            "prompt": "빈칸에 들어갈 단어를 입력하세요.",
            "question": self._blank_target_in_sentence(sentence, answer),
            "sentence": sentence,
            "answer": answer,
            "hint": target.get("ko", ""),
            "example_ko": target.get("example_ko", ""),
            "difficulty": difficulty,
        }

    def _build_word_order_quiz(self, target: dict, difficulty: str) -> dict:
        sentence = target.get("example", "").strip()
        tokens = self._tokenize_sentence(sentence)
        shuffled_tokens = tokens[:]
        random.shuffle(shuffled_tokens)
        if shuffled_tokens == tokens and len(tokens) > 1:
            shuffled_tokens.reverse()
        return {
            "type": "word_order",
            "prompt": "아래 단어를 눌러 올바른 문장을 완성하세요.",
            "question": target.get("example_ko", ""),
            "translation": target.get("example_ko", ""),
            "tokens": shuffled_tokens,
            "answer": sentence,
            "sentence": sentence,
            "example_ko": target.get("example_ko", ""),
            "difficulty": difficulty,
        }

    def get_all_words(self) -> List[dict]:
        return self._load_words()

    def get_quiz_question(self, completed_groups: Optional[List[int]] = None, difficulty: Optional[str] = None) -> dict:
        words = self._load_words()
        difficulty = self._normalize_difficulty(difficulty)
        
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
        
        quiz_type = random.choice(["multiple_choice", "true_false", "spelling", "fill_blank", "word_order"])
        
        if quiz_type == "multiple_choice":
            wrong_options = self._pick_wrong_options(target_pool, target, difficulty, 3)
            options = wrong_options + [target]
            random.shuffle(options)
            return {
                "type": "multiple_choice",
                "question": target['es'],
                "correct_answer": target['ko'],
                "options": [opt['ko'] for opt in options],
                "example": target['example'],
                "example_ko": target.get('example_ko', ''),
                "difficulty": difficulty
            }
        
        elif quiz_type == "true_false":
            is_correct = random.choice([True, False])
            display_ko = target['ko'] if is_correct else self._pick_wrong_options(target_pool, target, difficulty, 1)[0]['ko']
            return {
                "type": "true_false",
                "question": target['es'],
                "display_ko": display_ko,
                "correct_answer": "True" if is_correct else "False",
                "example": target['example'],
                "example_ko": target.get('example_ko', ''),
                "difficulty": difficulty
            }
            
        elif quiz_type == "spelling":
            return {
                "type": "spelling",
                "question": target['ko'],
                "correct_answer": target['es'],
                "example": target['example'],
                "example_ko": target.get('example_ko', ''),
                "difficulty": difficulty
            }

        elif quiz_type == "fill_blank":
            return self._build_fill_blank_quiz(target, difficulty)

        elif quiz_type == "word_order":
            return self._build_word_order_quiz(target, difficulty)

        return {"error": "Unsupported quiz type."}

vocab_service_instance = VocabService()
