import os
import logging
from typing import Tuple, Dict, Any
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from shared.models.packet import PacketModel

# Mock logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# --- KMS Wrapper Mock ---

class KMSClient:
    """
    Mock client for the KMS-Wrapper service.
    In production, this would be a gRPC/HTTP client connecting to kms-wrapper.
    """
    def __init__(self, kms_config: Dict[str, Any]):
        self.kms_config = kms_config
        logger.info(f"Initialized KMS client for {kms_config.get('ADDRESS', 'mock')}")
        
    def generate_data_key(self) -> Tuple[str, bytes]:
        """
        Simulates requesting a new Data Encryption Key (DEK) from the KMS.
        The KMS would typically return a unique Key ID and the raw key material.
        """
        # In a real system, the KMS returns: 
        # 1. key_id (e.g., "kms-key-123")
        # 2. encryption_key (a secure random 256-bit key)
        key_id = f"dek-{os.urandom(4).hex()}"
        encryption_key = os.urandom(32) # 256-bit key
        
        logger.debug(f"KMS MOCK: Generated new data key with ID: {key_id}")
        return key_id, encryption_key

# --- Encryptor ---

class Encryptor:
    """
    Handles encryption of the raw packet payload using AES-256 GCM.
    It relies on the KMSClient to obtain the data encryption key (DEK).
    """
    
    def __init__(self, kms_config: Dict[str, Any]):
        self.kms_client = KMSClient(kms_config)

    def encrypt_payload(self, raw_payload: bytes) -> PacketModel:
        """
        Encrypts the raw payload and prepares the necessary storage metadata.
        
        Args:
            raw_payload: The raw bytes payload from the collector.
            
        Returns:
            A PacketModel containing the ciphertext and encryption metadata.
        """
        
        # 1. Key Generation (Delegated to KMS)
        # We assume the KMS also manages the master key and returns the DEK
        key_id, encryption_key = self.kms_client.generate_data_key()
        
        # 2. Nonce Generation
        # AES-GCM requires a unique, random 96-bit (12-byte) nonce/IV
        nonce = os.urandom(12)
        
        # 3. Encryption
        aesgcm = AESGCM(encryption_key)
        
        # ciphertext = Encrypt(key, nonce, plaintext, associated_data=None)
        # AESGCM.encrypt automatically appends the authentication tag (TAG)
        # to the ciphertext. We need to separate it for storage as nonce, tag, ciphertext.
        ciphertext_with_tag = aesgcm.encrypt(nonce, raw_payload, associated_data=None)

        # AES-GCM tags are 16 bytes long.
        tag = ciphertext_with_tag[-16:]
        ciphertext = ciphertext_with_tag[:-16]

        logger.debug(f"Payload encrypted. Key ID: {key_id}, Nonce size: {len(nonce)}, Tag size: {len(tag)}")
        
        # 4. Return storage-ready components
        # Note: We return the key_id, nonce, and tag separately from the ciphertext 
        # as this is often easier for database indexing and retrieval.
        return PacketModel(
            id="", # Will be set by the receiver
            timestamp_ms=0, # Will be set by the receiver
            source_ip="", # Will be set by the receiver
            destination_ip="", # Will be set by the receiver
            ciphertext=ciphertext,
            key_id=key_id,
            nonce=nonce,
            tag=tag
        )

    def close(self):
        """Clean up resources if needed."""
        logger.info("Encryptor closed.")
        pass