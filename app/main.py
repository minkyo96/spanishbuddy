
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api import grammar, curriculum, basics, vocab

app = FastAPI(title="Spanish Buddy")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(grammar.router)
app.include_router(curriculum.router)
app.include_router(basics.router)
app.include_router(vocab.router)

@app.get('/')
async def read_index():
    return FileResponse('static/index.html')
