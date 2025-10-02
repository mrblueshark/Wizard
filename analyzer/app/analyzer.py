import os
import json
import logging
import time
from datetime import datetime, timezone

from kafka import KafkaConsumer
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure

# --- Configuration ---
KAFKA_BROKERS = os.getenv('KAFKA_BROKERS', 'kafka:9092').split(',')
KAFKA_INPUT_TOPIC = os.getenv('KAFKA_INPUT_TOPIC', 'events').strip()
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://mongo:27017/').strip()
MONGO_DB_NAME = os.getenv('MONGO_DB_NAME', 'wizard_analysis').strip()
MONGO_COLLECTION_NAME = 'results'

# --- Setup Logging ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('AnalyzerService')

class Analyzer:
    """
    Consumes events from Kafka, runs a simulated analysis, and persists results to MongoDB.
    """
    def __init__(self):
        # 1. MongoDB Setup
        self.mongo_client = None
        self.mongo_collection = None
        # Give infrastructure services time to start before connecting
        time.sleep(5) 
        self._setup_mongodb()

        # 2. Kafka Consumer Setup
        self.consumer = self._setup_kafka_consumer()

    def _setup_mongodb(self):
        """Initializes MongoDB connection and collection handle."""
        try:
            # Set serverSelectionTimeoutMS low since we rely on docker-compose depends_on for basic startup
            self.mongo_client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000) 
            # The ismaster command is a lightweight way to check connection
            self.mongo_client.admin.command('ismaster') 
            db = self.mongo_client[MONGO_DB_NAME]
            self.mongo_collection = db[MONGO_COLLECTION_NAME]
            logger.info(f"Successfully connected to MongoDB database: {MONGO_DB_NAME}")
        except ConnectionFailure as e:
            logger.error(f"Failed to connect to MongoDB at {MONGO_URI}: {e}")
            raise

    def _setup_kafka_consumer(self):
        """Initializes the Kafka Consumer."""
        try:
            consumer = KafkaConsumer(
                KAFKA_INPUT_TOPIC,
                bootstrap_servers=KAFKA_BROKERS,
                group_id='analyzer-group',
                auto_offset_reset='earliest',
                value_deserializer=lambda x: json.loads(x.decode('utf-8'))
            )
            logger.info(f"Kafka consumer set up for topic: {KAFKA_INPUT_TOPIC}")
            return consumer
        except Exception as e:
            logger.error(f"Failed to set up Kafka consumer: {e}")
            raise

    def _run_analysis(self, event: dict) -> dict:
        """
        Simulated business logic: runs analysis on the event.
        """
        user_id = event.get('user_id')
        event_type = event.get('type')
        event_id = event.get('id')
        
        score = 0.0
        labels = ["normal"]
        detail_message = f"Basic processing for {event_type} event."

        if event_type == "PURCHASE":
            score = 0.9
            labels = ["transaction", "high_value"]
        elif event_type == "TELEMETRY":
            latency = event.get('data', {}).get('latency_ms', 0)
            if latency > 100:
                score = 0.5
                labels = ["telemetry", "high_latency"]
        
        # Define the analysis result structure (matches the Go model)
        result = {
            "event_id": event_id,
            "user_id": user_id, 
            "score": score,
            "labels": labels,
            "detail_message": detail_message,
            "processed_at": datetime.now(timezone.utc).isoformat()
        }
        return result

    def _persist_result(self, result: dict):
        """Saves the analysis result to MongoDB."""
        try:
            # Ensure we only try to persist if the collection handle is ready
            if self.mongo_collection:
                insert_result = self.mongo_collection.insert_one(result)
                logger.info(f"Analysis result persisted: ID={insert_result.inserted_id}, EventID={result['event_id']}")
            else:
                logger.error("MongoDB collection handle is not initialized. Cannot persist data.")
        except OperationFailure as e:
            logger.error(f"MongoDB persistence failed for event {result['event_id']}: {e}")
            
    def run(self):
        """Main loop to consume and process messages."""
        logger.info("Analyzer Service started. Waiting for messages...")
        
        for message in self.consumer:
            event = message.value
            logger.info(f"Received event {event.get('id')} of type {event.get('type')} from partition {message.partition}")
            
            try:
                analysis_result = self._run_analysis(event)
                self._persist_result(analysis_result)
                
            except Exception as e:
                logger.error(f"An unexpected error occurred during processing: {e}", exc_info=True)


if __name__ == '__main__':
    # Give services a brief moment to start up (if depends_on failed us)
    time.sleep(10) 
    
    while True:
        try:
            analyzer = Analyzer()
            analyzer.run()
        except Exception as e:
            logger.error(f"Main Analyzer loop encountered a fatal error: {e}. Retrying in 5 seconds...")
            time.sleep(5)
