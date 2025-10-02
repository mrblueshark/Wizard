import logging
import time
from analyzer.app.db import AnalyzerDB
from analyzer.app.decryptor import Decryptor
from analyzer.app.query_engine import QueryEngine
from analyzer.app.config import ANALYZER_CONFIG
from shared.models.packet import PacketModel 

# Setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def run_analysis_loop():
    """
    Simulates the main loop where analysts query the system.
    """
    logger.info("Analyzer service starting up...")

    # 1. Initialize dependencies
    db_client = AnalyzerDB(db_config=ANALYZER_CONFIG)
    decryptor = Decryptor(kms_config={"ADDRESS": ANALYZER_CONFIG["KMS_ADDRESS"]})
    query_engine = QueryEngine(config={})
    
    # Simple query definition
    test_query = "source_ip == '192.168.1.1' and protocol == 'TCP'"
    
    try:
        while True:
            logger.info(f"\n--- Running Analysis Loop ---")
            
            # 2. Retrieve Encrypted Data from DB
            # In a real app, this would be based on a time window or user input
            encrypted_packets: List[PacketModel] = db_client.fetch_packets_by_time_range(
                start_ms=int(time.time() * 1000) - 3600000 # Last hour of data
            )
            
            if not encrypted_packets:
                logger.info("No new encrypted packets found to analyze.")
                time.sleep(10)
                continue

            logger.info(f"Retrieved {len(encrypted_packets)} encrypted packets.")

            # 3. Decrypt the Data
            decrypted_packets: List[PacketModel] = []
            for ep in encrypted_packets:
                try:
                    # Decryptor handles KMS key retrieval and AES-GCM decryption
                    dp = decryptor.decrypt_packet(ep)
                    decrypted_packets.append(dp)
                except Exception as e:
                    logger.error(f"Failed to decrypt packet {ep.id}. Skipping. Error: {e}")
            
            logger.info(f"Successfully decrypted {len(decrypted_packets)} packets.")

            # 4. Run Query against Decrypted Data
            if decrypted_packets:
                results = query_engine.execute_query(decrypted_packets, test_query)
                
                logger.info(f"Query Results ({test_query}): Found {len(results)} matches.")
                if results:
                    # Print the first result for verification
                    logger.info("Example result:")
                    logger.info(results[0])
            
            # Pause for a new cycle
            time.sleep(20)

    except KeyboardInterrupt:
        logger.info("Analyzer shutdown initiated.")
    except Exception as e:
        logger.critical(f"FATAL ERROR in analysis loop: {e}", exc_info=True)
    finally:
        # 5. Cleanup
        db_client.close()
        decryptor.close()
        query_engine.close()
        logger.info("Analyzer service gracefully stopped.")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    run_analysis_loop()