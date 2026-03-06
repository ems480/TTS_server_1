import os
import uuid
import edge_tts
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from database import SessionLocal
from models import Audio
from utils import generate_hash
from google_drive_client import upload_file_to_drive

app = FastAPI()
VOICE_DEFAULT = "en-US-AvaNeural"
AUDIO_FOLDER = "/mnt/persistent/audio_cache"
os.makedirs(AUDIO_FOLDER, exist_ok=True)

# Allow Android apps
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "Edge TTS server with persistent storage running"}

@app.get("/tts")
async def tts(text: str, title: str = None, voice: str = VOICE_DEFAULT, rate: str = "-15%", pitch: str = "-5Hz"):
    db = SessionLocal()
    text_hash = generate_hash(text, voice, rate, pitch)

    # Check if audio already exists
    existing = db.query(Audio).filter(Audio.text_hash == text_hash).first()
    if existing:
        return JSONResponse({
            "status": "cached",
            "google_drive_url": existing.google_drive_url
        })

    # Generate new audio
    filename = f"{AUDIO_FOLDER}/{uuid.uuid4()}.mp3"
    communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    await communicate.save(filename)

    # Set title
    file_title = title if title else f"tts_{uuid.uuid4()}.mp3"

    # Upload to Google Drive
    drive_url = upload_file_to_drive(filename, file_title)

    # Save to DB
    audio = Audio(
        id=str(uuid.uuid4()),
        text_hash=text_hash,
        title=file_title,
        google_drive_url=drive_url
    )
    db.add(audio)
    db.commit()

    # Remove local file to save disk space
    os.remove(filename)

    return JSONResponse({
        "status": "generated",
        "google_drive_url": drive_url
    })
