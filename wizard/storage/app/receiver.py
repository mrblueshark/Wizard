import logging
from typing import Dict, Any

# gRPC dependencies
import grpc
# Generated stubs (will be present after step 7)
from storage.app import transport_pb2 as pb
from storage.app import transport_pb2_grpc as pb_grpc

# Local dependencies
from storage.app.encryptor import Encryptor
from storage.app.db import StorageDB
from shared.models.packet import PacketModel

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class DataReceiverServicer(pb_grpc.DataReceiverServicer):
    """
    gRPC Server implementation for the DataReceiver service.
    Handles incoming packets from the Collector, encrypts them, and stores them.
    """
    
    def __init__(self, db_client: StorageDB, encryptor: Encryptor):
        self.db_client = db_client
        self.encryptor = encryptor
        logger.info("DataReceiverServicer initialized.")

    def StorePacket(self, request: pb.Packet, context: grpc.ServicerContext) -> pb.StoreResponse:
        """
        Implements the rpc StorePacket(Packet) returns (StoreResponse) method.
        """
        
        packet_id = request.id
        
        logger.info(f"RECEIVING: Packet ID {packet_id} received from collector.")
        
        try:
            # 1. Encrypt the raw payload
            # The encryptor returns a PacketModel with ciphertext/metadata, 
            # but missing non-encryption-related fields (id, IPs, timestamp).
            encrypted_data_model: PacketModel = self.encryptor.encrypt_payload(request.payload)
            
            # 2. Complete the storage model with fields from the gRPC request
            storage_model = PacketModel(
                id=packet_id,
                timestamp_ms=request.timestamp_ms,
                source_ip=request.source_ip,
                destination_ip=request.destination_ip,
                ciphertext=encrypted_data_model.ciphertext,
                key_id=encrypted_data_model.key_id,
                nonce=encrypted_data_model.nonce,
                tag=encrypted_data_model.tag
            )
            
            # 3. Store the fully-populated encrypted model in the database
            stored_id = self.db_client.save_encrypted_packet(storage_model)
            
            # 4. Return success response
            return pb.StoreResponse(
                success=True,
                message=f"Packet stored successfully and encrypted with key {storage_model.key_id}.",
                stored_id=stored_id
            )
            
        except Exception as e:
            logger.error(f"FATAL ERROR: Failed to process packet ID {packet_id}: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal processing error: {e}")
            
            # 5. Return failure response
            return pb.StoreResponse(
                success=False,
                message=f"Failed to store packet: {e}",
                stored_id=packet_id # Return the original ID for debugging
            )