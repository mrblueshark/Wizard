# Wizard/python/tests/test_core.py

import pytest
import os
from unittest.mock import patch, MagicMock
from datetime import datetime

# Assuming the AnalyzerCore class is in this module path
# NOTE: The actual path might be 'wizard.python.analyzer.core', 
# but for local testing, we assume direct import is possible.
from python.analyzer.core import AnalyzerCore 

# Mock environment variables before initializing the AnalyzerCore
@pytest.fixture(scope="module", autouse=True)
def mock_env():
    """Mocks required environment variables for the AnalyzerCore."""
    with patch.dict(os.environ, {
        "KAFKA_BROKER": "mock_broker:9092",
        "KAFKA_TOPIC": "mock_topic",
        "MONGODB_URI": "mongodb://mock_mongo:27017/",
        "MONGODB_ANALYSIS_DB": "mock_db",
    }):
        yield

# Fixture to mock the external dependencies (Kafka and Mongo)
@pytest.fixture
def mock_analyzer():
    """
    Creates an AnalyzerCore instance with mocked Kafka and MongoDB clients.
    """
    with patch('python.analyzer.core.KafkaConsumer') as MockKafka, \
         patch('python.analyzer.core.MongoClient') as MockMongo:
        
        # Configure the MongoDB mock collection to return a mock object
        mock_mongo_client = MockMongo.return_value
        mock_db = mock_mongo_client.__getitem__.return_value # Mock client['db']
        mock_collection = mock_db.__getitem__.return_value   # Mock db['collection']
        
        # Set up a mock for the KafkaConsumer instance
        MockKafka.return_value = MagicMock()
        
        analyzer = AnalyzerCore()
        
        # Attach the mock collection to the analyzer instance for testing persistence
        analyzer.results_collection = mock_collection
        
        yield analyzer
        
        MockKafka.stop.return_value = None # Clean up mock consumers

def test_analyzer_initialization(mock_analyzer):
    """Test if the AnalyzerCore initializes without raising exceptions."""
    assert mock_analyzer.kafka_broker == "mock_broker:9092"
    assert mock_analyzer.mongodb_db_analysis == "mock_db"
    # Check if the external clients were called during initialization
    assert AnalyzerCore.MongoClient.called
    assert AnalyzerCore.KafkaConsumer.called

def test_run_analysis_low_value_event(mock_analyzer):
    """Test analysis for a low-value action like login."""
    event = {
        "EventID": "uuid-1234",
        "UserID": "user-A",
        "Timestamp": datetime(2025, 1, 1).timestamp(),
        "Action": "login",
        "Payload": {"method": "email"},
    }
    
    result = mock_analyzer._run_analysis(event)
    
    assert result['user_id'] == "user-A"
    assert result['original_action'] == "login"
    assert result['analysis_type'] == "LowValue"
    assert "method" in result['event_details']

def test_run_analysis_high_value_event(mock_analyzer):
    """Test analysis for a high-value action like checkout."""
    event = {
        "EventID": "uuid-5678",
        "UserID": "user-B",
        "Timestamp": datetime(2025, 1, 2).timestamp(),
        "Action": "checkout",
        "Payload": {"total_amount": 450.0},
    }
    
    result = mock_analyzer._run_analysis(event)
    
    assert result['user_id'] == "user-B"
    assert result['original_action'] == "checkout"
    assert result['analysis_type'] == "HighValue"
    assert result['event_details']['total_amount'] == 450.0

def test_persist_result_calls_insert_one(mock_analyzer):
    """Test if the _persist_result method correctly calls MongoDB's insert_one."""
    mock_result = {
        "user_id": "test-user", 
        "original_action": "test", 
        "processed_at": datetime.now().isoformat()
    }
    
    mock_analyzer._persist_result(mock_result)
    
    # Assert that the insert_one method on the mock collection was called once
    mock_analyzer.results_collection.insert_one.assert_called_once()
    
    # Assert that the first argument passed to insert_one matches the result
    called_with = mock_analyzer.results_collection.insert_one.call_args[0][0]
    assert called_with['user_id'] == "test-user"
