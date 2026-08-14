import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def transcribe_audio(file_path: str) -> str:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is missing in your .env file!")
    client = Groq(api_key=api_key)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Audio file not found at: {file_path}")
    with open(file_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            file=(os.path.basename(file_path), audio_file.read()),
            model="whisper-large-v3-turbo",
            response_format="text"
        )
    return transcription
