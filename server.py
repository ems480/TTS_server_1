import uuid
import edge_tts
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# allow Android apps
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

VOICE_DEFAULT = "en-US-AvaNeural"

@app.get("/")
def home():
    return {"status": "TTS server running"}

@app.get("/tts")
async def tts(text: str, voice: str = VOICE_DEFAULT, rate: str = "-15%", pitch: str = "-5Hz"):

    filename = f"{uuid.uuid4()}.mp3"

    communicate = edge_tts.Communicate(
        text,
        voice,
        rate=rate,
        pitch=pitch
    )

    await communicate.save(filename)

    return FileResponse(filename, media_type="audio/mpeg", filename="speech.mp3")