import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """
You are an expert AI Voice Assistant tasked with parsing phone call transcripts into structured JSON records.

### REQUIRED JSON OUTPUT SCHEMA
{
  "caller_name": string | null,
  "caller_intent": string,
  "callback_number": string | null,
  "urgency_level": "Low" | "Medium" | "High"
}

### RULES
1. If caller name is unstated, return null.
2. If phone number is unstated, return null.
3. Keep caller_intent brief (1 concise sentence).
4. Do not invent or fabricate information not in the transcript.
Output strictly valid JSON and nothing else.
"""

def extract_call_data(transcript: str) -> dict:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is missing in your .env file!")
    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Transcript:\n{transcript}"}
        ],
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)