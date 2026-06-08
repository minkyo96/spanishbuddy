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
            "id": target.get("id"),
            "type": "fill_blank",
            "prompt": "빈칸에 들어갈 단어를 입력하세요.",
            "question": self._blank_target_in_sentence(sentence, answer),
            "sentence": sentence,
            "answer": answer,
            "hint": self._build_quiz_hint(target, "fill_blank", answer=answer),
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
            "id": target.get("id"),
            "type": "word_order",
            "prompt": "아래 단어를 눌러 올바른 문장을 완성하세요.",
            "question": target.get("example_ko", ""),
            "translation": target.get("example_ko", ""),
            "tokens": shuffled_tokens,
            "answer": sentence,
            "sentence": sentence,
            "example_ko": target.get("example_ko", ""),
            "hint": self._build_quiz_hint(target, "word_order", tokens=shuffled_tokens),
            "difficulty": difficulty,
        }

    def _build_quiz_hint(self, target: dict, quiz_type: str, answer: str = "", tokens: Optional[List[str]] = None) -> str:
        category = target.get("category", "")
        pos = target.get("pos", "")

        if quiz_type == "multiple_choice":
            parts = []
            if category:
                parts.append(f"분류: {category}")
            if pos:
                parts.append(f"품사: {pos}")
            return " · ".join(parts) or "뜻을 떠올려 보세요."

        if quiz_type == "true_false":
            parts = []
            if category:
                parts.append(f"분류: {category}")
            parts.append("예문을 함께 읽고 판단해 보세요.")
            return " · ".join(parts)

        if quiz_type == "spelling":
            parts = []
            if answer:
                parts.append(f"첫 글자: {answer[:1]}")
                parts.append(f"글자 수: {len(answer)}자")
            return " · ".join(parts) or "철자를 하나씩 떠올려 보세요."

        if quiz_type == "fill_blank":
            parts = []
            if answer:
                parts.append(f"첫 글자: {answer[:1]}")
                parts.append(f"글자 수: {len(answer)}자")
            return " · ".join(parts) or "빈칸 앞뒤 문장을 잘 살펴보세요."

        if quiz_type == "word_order":
            token_list = tokens or []
            parts = []
            if token_list:
                parts.append(f"총 {len(token_list)}단어")
                parts.append(f"첫 단어: {token_list[0]}")
            return " · ".join(parts) or "문장 순서를 천천히 맞춰 보세요."

        return ""

    def _build_quiz_key(self, target: dict, quiz_type: str) -> str:
        return f"{target.get('id')}:{quiz_type}"

    def get_all_words(self) -> List[dict]:
        return self._load_words()

    def get_quiz_question(
        self,
        completed_groups: Optional[List[int]] = None,
        difficulty: Optional[str] = None,
        excluded_ids: Optional[List[int]] = None,
        excluded_question_keys: Optional[List[str]] = None,
    ) -> dict:
        words = self._load_words()
        difficulty = self._normalize_difficulty(difficulty)
        excluded_id_set = set(excluded_ids or [])
        excluded_question_key_set = set(excluded_question_keys or [])
        
        # Filter words based on completed groups
        if completed_groups is not None and len(completed_groups) > 0:
            filtered_words = []
            for group_idx in completed_groups:
                start = group_idx * 20
                end = start + 20
                filtered_words.extend(words[start:end])
            
            if not filtered_words:
                return {"error": "No words learned yet."}
            target_pool = [word for word in filtered_words if word.get("id") not in excluded_id_set]
        else:
            # If no groups completed, we can't generate a quiz based on learned words.
            # But for the first time, maybe we allow all or return error.
            # User request: "only within the range of learned words"
            return {"error": "Please mark at least one vocab group as completed to start the quiz!"}

        quiz_types = ["multiple_choice", "true_false", "spelling", "fill_blank", "word_order"]
        available_combinations = [
            (word, quiz_type)
            for word in target_pool
            for quiz_type in quiz_types
            if self._build_quiz_key(word, quiz_type) not in excluded_question_key_set
        ]

        if not available_combinations:
            return {"error": "No more unique quiz questions available in the selected vocab groups."}

        target, quiz_type = random.choice(available_combinations)
        quiz_key = self._build_quiz_key(target, quiz_type)
        
        if quiz_type == "multiple_choice":
            wrong_options = self._pick_wrong_options(target_pool, target, difficulty, 3)
            options = wrong_options + [target]
            random.shuffle(options)
            return {
                "id": target['id'],
                "quiz_key": quiz_key,
                "type": "multiple_choice",
                "question": target['es'],
                "correct_answer": target['ko'],
                "hint": self._build_quiz_hint(target, quiz_type),
                "options": [opt['ko'] for opt in options],
                "example": target['example'],
                "example_ko": target.get('example_ko', ''),
                "category": target.get('category', ''),
                "pos": target.get('pos', ''),
                "difficulty": difficulty
            }
        
        elif quiz_type == "true_false":
            is_correct = random.choice([True, False])
            display_ko = target['ko'] if is_correct else self._pick_wrong_options(target_pool, target, difficulty, 1)[0]['ko']
            return {
                "id": target['id'],
                "quiz_key": quiz_key,
                "type": "true_false",
                "question": target['es'],
                "display_ko": display_ko,
                "correct_answer": "True" if is_correct else "False",
                "hint": self._build_quiz_hint(target, quiz_type),
                "example": target['example'],
                "example_ko": target.get('example_ko', ''),
                "category": target.get('category', ''),
                "pos": target.get('pos', ''),
                "difficulty": difficulty
            }
            
        elif quiz_type == "spelling":
            return {
                "id": target['id'],
                "quiz_key": quiz_key,
                "type": "spelling",
                "question": target['ko'],
                "correct_answer": target['es'],
                "hint": self._build_quiz_hint(target, quiz_type, answer=target['es']),
                "example": target['example'],
                "example_ko": target.get('example_ko', ''),
                "difficulty": difficulty
            }

        elif quiz_type == "fill_blank":
            quiz = self._build_fill_blank_quiz(target, difficulty)
            quiz["quiz_key"] = quiz_key
            return quiz

        elif quiz_type == "word_order":
            quiz = self._build_word_order_quiz(target, difficulty)
            quiz["quiz_key"] = quiz_key
            return quiz

        return {"error": "Unsupported quiz type."}

vocab_service_instance = VocabService()
