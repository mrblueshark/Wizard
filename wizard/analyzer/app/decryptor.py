import logging
import base64
import requests
from typing import Dict, Any, Optional
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidTag

from shared.models.packet import PacketModel

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# --- KMS HTTP Client ---

class KMSClient:
    """
    HTTP Client for the KMS-Wrapper service (FastAPI).
    Used to retrieve the Data Encryption Key (DEK).
    """
    def __init__(self, kms_config: Dict[str, Any]):
        # KMS_ADDRESS from config is used (e.g., kms-wrapper:8080)
        self.base_url = f"http://{kms_config.get('ADDRESS')}"
        logger.info(f"Initialized KMS HTTP client for {self.base_url}")
        
    def retrieve_data_key(self, key_id: str) -> Optional[bytes]:
        """
        Retrieves the raw data encryption key using the key ID.
        """
        url = f"{self.base_url}/retrieve-key"
        try:
            # We must pass key_id in the body as per the handler definition
            response = requests.post(url, json={"key_id": key_id}, timeout=5) 
            response.raise_for_status()
            
            data = response.json()
            # The key material is base64 encoded by the KMS wrapper
            raw_key = base64.b64decode(data['key_material'])
            
            logger.debug(f"KMS SUCCESS: Key retrieved for ID: {key_id}")
            return raw_key
            
        except requests.exceptions.RequestException as e:
            logger.error(f"KMS ERROR: Failed to retrieve key ID {key_id} from {url}: {e}")
            return None

# --- Decryptor ---

class Decryptor:
    """
    Handles decryption of the packet ciphertext using AES-256 GCM.
    Relies on the KMSClient to obtain the data encryption key (DEK).
    """
    
    def __init__(self, kms_config: Dict[str, Any]):
        self.kms_client = KMSClient(kms_config)

    def decrypt_packet(self, packet: PacketModel) -> Optional[bytes]:
        """
        Decrypts the ciphertext payload of a single PacketModel.
        
        Args:
            packet: PacketModel containing ciphertext and encryption metadata.
            
        Returns:
            The raw, decrypted bytes payload, or None on failure.
        """
        
        # 1. Key Retrieval (Delegated to KMS)
        decryption_key = self.kms_client.retrieve_data_key(packet.key_id)
        if not decryption_key:
            logger.error(f"DECRYPTION FAIL: Key not found for ID {packet.key_id}.")
            return None

        try:
            # 2. Prepare the AES-GCM object
            aesgcm = AESGCM(decryption_key)
            
            # 3. Combine ciphertext and tag (AESGCM.decrypt expects this)
            ciphertext_with_tag = packet.ciphertext + packet.tag
            
            # 4. Decryption
            # plaintext = Decrypt(key, nonce, ciphertext_with_tag, associated_data=None)
            plaintext = aesgcm.decrypt(packet.nonce, ciphertext_with_tag, associated_data=None)
            
            logger.info(f"DECRYPTION SUCCESS for Packet ID: {packet.id}")
            return plaintext
            
        except InvalidTag:
            # This indicates tampering or an incorrect key/nonce/tag combination
            logger.critical(f"DECRYPTION FAIL: Invalid Tag (potential tampering) for Packet ID: {packet.id}")
            return None
        except Exception as e:
            logger.error(f"DECRYPTION FAIL: An unexpected error occurred for Packet ID {packet.id}: {e}")
            return None

    def close(self):
        """Clean up resources if needed."""
        logger.info("Decryptor closed.")
        pass
