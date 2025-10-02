# File: python/wizard/main.py

import os
import uvicorn
import logging
import asyncio
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from typing import Callable

# Import utilities and core logic
from wizard.utils.logging import setup_logging
# NOTE: We assume a database utility file for connection checks exists
# from wizard.utils.db_utils import check_db_connection 

# --- Application Initialization ---

# 1. Setup Structured Logging as the very first step
setup_logging(level=os.environ.get("WIZARD_LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

# Initialize the FastAPI app
app = FastAPI(
    title="Wizard Analyzer API Service",
    version="0.1.0",
    description="Analyzes events and serves results via REST API."
)

# --- Dependency Placeholder (from previous step) ---
def verify_api_key(api_key: str = None):
    # Simplified authentication check
    expected_key = os.environ.get("WIZARD_API_KEY", "default_secret")
    if api_key != expected_key:
        logger.warning("Attempted access with invalid API key.", extra={'status': 'unauthorized'})
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API Key")
    return True


# --- Startup and Shutdown Events ---

@app.on_event("startup")
async def startup_event():
    """Executed when the FastAPI application starts up."""
    logger.info("Starting up Wizard Analyzer API...", extra={'port': os.environ.get("ANALYZER_PORT", 8000)})
    
    # 1. Database Readiness Check (Crucial for production services)
    db_host = os.environ.get("DB_HOST", "db_local")
    db_port = int(os.environ.get("DB_PORT", 5432))
    
    # NOTE: This part requires the check_db_connection function to be defined elsewhere.
    # For now, we simulate the check.
    
    max_retries = 10
    for attempt in range(max_retries):
        try:
            # check_db_connection(host=db_host, port=db_port)
            # SIMULATION: Assume DB is ready on the third attempt
            if attempt < 2:
                raise ConnectionError("Database not ready yet.")
                
            logger.info("Database connection verified.", extra={'db_host': db_host})
            break # Exit the loop if connection succeeds
        except ConnectionError as e:
            if attempt == max_retries - 1:
                logger.critical("Failed to connect to database after max retries. Exiting.")
                # In a real app, you might raise an exception to halt startup
                raise Exception(f"Fatal: DB connection failed: {e}")
            logger.warning(f"Database not ready. Retrying in 2s... (Attempt {attempt + 1}/{max_retries})")
            await asyncio.sleep(2)


@app.on_event("shutdown")
def shutdown_event():
    """Executed when the FastAPI application is shutting down."""
    logger.info("Wizard Analyzer API shutting down gracefully.")
    # Here you would typically close database connection pools, 
    # Kafka consumers, or clean up temporary resources.


# --- API Endpoints (from previous step) ---

@app.get("/health", tags=["Monitoring"])
async def health_check():
    """Simple health check endpoint for monitoring systems."""
    # In a full app, this would also check DB status
    return JSONResponse(content={"status": "UP", "service": "Analyzer API"})

@app.get("/api/v1/analysis/{item_id}", tags=["Core API"])
async def get_analysis_result(item_id: int, authorized: bool = Depends(verify_api_key)):
    """Retrieves the analysis result for a given item ID."""
    # Logic imported from wizard.core.analysis_engine
    # Placeholder: return analyze_event(item_id)
    if item_id % 2 == 0:
        return {"item_id": item_id, "result": "Analyzed and OK"}
    else:
        raise HTTPException(status_code=404, detail=f"Analysis for Item ID {item_id} not found.")

# --- Main Run Block ---

if __name__ == "__main__":
    port = int(os.environ.get("ANALYZER_PORT", 8000))
    logger.info(f"Starting Uvicorn web server on port {port}")
    
    # Uvicorn runs the application, referencing the 'app' object in this file ('main')
    uvicorn.run("wizard.main:app", host="0.0.0.0", port=port, reload=True, log_config=None)