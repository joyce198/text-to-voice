from fastapi import FastAPI, Form, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import edge_tts
import os
import uuid

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def remove_file(path: str):
    if os.path.exists(path):
        os.remove(path)

@app.post("/convert")
async def convert_text_to_speech(
    background_tasks: BackgroundTasks,
    text: str = Form(...),
    voice: str = Form(...),
    rate: str = Form("+0%"),
    pitch: str = Form("+0Hz")
):

    filename = f"{uuid.uuid4()}.mp3"
    filepath = f"./{filename}"

    communicate = edge_tts.Communicate(
        text,
        voice,
        rate=rate,
        pitch=pitch
    )

    await communicate.save(filepath)

    background_tasks.add_task(remove_file, filepath)

    return FileResponse(
        filepath,
        media_type="audio/mpeg",
        filename="output.mp3"
    )