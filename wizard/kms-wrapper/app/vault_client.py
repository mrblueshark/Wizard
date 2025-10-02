import logging
import os
from typing import Tuple, Optional, Dict, Any

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Global Mock Key Store:
# In a real scenario, this would be a secure, persistent, and encrypted store 
# (e.g., using a dedicated Vault API or secure database).
# Structure: {key_id: raw_encryption_key_bytes}
MOCK_KEY_STORE: Dict[str, bytes] = {}

class VaultClient:
    """
    Simulates a client that interacts with a Key Management System (KMS),
    such as HashiCorp Vault.
    
    Responsibilities:
    1. Generate a new Data Encryption Key (DEK).
    2. Securely store and retrieve DEKs.
    """
    
    def __init__(self, kms_config: Dict[str, Any]):
        self.kms_address = kms_config.get("KMS_ADDRESS", "vault.local")
        logger.info(f"VaultClient initialized, connected to mock KMS at {self.kms_address}")

    def generate_and_store_data_key(self) -> Tuple[str, bytes]:
        """
        Generates a new 256-bit symmetric encryption key and securely stores it.
        Returns the key ID (identifier) and the raw key material.
        """
        # 1. Generate unique ID and random key material (256-bit / 32 bytes)
        key_id = f"dek-{os.urandom(8).hex()}"
        encryption_key = os.urandom(32) 
        
        # 2. Store the key in the MOCK_KEY_STORE
        MOCK_KEY_STORE[key_id] = encryption_key
        
        logger.info(f"Generated and stored new DEK: {key_id}")
        return key_id, encryption_key

    def retrieve_data_key(self, key_id: str) -> Optional[bytes]:
        """
        Retrieves the raw data encryption key using its ID.
        """
        key = MOCK_KEY_STORE.get(key_id)
        if key:
            logger.debug(f"Retrieved DEK for ID: {key_id}")
        else:
            logger.warning(f"Failed to find DEK for ID: {key_id}")
            
        return key
