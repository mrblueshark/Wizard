import pytest
from wizard.core.analysis_engine import analyze_event # Assuming wizard is in PYTHONPATH

# --- Fixtures and Setup (optional but good practice) ---
# None needed for these simple tests, but fixtures would go here.

# --- Test Cases ---

def test_login_event_low_risk():
    """Tests a standard LOGIN event resulting in a low risk score."""
    event = {
        "id": "abc-123",
        "type": "LOGIN",
        "user_id": "u-42",
        "data": {
            "country": "US",
            "device": "desktop"
        }
    }
    
    result = analyze_event(event)
    
    # Assertions
    assert result["event_id"] == "abc-123"
    assert result["score"] == pytest.approx(0.5, abs=1e-4) # Score tolerance
    assert "high_risk" not in result["labels"]

def test_high_value_purchase_high_risk():
    """Tests a PURCHASE event with a high value, triggering a high risk label."""
    event = {
        "id": "def-456",
        "type": "PURCHASE",
        "user_id": "u-43",
        "data": {
            "value": 1500.00,  # Value > 1000, should increase score by 0.2
            "item_count": 3
        }
    }
    
    result = analyze_event(event)
    
    # Base score (0.8) + High Value rule (0.2) = 1.0
    assert result["score"] == pytest.approx(1.0, abs=1e-4)
    assert "high_risk" in result["labels"]
    assert "high_value_transaction" in result["labels"]

def test_unknown_event_type():
    """Tests an event that doesn't match any known rules."""
    event = {
        "id": "ghi-789",
        "type": "UNKNOWN_PING",
        "user_id": "u-44",
        "data": {}
    }
    
    result = analyze_event(event)
    
    # Should default to a base score of 0.0
    assert result["score"] == pytest.approx(0.0, abs=1e-4)
    assert result["labels"] == []

