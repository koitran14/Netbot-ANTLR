from typing import Dict, List, Optional
from src.database.utils.helpers import sanitize_input
from src.database.client import pg_client
from datetime import datetime
from uuid import UUID

class TopupModel:
    def __init__(self):
        self.table = "topups"

    def add_topup(self, user_id: int, amount: float, currency: str = "usd") -> Optional[Dict]:
        data = sanitize_input({"user_id": user_id, "amount": amount, "currency": currency})
        if data["amount"] <= 0:
            raise ValueError("Top-up amount must be positive")
        if data["currency"] not in ["usd", "dollars"]:
            raise ValueError("Invalid currency")
        
        conn = pg_client.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    f"""
                    INSERT INTO {self.table} (user_id, amount, currency)
                    VALUES (%s, %s, %s)
                    RETURNING id, user_id, amount, currency, created_at
                    """,
                    (data["user_id"], data["amount"], data["currency"])
                )
                conn.commit()
                result = cur.fetchone()
                if result:
                    return {
                        "id": result[0],
                        "user_id": result[1],
                        "amount": result[2],
                        "currency": result[3],
                        "created_at": result[4]
                    }
                return None
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            pg_client.release_connection(conn)

    def get_by_user(self, user_id: int, query_type: str = "all") -> List[Dict]:
        """Retrieve top-up history for a user (latest, oldest, or all)."""
        valid_query_types = ["latest", "oldest", "all"]
        if query_type not in valid_query_types:
            raise ValueError(f"Invalid query_type. Must be one of {valid_query_types}")

        conn = pg_client.get_connection()
        try:
            with conn.cursor() as cur:
                order_clause = "ORDER BY created_at DESC" if query_type != "oldest" else "ORDER BY created_at ASC"
                limit_clause = "LIMIT 1" if query_type in ["latest", "oldest"] else ""
                
                cur.execute(
                    f"""
                    SELECT id, user_id, amount, currency, created_at
                    FROM {self.table}
                    WHERE user_id = %s
                    {order_clause}
                    {limit_clause}
                    """,
                    (user_id,)
                )
                results = cur.fetchall()
                return [
                    {
                        "id": row[0],
                        "user_id": row[1],
                        "amount": row[2],
                        "currency": row[3],
                        "created_at": row[4]
                    }
                    for row in results
                ]
        finally:
            pg_client.release_connection(conn)