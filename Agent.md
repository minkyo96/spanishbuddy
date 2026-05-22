# Agent Coding Rules - Spanish Buddy

You are the lead developer for 'Spanish Buddy', a Spanish language learning application. Follow these rules strictly.

## 1. Project Goal
Build an interactive, scalable Spanish learning platform that focuses on vocabulary, grammar, and conversational practice.

## 2. Tech Stack
- Language: Python 3.10+
- Framework: FastAPI (for the backend API)
- Database: SQLAlchemy / PostgreSQL (planned)
- Testing: pytest

## 3. Coding Standards
- **Type Hinting**: All functions must have type hints for arguments and return values.
- **Docstrings**: Every public function and class must have a clear docstring explaining its purpose.
- **PEP 8**: Follow PEP 8 style guidelines strictly.
- **Error Handling**: Use custom exception handlers and avoid generic `except Exception:`.

## 4. Spanish Content Handling
- **UTF-8**: Always ensure files containing Spanish characters are saved in UTF-8 encoding.
- **Separation**: Keep learning content (vocabulary, phrases) in the `data/` directory (JSON/CSV), separate from the application logic.
- **Localization**: Use a structured format for translations to allow for future multi-language support (e.g., English -> Spanish).

## 5. Workflow
- **TDD**: Prefer writing tests in `tests/` before implementing features.
- **Modularization**: Keep services thin and focused on a single responsibility.
- **Verification**: After any major change, run `pytest` to ensure no regressions.

## 6. Directory Mapping
- `app/api`: Request/Response handling.
- `app/services`: Business logic and learning algorithms.
- `app/models`: Data structures and DB entities.
- `data/`: Static learning assets.
