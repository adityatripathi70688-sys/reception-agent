import os
import io
import pandas as pd
import streamlit as st

# Local module imports
from src.database import init_db, fetch_all_calls, save_call
from src.transcriber import transcribe_audio
from src.extractor import extract_call_data

# ------------------------------------------------------------------------------
# Configuration & Theme Setup
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="OpsPulse | AI Receptionist OS",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom UI Styling
st.markdown("""
    <style>
    .main { background-color: #0b0e14; }
    
    /* Card Container Styling */
    .metric-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 16px;
        text-align: center;
    }
    
    /* Header Styles */
    .app-header {
        font-size: 2rem;
        font-weight: 700;
        color: #f0f6fc;
        margin-bottom: 4px;
    }
    .app-subtext {
        color: #8b949e;
        font-size: 0.95rem;
        margin-bottom: 20px;
    }
    
    /* Urgency Badges */
    .badge {
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .badge-high { background-color: #4a1313; color: #ff6b6b; border: 1px solid #ff6b6b; }
    .badge-med  { background-color: #3d2c00; color: #ffd166; border: 1px solid #ffd166; }
    .badge-low  { background-color: #0d3b1e; color: #06d6a0; border: 1px solid #06d6a0; }
    </style>
""", unsafe_allow_html=True)


# ------------------------------------------------------------------------------
# Helper Functions
# ------------------------------------------------------------------------------
def generate_draft_email(caller_name: str, intent: str) -> str:
    """Generates a quick follow-up email template for customer support response."""
    name = caller_name if caller_name and caller_name != "Unknown" else "Valued Customer"
    return (
        f"Subject: Re: Your recent inquiry regarding {intent[:30]}...\n\n"
        f"Hi {name},\n\n"
        f"Thank you for contacting our support team. We received your request regarding: "
        f"\"{intent}\".\n\n"
        f"A support specialist is currently reviewing your request and will follow up with you shortly.\n\n"
        f"Best regards,\nOperations Support Team"
    )

def convert_df_to_csv(dataframe: pd.DataFrame) -> bytes:
    """Utility function to convert Pandas DataFrame to downloadable CSV bytes."""
    return dataframe.to_csv(index=False).encode('utf-8')


# ------------------------------------------------------------------------------
# App Initialization & Sidebar
# ------------------------------------------------------------------------------
init_db()

st.markdown('<div class="app-header">⚡ OpsPulse AI Receptionist</div>', unsafe_allow_html=True)
st.markdown('<div class="app-subtext">Automated voice processing, intent classification, and instant escalation system.</div>', unsafe_allow_html=True)

# Sidebar - Voice Ingestion
st.sidebar.title("🎙️ Audio Processing Studio")
st.sidebar.write("Upload customer call recordings to run through the AI pipeline.")

uploaded_audio = st.sidebar.file_uploader("Upload Audio (.mp3 / .wav)", type=["mp3", "wav"])

if uploaded_audio:
    if st.sidebar.button("Process Audio Recording", type="primary", use_container_width=True):
        try:
            # Temporary storage handling
            temp_directory = os.path.join("data", "temp")
            os.makedirs(temp_directory, exist_ok=True)
            saved_audio_path = os.path.join(temp_directory, uploaded_audio.name)
            
            with open(saved_audio_path, "wb") as buffer:
                buffer.write(uploaded_audio.getbuffer())
            
            # Step 1: Speech-to-Text
            with st.spinner("Transcribing audio transcript (Whisper)..."):
                transcript = transcribe_audio(saved_audio_path)
            
            # Step 2: Information Extraction
            with st.spinner("Analyzing intent & extracting metadata (Llama 3.3)..."):
                analysis_results = extract_call_data(transcript)
            
            urgency_rating = analysis_results.get("urgency_level", "Low")
            
            # Step 3: Database Persistence
            save_call(
                name=analysis_results.get("caller_name"),
                intent=analysis_results.get("caller_intent"),
                phone=analysis_results.get("callback_number"),
                urgency=urgency_rating,
                transcript=transcript
            )
            
            st.sidebar.success("Call record successfully indexed!")
            
            # Immediate Escalation Alert
            if urgency_rating == "High":
                st.error(f"🚨 **HIGH URGENCY ALERT**: Immediate action required for caller **{analysis_results.get('caller_name', 'Unknown')}**!")
                st.toast("Urgent call registered in queue!", icon="🚨")
            
            st.rerun()

        except Exception as err:
            st.sidebar.error(f"Failed to process call: {str(err)}")


# ------------------------------------------------------------------------------
# Dashboard Content & Analytics
# ------------------------------------------------------------------------------
records = fetch_all_calls()

if records:
    # Build DataFrame safely
    if len(records[0]) >= 6:
        call_logs_df = pd.DataFrame(records, columns=["ID", "Caller Name", "Phone Number", "Urgency", "Intent", "Raw Transcript"])
    else:
        call_logs_df = pd.DataFrame(records, columns=["ID", "Caller Name", "Phone Number", "Urgency", "Intent"])
        call_logs_df["Raw Transcript"] = "Transcript unavailable."

    # Top Metric Bar
    total_calls_count = len(call_logs_df)
    high_urgency_count = len(call_logs_df[call_logs_df["Urgency"] == "High"])
    med_urgency_count = len(call_logs_df[call_logs_df["Urgency"] == "Medium"])
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Inbound Calls", total_calls_count)
    col2.metric("High Priority Calls", high_urgency_count, delta=f"{high_urgency_count} Urgent", delta_color="inverse")
    col3.metric("Medium Priority Calls", med_urgency_count)
    col4.metric("Engine Status", "Active", "0 Latency")

    st.divider()

    # Main Tabbed Interface
    table_tab, analytics_tab = st.tabs(["📋 Active Call Queue", "📊 Analytics & Export"])

    with table_tab:
        # Search & Filter Header
        f_col1, f_col2, f_col3 = st.columns([1, 2, 1])
        with f_col1:
            selected_urgencies = st.multiselect(
                "Filter Urgency",
                options=["Low", "Medium", "High"],
                default=["Low", "Medium", "High"]
            )
        with f_col2:
            search_term = st.text_input("🔍 Search Callers or Keywords", placeholder="Type caller name or intent...")
        with f_col3:
            st.write("") # Alignment padding
            st.write("")
            csv_bytes = convert_df_to_csv(call_logs_df)
            st.download_button(
                label="📥 Export CSV Report",
                data=csv_bytes,
                file_name="call_logs_report.csv",
                mime="text/csv",
                use_container_width=True
            )

        # Apply Table Filtering
        filtered_logs = call_logs_df[call_logs_df["Urgency"].isin(selected_urgencies)]
        if search_term:
            filtered_logs = filtered_logs[
                filtered_logs["Caller Name"].str.contains(search_term, case=False, na=False) |
                filtered_logs["Intent"].str.contains(search_term, case=False, na=False)
            ]

        st.dataframe(filtered_logs[["ID", "Caller Name", "Phone Number", "Urgency", "Intent"]], use_container_width=True)

        st.divider()

        # Detailed Call Inspector
        st.subheader("🔍 Deep Record Inspector")
        available_ids = call_logs_df["ID"].tolist()
        selected_record_id = st.selectbox("Select Record ID to Inspect:", available_ids)

        if selected_record_id:
            record = call_logs_df[call_logs_df["ID"] == selected_record_id].iloc[0]
            
            c1, c2, c3 = st.columns(3)
            c1.markdown(f"**Caller Name:** `{record['Caller Name']}`")
            c2.markdown(f"**Callback Number:** `{record['Phone Number']}`")
            
            badge_class = "badge-high" if record['Urgency'] == 'High' else ("badge-med" if record['Urgency'] == 'Medium' else "badge-low")
            c3.markdown(f"**Urgency Level:** <span class='badge {badge_class}'>{record['Urgency']}</span>", unsafe_allow_html=True)

            st.write(f"**Extracted Intent:** {record['Intent']}")
            
            with st.expander("🎙️ View Audio Transcript", expanded=True):
                st.info(f"\"{record['Raw Transcript']}\"")

            # NEW FEATURE: Automated Email Response Drafter
            with st.expander("✉️ Auto-Generated Response Draft"):
                email_draft = generate_draft_email(record['Caller Name'], record['Intent'])
                st.code(email_draft, language="markdown")

    with analytics_tab:
        st.subheader("📈 Urgency Volume Breakdown")
        urgency_counts = call_logs_df["Urgency"].value_counts()
        st.bar_chart(urgency_counts)
        
        st.subheader("System Metadata")
        st.json({
            "database_records": total_calls_count,
            "models_deployed": {
                "transcription": "whisper-large-v3-turbo",
                "extraction_llm": "llama-3.3-70b-versatile"
            },
            "environment": "Development / Local"
        })

else:
    st.info("👋 No calls recorded yet. Upload an audio recording in the sidebar to get started.")