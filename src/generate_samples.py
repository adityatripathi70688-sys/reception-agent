import os
from gtts import gTTS

# Ensure output directory exists
OUTPUT_DIR = os.path.join("data", "audio_samples")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Sample call recordings for testing
SAMPLES = [
    {
        "filename": "sample_1.mp3",
        "text": "This is Priya Nair. I need to reschedule my appointment "
            "from Thursday, it's a bit time sensitive since I'm "
            "traveling. My number is 555-330-9021, please call me "
            "back today if possible"
    },
    {
        "filename": "sample_2.mp3",
        "text": "Hi, this is Sarah Connor. I urgently need to speak with the billing department regarding an unexpected charge on my account. Reach me at 555-9876."
    },
    {
        "filename": "sample_3.mp3",
        "text": "Good afternoon, I am calling to ask about your business hours on weekends. No need to call me back, thanks!"
    }
]

def generate_audio():
    print("🎙️ Generating sample audio files...")
    for sample in SAMPLES:
        file_path = os.path.join(OUTPUT_DIR, sample["filename"])
        tts = gTTS(text=sample["text"], lang="en")
        tts.save(file_path)
        print(f"  [+] Saved: {file_path}")
    print("✅ All sample audio files generated successfully!")

if __name__ == "__main__":
    generate_audio()