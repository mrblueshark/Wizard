import uvicorn
import logging
from fastapi import FastAPI
from shared.config import APP_CONFIG # NEW: Import shared config
from kms_wrapper.app.vault_client import VaultClient
from kms_wrapper.app import handlers as api_handlers

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Configuration placeholder (can be expanded later)
# REMOVED: KMS_CONFIG is no longer needed

def create_app():
    """Initializes and configures the FastAPI application."""
    app = FastAPI(
        title="KMS Wrapper Service",
        description="Handles Data Encryption Key (DEK) generation and retrieval.",
        version="1.0.0",
        docs_url="/docs"
    )

    # 1. Initialize the Vault/KMS Client using configured address
    vault_client = VaultClient(
        kms_config={
            "KMS_ADDRESS": f"http://{APP_CONFIG.KMS_WRAPPER_ADDRESS}:{APP_CONFIG.KMS_WRAPPER_PORT}"
        }
    )
    
    # 2. Inject the client instance into the handlers module
    api_handlers.set_vault_client(vault_client)
    
    # 3. Include the API router
    app.include_router(api_handlers.router)

    return app

# Main entrypoint
def start_server():
    """Starts the Uvicorn server."""
    app = create_app()
    
    host = "0.0.0.0" 
    # Use the configured port
    port = APP_CONFIG.KMS_WRAPPER_PORT
    
    logger.info(f"KMS Wrapper Starting on http://{host}:{port}")
    
    uvicorn.run(
        app, 
        host=host, 
        port=port,
        log_level="info"
    )

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    start_server()
