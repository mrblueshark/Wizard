from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import logging
import base64

from kms_wrapper.app.vault_client import VaultClient # Note: Relative import adjusted for context

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# API Router setup
router = APIRouter()

# The VaultClient instance will be set in main.py
vault_client: Optional[VaultClient] = None

def set_vault_client(client: VaultClient):
    """Utility function to inject the initialized VaultClient instance."""
    global vault_client
    vault_client = client

# --- Request/Response Models (Simplified) ---

# Request for decryption key
class DecryptKeyRequest(Dict[str, str]):
    key_id: str

# Response containing the raw key (base64 encoded)
class KeyResponse(Dict[str, str]):
    key_id: str
    key_material: str # Base64 encoded key
    message: str


# --- API Routes ---

@router.post("/generate-key", response_model=KeyResponse)
def generate_key_endpoint():
    """
    Endpoint used by the 'storage' service (encryptor) to generate a new key 
    before encrypting a packet.
    """
    if not vault_client:
        raise HTTPException(status_code=500, detail="Vault client not initialized.")
        
    key_id, raw_key = vault_client.generate_and_store_data_key()
    
    # Return the key material base64 encoded for safe HTTP transmission
    b64_key = base64.b64encode(raw_key).decode('utf-8')
    
    return KeyResponse(
        key_id=key_id,
        key_material=b64_key,
        message="New DEK generated and securely stored."
    )


@router.post("/retrieve-key", response_model=KeyResponse)
def retrieve_key_endpoint(request: DecryptKeyRequest):
    """
    Endpoint used by the 'analyzer' service (decryptor) to retrieve a key 
    using its ID for decryption.
    """
    if not vault_client:
        raise HTTPException(status_code=500, detail="Vault client not initialized.")
        
    key_id = request.get('key_id')
    raw_key = vault_client.retrieve_data_key(key_id)
    
    if not raw_key:
        logger.error(f"Retrieval failure for key ID: {key_id}")
        raise HTTPException(status_code=404, detail=f"Key ID '{key_id}' not found.")

    b64_key = base64.b64encode(raw_key).decode('utf-8')
    
    return KeyResponse(
        key_id=key_id,
        key_material=b64_key,
        message="DEK retrieved successfully."
    )
