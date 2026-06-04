from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api import grammar, curriculum, basics, vocab
import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

app = FastAPI(title="Spanish Buddy")

@app.post("/chat")
async def chat(data: dict):
    user_message = data.get("message", "")
    if not user_message:
        raise HTTPException(status_code=400, detail="Message is required")

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=user_message,
            config=types.GenerateContentConfig(
                system_instruction="You are a professional and friendly Spanish tutor. The user will send you a message in Spanish. Your task is to: 1. Respond to the user's message naturally in Spanish. 2. Analyze the user's input and provide coaching-style feedback in Korean. 3. Feedback should usually include: a short encouragement about what was good, and one or more helpful suggestions for more natural or correct Spanish. 4. If there are errors, mention them clearly using this exact format somewhere in the feedback: '[Original mistake] -> [Corrected version]: [Detailed explanation in Korean]'. 5. Do NOT use the phrase '오류 없음'. Even when the Spanish is very good, still give a short positive comment and, if useful, one more natural alternative or nuance tip. 6. Never write the feedback in Spanish or English, even partially, except for the original Spanish sentence and its corrected Spanish version inside the error format. 7. The JSON field \"response\" must contain only the Spanish reply, and the JSON field \"feedback\" must contain only Korean text. You MUST respond strictly in JSON format: {\"response\": \"Spanish response\", \"feedback\": \"Korean feedback\"}.", 
                response_mime_type="application/json"
            )
        )

        return json.loads(response.text or "{}")
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        raise HTTPException(status_code=500, detail=str(e))


app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(grammar.router)
app.include_router(curriculum.router)
app.include_router(basics.router)
app.include_router(vocab.router)

@app.get('/')
async def read_index():
    return FileResponse('static/index.html')
