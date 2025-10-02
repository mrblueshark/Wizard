import logging
import json
from datetime import datetime, timezone
import sys

# Define a custom formatter to output logs in a JSON structure
class JsonFormatter(logging.Formatter):
    """A custom logging formatter that outputs records as JSON objects."""
    
    def format(self, record):
        # Base log data
        log_record = {
            "timestamp": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "name": record.name,
            "module": record.module,
            "lineno": record.lineno,
            "message": record.getMessage(),
        }

        # Handle exception information if present
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        
        # Add extra fields (stored in record.__dict__)
        for key, value in record.__dict__.items():
            if key not in ['name', 'levelno', 'levelname', 'pathname', 'filename', 
                           'module', 'exc_info', 'exc_text', 'stack_info', 'lineno', 
                           'funcName', 'created', 'asctime', 'msecs', 'relativeCreated', 
                           'thread', 'threadName', 'process', 'message', 'msg', 'args']:
                log_record[key] = value

        return json.dumps(log_record)

def setup_logging(level: str = "INFO"):
    """
    Configures the root Python logger with a stream handler and JSON formatter.
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(level.upper())

    if root_logger.hasHandlers():
        return

    handler = logging.StreamHandler(sys.stdout)
    formatter = JsonFormatter()
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)
    
    # Suppress verbose logs from external libraries
    logging.getLogger('uvicorn').setLevel(logging.WARNING)
    logging.getLogger('fastapi').setLevel(logging.WARNING)
    logging.getLogger('asyncpg').setLevel(logging.WARNING)

    root_logger.info("Logging configured with JSON output.", extra={'config_level': level})

# --- Example Usage (Self-test) ---
if __name__ == "__main__":
    setup_logging(level="DEBUG")
    logger = logging.getLogger("wizard.main")
    
    logger.info("Application started.", extra={'api_port': 8000})
    
    try:
        1 / 0
    except ZeroDivisionError as e:
        logger.error("A critical error occurred.", exc_info=True, extra={'user_id': 'test-001'})
