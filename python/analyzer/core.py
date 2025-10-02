# Wizard/python/analyzer/core.py

import json
import os
import logging
from kafka import KafkaConsumer
from pymongo import MongoClient
from datetime import datetime

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AnalyzerCore:
    """
    Core class responsible for consuming Kafka events, running analysis, 
    and persisting results to MongoDB.
    """
    def __init__(self):
        # Configuration loaded from environment variables
        self.kafka_broker = os.getenv("KAFKA_BROKER", "localhost:9092")
        self.kafka_topic = os.getenv("KAFKA_TOPIC", "events")
        self.mongodb_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
        self.mongodb_db_analysis = os.getenv("MONGODB_ANALYSIS_DB", "wizard_analysis_dev")
        
        # Initialize Kafka Consumer
        try:
            self.consumer = KafkaConsumer(
                self.kafka_topic,
                bootstrap_servers=[self.kafka_broker],
                auto_offset_reset='latest', # Start consuming at the latest offset
                enable_auto_commit=True,
                group_id='analyzer-group',
                value_deserializer=lambda x: json.loads(x.decode('utf-8'))
            )
            logger.info(f"Kafka Consumer initialized for topic '{self.kafka_topic}' on broker: {self.kafka_broker}")
        except Exception as e:
            logger.error(f"Failed to initialize Kafka Consumer: {e}")
            raise

        # Initialize MongoDB Client and Collection
        try:
            self.mongo_client = MongoClient(self.mongodb_uri)
            self.db_analysis = self.mongo_client[self.mongodb_db_analysis]
            self.results_collection = self.db_analysis['results']
            logger.info(f"MongoDB connection established to database: {self.mongodb_db_analysis}")
        except Exception as e:
            logger.error(f"Failed to initialize MongoDB client: {e}")
            raise

    def run(self):
        """
        Main loop to continuously consume messages and process events.
        """
        logger.info("Analyzer core service starting main consumption loop...")
        for message in self.consumer:
            try:
                event_data = message.value
                
                # Process and analyze the event
                analysis_result = self._run_analysis(event_data)
                
                # Persist the result to MongoDB
                self._persist_result(analysis_result)

            except json.JSONDecodeError as e:
                logger.error(f"Failed to decode JSON message: {e}")
            except Exception as e:
                logger.error(f"An error occurred during event processing: {e}")

    def _run_analysis(self, event):
        """
        Performs basic analysis on the incoming event data.
        """
        # --- CRITICAL FIX: Ensure keys match the Go event model ---
        user_id = event.get('UserID', 'unknown_user')
        action = event.get('Action', 'unknown_action')
        timestamp = event.get('Timestamp', datetime.now().timestamp())
        
        # Example analysis: Determine event type and score
        event_type = "HighValue" if action in ["checkout", "add_to_cart"] else "LowValue"
        
        analysis = {
            "user_id": user_id,
            "original_action": action,
            "event_time": datetime.fromtimestamp(timestamp).isoformat(),
            "analysis_type": event_type,
            "processed_at": datetime.now().isoformat(),
            "event_details": event.get('Payload', {}), # Store payload details
        }
        
        return analysis

    def _persist_result(self, result):
        """
        Inserts the analysis result into the MongoDB collection.
        """
        try:
            self.results_collection.insert_one(result)
            logger.info(f"Persisted document for user {result['user_id']} ({result['original_action']}).")
        except Exception as e:
            logger.error(f"Failed to persist result to MongoDB: {e}")
            
# NOTE: This file is the core logic. The actual execution (main loop) 
# will be triggered by an entry point file (like main.py) that imports this class.
