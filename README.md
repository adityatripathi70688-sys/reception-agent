```markdown
# OpsPulse | AI Receptionist & Escalation Agent

An autonomous AI voice agent designed to process customer call audio, extract structured metadata (caller details, intent, urgency level), log records in a local database, and trigger priority escalation alerts via an interactive Streamlit operational dashboard.

---

## 📌 Features

- **Automated Speech Transcription**: Converts `.mp3` and `.wav` call recordings to text via OpenAI Whisper.
- **Structured Metadata Extraction**: Leverages Llama 3.3 to extract caller name, callback number, intent summary, and urgency rating in a single pass.
- **Real-Time Escalation Alerts**: Displays instant visual pop-ups for high-urgency callers.
- **Relational Persistence**: Automatically logs processed call transcripts and parsed JSON fields into SQLite.
- **Search & Analytics Dashboard**: Built with Streamlit for multi-attribute filtering, keyword searching, and data exports.

---

## 🛠️ Prerequisites

Before getting started, make sure you have the following installed:

- **Python 3.10+**
- **Git**
- A free **Groq API Key** (Get one at [console.groq.com](https://console.groq.com))

---

## 🚀 Quickstart Guide (Foolproof Setup)

Follow these step-by-step instructions to get the application running locally from scratch.

### 1. Clone the Repository
```bash
git clone https://github.com/adityatripathi70688-sys/reception-agent.git
cd reception-agent

```

### 2. Set Up a Virtual Environment

**On Windows:**

```cmd
python -m venv venv
venv\Scripts\activate

```

**On macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate

```

### 3. Install Dependencies

```bash
pip install -r requirements.txt

```

---

## 🔑 Environment Configuration

1. Create a `.env` file in the root directory of the project:
```bash
touch .env

```


2. Open `.env` in your text editor and add your Groq API key:
```env
GROQ_API_KEY=your_actual_groq_api_key_here

```



> ⚠️ **Note**: Do not commit your `.env` file to version control. Ensure `.env` is listed in your `.gitignore` file.

---

## 🏃 Running the Application End-to-End

Start the Streamlit dashboard by running:

```bash
streamlit run app.py

```

Once executed, Streamlit will open the web interface in your browser at:
`http://localhost:8501`

### How to test:

1. In the sidebar on the left, click **Browse files** under "Audio Processing Studio".
2. Select any sample `.wav` or `.mp3` audio file (sample files are provided in `data/sample_audio/` if available).
3. Click **Process Audio Recording**.
4. Watch the pipeline transcribe the audio, parse intent, log it to SQLite, and display the result in the active call queue table.

---

## 🏗️ Technical Architecture & Design Choices

The system follows an **Input → Think → Act → Output** cycle:

1. **Input**: Audio File (`.mp3` / `.wav`) uploaded through the Streamlit interface.
2. **Think (Pipeline Stage 1 - Speech Recognition)**: Audio is sent to `whisper-large-v3-turbo` hosted on Groq for ultra-fast, low-latency transcription.
3. **Think (Pipeline Stage 2 - Information Extraction)**: The raw text transcript is passed to `llama-3.3-70b-versatile` with system instructions to return strict JSON containing `caller_name`, `callback_number`, `caller_intent`, and `urgency_level` (`Low`, `Medium`, or `High`).
4. **Act**: The extracted payload is committed to an SQLite relational table (`data/db/reception.db`).
5. **Output**: The Streamlit interface updates metrics in real time. If `urgency_level == "High"`, a high-priority escalation toast and banner alert are rendered.

---

## ⚖️ Tradeoffs & Limitations

* **Groq API Dependency**: Relying on external cloud APIs keeps local hardware requirements low, but introduces network dependency. If offline processing is required, local execution via `whisper.cpp` or Ollama could be substituted.
* **Synchronous Audio Processing**: Audio file handling currently processes synchronously. For production enterprise volume, offloading processing to an asynchronous worker queue (such as Celery or Redis) would be preferred.
* **SQLite Database**: SQLite was chosen for zero-configuration local deployment. In a scaled deployment, upgrading to PostgreSQL would handle concurrent web requests better.

---

## 📂 Project Structure

```text
├── app.py                  # Main Streamlit dashboard UI & workflow entrypoint
├── src/
│   ├── database.py         # SQLite initialization, record insertion, and queries
│   ├── transcriber.py      # OpenAI Whisper API interface
│   └── extractor.py        # Llama 3 structured data extraction logic
├── data/
│   └── db/                 # Local SQLite database directory
├── requirements.txt        # Python package dependencies
├── .env.example            # Template for environment variables
└── README.md               # Project setup and architecture documentation

```
## 🔮 Future Roadmap & Enhancements

To transition OpsPulse into a fully production-ready enterprise solution, planned enhancements include:

- **Live Telephony & Webhook Integration**: Connect with Twilio or WebRTC to capture inbound phone calls live via WebSocket audio streams rather than file uploads.
- **Automated Outbound Escalations**: Integrate SMS/Email/Slack webhooks (e.g., Twilio API, Slack Webhooks, or PagerDuty) to dispatch instant alerts to human ops teams when high-urgency calls arrive.
- **Asynchronous Task Queue**: Transition from synchronous audio handling to background task processing using **Celery** or **Redis Queues (RQ)** for concurrent processing.
- **Database Migration**: Upgrade local SQLite persistence to **PostgreSQL / Supabase** to enable multi-node scaling and concurrent dashboard access.
- **Speaker Diarization**: Integrate **PyAnnote** or Whisper diarization models to distinguish between speaker turns (e.g., separating customer vs. automated prompt voices).
- **Sentiment & CSAT Metrics**: Expand LLM parsing to measure caller sentiment (Frustrated, Satisfied, Neutral) and predict customer satisfaction scores over time.

```
## OUTPUT

<img width="1891" height="904" alt="Screenshot 2026-08-14 232857" src="https://github.com/user-attachments/assets/721ef879-dacf-492e-98ba-fa8777b62ca4" />
<img width="1885" height="877" alt="Screenshot 2026-08-14 232836" src="https://github.com/user-attachments/assets/a0acc8f2-b047-437f-a9b6-1f88dd88b61a" />
<img width="1887" height="896" alt="Screenshot 2026-08-14 232817" src="https://github.com/user-attachments/assets/70909a67-5ec7-4703-a8eb-372c43d34cd5" />
<img width="1892" height="900" alt="Screenshot 2026-08-14 232803" src="https://github.com/user-attachments/assets/2e9a0673-478e-4e15-a804-918537774492" />
```

```
