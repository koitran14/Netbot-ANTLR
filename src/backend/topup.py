from datetime import datetime
import logging
from typing import Any, Dict, List, Optional

from .connection import MongoDBConnection

logger = logging.getLogger(__name__)


class Topup:
    """
    Class to handle top-up operations.
    """
    
    def __init__(self, connection: MongoDBConnection):
        self.collection = connection.get_collection("topups")
        self._create_indexes()
        
    def _create_indexes(self):
        """Create indexes for the topup collection."""
        
        try:
            self.collection.create_index([("created_at", -1)])
            logger.info("Indexes created successfully.")
        except Exception as e:
            logger.error(f"Failed to create indexes: {str(e)}")
            
    def save_topup(self, amount: str, currency: Optional[str], account: str, polite: Optional[str]) -> str:
        """Save a top-up request.

        Args:
            amount: The top-up amount (e.g., "100" or "100.50").
            currency: The currency (e.g., "usd") or None.
            account: The target account (e.g., "my account" or "JohnDoe").
            polite: Polite phrase (e.g., "please") or None.

        Returns:
            The inserted document's ID as a string.

        Raises:
            ValueError: If amount is invalid.
            RuntimeError: If database operation fails.
        """
        logger.info(f"Saving top-up: amount={amount}, currency={currency}, account={account}")
        try:
            amount_float = float(amount)
            if amount_float <= 0:
                raise ValueError("Amount must be positive")
        except ValueError:
            logger.error(f"Invalid amount format: {amount}")
            raise ValueError(f"Invalid amount format: {amount}")

        document = {
            "amount": amount_float,
            "currency": currency or "unknown",
            "account": account,
            "polite": polite,
            "created_at": datetime.utcnow(),
            "status": "pending"
        }
        
        try:
            result = self.collection.insert_one(document)
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Failed to save top-up: {str(e)}")
            raise RuntimeError(f"Failed to save top-up: {str(e)}")

    def get_topup_history(self, account: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieve top-up history.

        Args:
            account: The account to filter by or None.
            limit: Maximum number of records to return.

        Returns:
            A list of top-up documents sorted by creation time (newest first).

        Raises:
            RuntimeError: If database operation fails.
        """
        logger.info(f"Retrieving top-up history for account={account}")
        try:
            query = {"account": account} if account else {}
            cursor = self.collection.find(query).sort("created_at", -1).limit(limit)
            return list(cursor)
        except Exception as e:
            logger.error(f"Failed to retrieve top-up history: {str(e)}")
            raise RuntimeError(f"Failed to retrieve top-up history: {str(e)}")