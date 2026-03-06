from sqlalchemy import Column, String
from database import Base

class Audio(Base):
    __tablename__ = "audio"
    id = Column(String, primary_key=True)
    text_hash = Column(String, unique=True)
    title = Column(String)
    google_drive_url = Column(String)
