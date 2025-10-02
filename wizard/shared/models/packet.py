from dataclasses import dataclass
from typing import Optional

@dataclass
class PacketModel:
    """
    A model representing a packet as it is stored in the database.
    Note: The payload here is the *encrypted* data (ciphertext).
    """
    id: str
    timestamp_ms: int
    source_ip: str
    destination_ip: str
    
    # Encrypted data payload
    ciphertext: bytes
    
    # Metadata for decryption
    key_id: str                   # Identifier for the key in the KMS
    nonce: bytes                  # Nonce used for AES-GCM
    tag: bytes                    # Authentication tag for AES-GCM