import json
import logging
from typing import List, Dict, Any
import pandas as pd
from shared.models.packet import PacketModel

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class QueryEngine:
    """
    Handles data structuring and execution of DSL-like queries 
    against decrypted packet data using the pandas library.
    """
    
    def __init__(self, config: Dict[str, Any]):
        logger.info("Query Engine initialized.")
        # Config can hold query optimization settings, etc.

    def execute_query(self, decrypted_packets: List[PacketModel], dsl_query: str) -> List[Dict[str, Any]]:
        """
        Processes a list of decrypted packets and runs a query against them.
        
        Args:
            decrypted_packets: A list of PacketModel instances with the 
                               payload field containing the original, 
                               decrypted raw bytes (which we assume is JSON).
            dsl_query: A string representing the query (e.g., "source_ip == '10.0.0.1' and protocol == 'TCP'").
            
        Returns:
            A list of dictionaries representing the filtered, queried results.
        """
        
        if not decrypted_packets:
            logger.warning("Attempted to query an empty list of packets.")
            return []

        # 1. Structure Data for Analysis
        # We need to transform the list of PacketModels into a format pandas can use.
        # This includes parsing the 'payload' bytes, which is assumed to be a JSON string.
        
        records = []
        for packet in decrypted_packets:
            # Base metadata
            record = {
                "id": packet.id,
                "timestamp_ms": packet.timestamp_ms,
                "source_ip": packet.source_ip,
                "destination_ip": packet.destination_ip,
            }
            
            # Decrypted payload (assumed to be a JSON string containing network details)
            try:
                # The raw payload is the original data, which we assume is JSON
                payload_str = packet.payload.decode('utf-8')
                payload_data = json.loads(payload_str)
                # Merge payload data into the main record
                record.update(payload_data)
            except (UnicodeDecodeError, json.JSONDecodeError) as e:
                logger.error(f"Failed to parse decrypted payload for ID {packet.id}: {e}")
                # Skip or mark the record if payload parsing fails
                record["payload_error"] = str(e)

            records.append(record)

        # Create DataFrame
        df = pd.DataFrame(records)
        logger.info(f"DataFrame created with {len(df)} records. Columns: {list(df.columns)}")

        # 2. Execute the DSL Query
        try:
            # pandas.DataFrame.query() simulates running a DSL against the data
            filtered_df = df.query(dsl_query, engine='python') # Using 'python' engine for simplicity/compatibility
            
            logger.info(f"Query '{dsl_query}' executed. Found {len(filtered_df)} matches.")

            # 3. Return results as a list of dictionaries
            # Exclude metadata fields like key_id, nonce, tag from final output
            cols_to_keep = [col for col in filtered_df.columns if col not in ['ciphertext', 'key_id', 'nonce', 'tag', 'payload_error']]
            
            return filtered_df[cols_to_keep].to_dict('records')

        except Exception as e:
            logger.error(f"Error executing query '{dsl_query}': {e}")
            return []

    def close(self):
        """Clean up resources if needed."""
        logger.info("Query Engine closed.")
        pass