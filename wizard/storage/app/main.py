import logging
import time
from concurrent import futures

import grpc
from storage.app import transport_pb2_grpc as pb_grpc
from storage.app.receiver import DataReceiverServicer
from storage.app.db import StorageDB
from storage.app.encryptor import Encryptor
from storage.app.config import STORAGE_CONFIG

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def serve():
    """Starts the gRPC server for the storage service."""
    
    # 1. Initialize dependencies
    db_client = StorageDB(db_config=STORAGE_CONFIG)
    encryptor = Encryptor(kms_config={"ADDRESS": STORAGE_CONFIG["KMS_ADDRESS"]})
    
    # 2. Setup gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    # 3. Add the servicer implementation to the server
    pb_grpc.add_DataReceiverServicer_to_server(
        DataReceiverServicer(db_client=db_client, encryptor=encryptor),
        server
    )
    
    # 4. Bind and start the server
    port = STORAGE_CONFIG["GRPC_PORT"]
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    logger.info(f"Storage gRPC Server started, listening on port {port}")
    
    try:
        # Keep the main thread alive for the server to run
        while True:
            time.sleep(86400) # Sleep for a day
    except KeyboardInterrupt:
        logger.info("Shutting down server...")
        server.stop(0)
    finally:
        # 5. Clean up resources
        db_client.close()
        encryptor.close()
        logger.info("Storage service shutdown complete.")

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    serve()