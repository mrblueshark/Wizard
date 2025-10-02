import logging
from typing import Dict, Any
from shared.models.packet import PacketModel

# Mock logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class StorageDB:
    """
    Simulated Postgres Database Client for the Storage service.
    This class handles the persistence of the encrypted packet data.
    """
    
    # Simple in-memory dictionary to simulate the database table
    # Stores PacketModel instances after encryption
    _db_storage = {} 

    def __init__(self, db_config: Dict[str, Any]):
        self.db_config = db_config
        logger.info(f"Initialized storage DB client for {db_config.get('DB_HOST', 'localhost')}")

    def save_encrypted_packet(self, packet: PacketModel) -> str:
        """
        Saves the encrypted packet data to the simulated database.
        Returns the ID under which it was stored.
        """
        
        # In a real database, this would be an INSERT operation using psycopg2.
        # We store the PacketModel instance directly in our mock storage.
        self._db_storage[packet.id] = packet
        
        logger.info(f"DB WRITE: Saved encrypted data for ID: {packet.id}. Key ID used: {packet.key_id}")
        
        return packet.id

    def fetch_encrypted_packet(self, packet_id: str) -> PacketModel or None:
        """
        Retrieves an encrypted packet by ID. 
        """
        # Retrieves the full PacketModel instance from the mock store
        return self._db_storage.get(packet_id)

    def close(self):
        """Close database connection."""
        logger.info("Closed storage DB connection.")
        pass