import hashlib

def generate_hash(text: str, voice: str = "en-US-AvaNeural", rate: str = "-15%", pitch: str = "-5Hz"):
    text = text.strip().lower()
    combined = f"{text}_{voice}_{rate}_{pitch}"
    return hashlib.sha256(combined.encode()).hexdigest()
