from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Render persistent disk path
DB_PATH = "/mnt/persistent/audio.db"
os.makedirs("/mnt/persistent", exist_ok=True)  # Ensure folder exists

DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
