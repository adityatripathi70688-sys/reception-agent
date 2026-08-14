import os
from src.database import init_db, save_call, fetch_all_calls
from src.transcriber import transcribe_audio
from src.extractor import extract_call_data

def process_single_audio(file_path: str):
    print(f'\n[1/3] Transcribing Audio: {file_path}')
    transcript = transcribe_audio(file_path)
    print(f'    Raw Text: "{transcript.strip()}"')

    print('[2/3] Extracting Structured Caller Information...')
    extracted_data = extract_call_data(transcript)
    
    print('[3/3] Saving Record to SQLite Database...')
    save_call(
        name=extracted_data.get("caller_name"),
        intent=extracted_data.get("caller_intent"),
        phone=extracted_data.get("callback_number"),
        urgency=extracted_data.get("urgency_level"),
        transcript=transcript
    )
    print('[+] Successfully processed and saved!')

def display_dashboard():
    records = fetch_all_calls()
    print('\n' + '='*80)
    print('RECEPTIONIST AGENT DASHBOARD - CALL LOGS')
    print('='*80)
    print(f'{"ID":<4} | {"Caller Name":<15} | {"Phone Number":<12} | {"Urgency":<8} | {"Intent"}')
    print('-' * 80)
    for row in records:
        call_id, name, phone, urgency, intent = row
        name_str = name if name else 'Unknown'
        phone_str = phone if phone else 'N/A'
        print(f'{call_id:<4} | {name_str:<15} | {phone_str:<12} | {urgency:<8} | {intent}')
    print('='*80 + '\n')

def main():
    init_db()
    samples_dir = os.path.join('data', 'audio_samples')
    if os.path.exists(samples_dir):
        audio_files = [f for f in os.listdir(samples_dir) if f.endswith(('.mp3', '.wav'))]
        print(f'Processing {len(audio_files)} audio call(s)...')
        for audio_file in audio_files:
            file_path = os.path.join(samples_dir, audio_file)
            process_single_audio(file_path)
    display_dashboard()

if __name__ == '__main__':
    main()
