# Wizard/python/analyzer/utils.py

import os
from dotenv import load_dotenv

# Optional: Load environment variables from a .env file if running locally
load_dotenv() 

def load_analyzer_config():
    """
    Loads necessary configuration settings for the Analyzer service from 
    environment variables.
    
    Returns:
        dict: A dictionary containing all required configuration values.
    """
    config = {}
    
    # Kafka Configuration
    config['KAFKA_BROKER'] = os.getenv("KAFKA_BROKER", "localhost:9092")
    config['KAFKA_TOPIC'] = os.getenv("KAFKA_TOPIC", "events")
    
    # MongoDB Configuration
    config['MONGODB_URI'] = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
    config['MONGODB_ANALYSIS_DB'] = os.getenv("MONGODB_ANALYSIS_DB", "wizard_analysis_dev")
    
    # Logging Level
    config['LOG_LEVEL'] = os.getenv("LOG_LEVEL", "INFO")
    
    # Validation check (add more robust checks if needed)
    if not config['KAFKA_BROKER'] or not config['MONGODB_URI']:
        print("FATAL: Required environment variables (KAFKA_BROKER or MONGODB_URI) are missing.")
        # In a real app, you would raise an exception here
        
    return config

def setup_logging(level_str="INFO"):
    """
    Sets up basic logging configuration based on the provided level string.
    """
    import logging
    levels = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARN": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL
    }
    log_level = levels.get(level_str.upper(), logging.INFO)
    
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
    )
    logging.getLogger(__name__).info(f"Logging initialized at {level_str.upper()} level.")
