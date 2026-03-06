from database import engine
from models import Base
import os

# Ensure persistent audio folder exists
AUDIO_FOLDER = "/mnt/persistent/audio_cache"
os.makedirs(AUDIO_FOLDER, exist_ok=True)

# Create database tables
Base.metadata.create_all(bind=engine)

print("Database and folders initialized!")
