from typing import Dict, List, Optional
from src.database.client import pg_client
from src.database.utils.helpers import sanitize_input
from src.database.models.user import UserModel

class OrderModel:
    def __init__(self):
        self.table = "orders"
        self.user_model = UserModel()

    def create(self, user_id: int, total_amount: float, status: str = "Pending") -> Optional[Dict]:
        data = sanitize_input({"user_id": user_id, "total_amount": total_amount, "status": status})
        conn = pg_client.get_connection()
        try:
            with conn.cursor() as cur:
                # Create order
                cur.execute(
                    f"INSERT INTO {self.table} (user_id, total_amount, status) VALUES (%s, %s, %s) RETURNING id, user_id, total_amount, status, created_at",
                    (data["user_id"], data["total_amount"], data["status"])
                )
                order_result = cur.fetchone()
                if not order_result:
                    return None

                # Increment user's order count
                self.user_model.increment_orders(data["user_id"])

                conn.commit()
                return {
                    "id": order_result[0],
                    "user_id": order_result[1],
                    "total_amount": order_result[2],
                    "status": order_result[3],
                    "created_at": order_result[4]
                }
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            pg_client.release_connection(conn)

    def read(self, order_id: int) -> Optional[Dict]:
        conn = pg_client.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    f"SELECT id, user_id, total_amount, status, created_at FROM {self.table} WHERE id = %s ORDER BY id DESC",
                    (order_id,)
                )
                result = cur.fetchone()
                if result:
                    return {
                        "id": result[0],
                        "user_id": result[1],
                        "total_amount": result[2],
                        "status": result[3],
                        "created_at": result[4]
                    }
                return None
        finally:
            pg_client.release_connection(conn)

    def list_by_user(self, user_id: int) -> List[Dict]:
        conn = pg_client.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    f"SELECT id, user_id, total_amount, status, created_at FROM {self.table} WHERE user_id = %s ORDER BY id DESC",
                    (user_id,)
                )
                results = cur.fetchall()
                return [
                    {"id": row[0], "user_id": row[1], "total_amount": row[2], "status": row[3], "created_at": row[4]}
                    for row in results
                ]
        finally:
            pg_client.release_connection(conn)