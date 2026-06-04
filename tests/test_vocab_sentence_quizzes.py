import random

from app.services.vocab_service import VocabService


TEST_WORDS = [
    {
        "id": 1,
        "es": "hablo",
        "ko": "말하다",
        "category": "동사",
        "example": "Yo hablo español todos los días.",
        "example_ko": "나는 매일 스페인어를 말해요.",
    },
    {
        "id": 2,
        "es": "es",
        "ko": "~이다",
        "category": "동사",
        "example": "Mi nombre es Ana.",
        "example_ko": "내 이름은 아나예요.",
    },
    {
        "id": 3,
        "es": "estoy",
        "ko": "~에 있다 / ~한 상태다",
        "category": "동사",
        "example": "Estoy muy contento hoy.",
        "example_ko": "오늘 나는 매우 기뻐요.",
    },
]


def make_service(tmp_path):
    data_path = tmp_path / "words.json"
    data_path.write_text(__import__("json").dumps(TEST_WORDS, ensure_ascii=False), encoding="utf-8")
    return VocabService(str(data_path))


def test_get_quiz_question_supports_fill_blank(tmp_path, monkeypatch):
    service = make_service(tmp_path)

    chosen = iter([TEST_WORDS[0], "fill_blank"])
    monkeypatch.setattr(random, "choice", lambda seq: next(chosen))
    monkeypatch.setattr(random, "sample", lambda seq, k: seq[:k])

    quiz = service.get_quiz_question(completed_groups=[0], difficulty="medium")

    assert quiz["type"] == "fill_blank"
    assert quiz["answer"] == "hablo"
    assert quiz["sentence"] == "Yo hablo español todos los días."
    assert "____" in quiz["question"]
    assert quiz["example_ko"] == "나는 매일 스페인어를 말해요."


def test_get_quiz_question_supports_word_order(tmp_path, monkeypatch):
    service = make_service(tmp_path)

    chosen = iter([TEST_WORDS[1], "word_order"])
    monkeypatch.setattr(random, "choice", lambda seq: next(chosen))

    def reverse_shuffle(items):
        items.reverse()

    monkeypatch.setattr(random, "shuffle", reverse_shuffle)
    monkeypatch.setattr(random, "sample", lambda seq, k: seq[:k])

    quiz = service.get_quiz_question(completed_groups=[0], difficulty="medium")

    assert quiz["type"] == "word_order"
    assert quiz["answer"] == "Mi nombre es Ana."
    assert quiz["sentence"] == "Mi nombre es Ana."
    assert quiz["tokens"]
    assert quiz["tokens"] != ["Mi", "nombre", "es", "Ana."]
    assert quiz["example_ko"] == "내 이름은 아나예요."
