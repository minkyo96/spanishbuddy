# 🇪🇸 Spanish Buddy

**Spanish Buddy** is a modern, minimalist Spanish learning application designed to provide an intuitive and effective way to master the Spanish language. It combines a structured curriculum with a powerful AI-driven tutor to give users a personalized learning experience.

![License](https://img.shields.io/badge/license-MIT-blue)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688)
![TailwindCSS](https://img.shields.io/badge/Frontend-TailwindCSS-38B2AC)
![GeminiAI](https://img.shields.io/badge/AI-Gemini%202.0-4285F4)

---

## ✨ Key Features

### 🤖 AI Chat Tutor
Powered by Google Gemini, the AI tutor doesn't just chat—it teaches.
- **Natural Conversation**: Practice real-world Spanish in a friendly environment.
- **Detailed Feedback**: Get instant corrections in Korean using the format: `[Mistake] -> [Correction]: [Detailed Explanation]`.
- **Nuance Learning**: Understand the "why" behind the grammar, not just the "what".

### 📚 Structured Curriculum
- **One-Month Roadmap**: A guided path to take you from zero to conversational.
- **Vocab Groups**: Organized vocabulary sets (20 words per group) for manageable learning.
- **Smart Quizzes**: A filtered quiz mechanism that focuses on content you've already studied.

### 🎨 User-Centric Design
- **'Speak'-inspired UI**: Clean, high-contrast, and mobile-first design focusing on whitespace.
- **Flashcard Interaction**: Large focus, flip animations, and single-word progression for better retention.
- **Zero-Friction Start**: Progress is tracked via browser `LocalStorage`, allowing users to start learning without an account.

---

## 🛠️ Tech Stack

| Layer | Technology | Description |
| :--- | :--- | :--- |
| **Backend** | [FastAPI](https://fastapi.tiangolo.com/) | High-performance Python framework for the API. |
| **Frontend** | [Tailwind CSS](https://tailwindcss.com/) | Utility-first CSS for a modern, app-like UI. |
| **AI Engine** | [Google Gemini](https://ai.google.dev/) | Advanced LLM for tutoring and feedback. |
| **Deployment** | [Vercel](https://vercel.com/) | Seamless frontend hosting and deployment. |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- A Google AI Studio API Key ([Get it here](https://aistudio.google.com/))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/spanish-buddy.git
   cd spanish-buddy
   ```

2. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

5. **Open in browser**
   Visit `http://127.0.0.1:8000`

---

## 📁 Project Structure

```text
spanish-buddy/
├── app/
│   ├── main.py          # Entry point & AI Chat logic
│   ├── api/             # API Routers (grammar, curriculum, vocab, basics)
│   └── ...
├── static/              # Frontend assets (HTML, CSS, JS)
│   ├── index.html       # Main app page
│   └── ...
├── .env                 # Environment secrets (not tracked by git)
└── requirements.txt      # Project dependencies
```

---

## 🗺️ Roadmap
- [ ] **User Authentication**: Transition from LocalStorage to a secure DB.
- [ ] **Customizable TTS**: Adjustable speech speed and voice options.
- [ ] **Daily Goals**: Tracking system for daily learning streaks.
- [ ] **Expanded Curriculum**: More advanced levels and specialized vocabulary (Business, Travel).

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
