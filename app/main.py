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
                system_instruction="You are a professional and friendly Spanish tutor. The user will send you a message in Spanish. Your task is to: 1. Respond to the user's message naturally in Spanish. 2. Analyze the user's input for grammatical errors, spelling mistakes, or unnatural phrasing. 3. Provide detailed feedback in Korean. If there are errors, please use the following format: '[Original mistake] -> [Corrected version]: [Detailed explanation of why it was wrong and how it works in Korean]'. This helps the user understand the nuance clearly. 4. If the user's Spanish is perfect, provide positive and encouraging feedback in Korean. You MUST respond strictly in JSON format: {\"response\": \"Spanish response\", \"feedback\": \"Korean feedback\"}.",
                response_mime_type="application/json"
            )
        )
        
        return json.loads(response.text)
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
