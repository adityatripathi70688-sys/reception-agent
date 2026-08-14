import pytest
from src.extractor import extract_call_metadata  # Adjust function name if different

def test_extract_call_metadata_returns_dict():
    sample_transcript = "Hi, my name is John Doe, call me back at 555-0199. My sink is overflowing!"
    
    # Run extractor
    result = extract_call_metadata(sample_transcript)
    
    # Assertions
    assert isinstance(result, dict)
    assert "caller_name" in result
    assert "urgency_level" in result
    assert result["urgency_level"] in ["Low", "Medium", "High"]

def test_high_urgency_escalation_flag():
    urgent_transcript = "Emergency! Gas leak detected at headquarters, call 911 immediately!"
    result = extract_call_metadata(urgent_transcript)
    
    # Verify the LLM assigns High urgency to an emergency call
    assert result.get("urgency_level") == "High"