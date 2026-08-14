import os
import pytest
from src.database import init_db, insert_call_record, get_all_records # Adjust imports

# Use a temporary database for testing so you don't corrupt real data
TEST_DB_PATH = "data/db/test_reception.db"

@pytest.fixture(autouse=True)
def setup_and_teardown_db():
    # Setup: Initialize clean DB before test
    init_db(TEST_DB_PATH)
    yield
    # Teardown: Remove test DB after test completes
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)

def test_insert_and_retrieve_record():
    mock_payload = {
        "caller_name": "Alice Smith",
        "callback_number": "555-1234",
        "caller_intent": "Billing query",
        "urgency_level": "Low",
        "transcript": "Hello, I have a question about my invoice."
    }
    
    # Insert record
    insert_call_record(mock_payload, db_path=TEST_DB_PATH)
    
    # Fetch records
    records = get_all_records(db_path=TEST_DB_PATH)
    assert len(records) == 1
    assert records[0]["caller_name"] == "Alice Smith"
    assert records[0]["urgency_level"] == "Low"