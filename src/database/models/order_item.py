from typing import Dict, List, Optional
from src.database.client import pg_client
from src.database.utils.helpers import sanitize_input

class OrderItemModel:
    def __init__(self):
        self.table = "order_items"

    def create(self, order_id: int, menu_item_id: int, quantity: int, price_at_order: float) -> Optional[Dict]:
        data = sanitize_input({"order_id": order_id, "menu_item_id": menu_item_id, "quantity": quantity, "price_at_order": price_at_order})
        conn = pg_client.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    f"INSERT INTO {self.table} (order_id, menu_item_id, quantity, price_at_order) VALUES (%s, %s, %s, %s) RETURNING id, order_id, menu_item_id, quantity, price_at_order",
                    (data["order_id"], data["menu_item_id"], data["quantity"], data["price_at_order"])
                )
                conn.commit()
                result = cur.fetchone()
                if result:
                    return {
                        "id": result[0],
                        "order_id": result[1],
                        "menu_item_id": result[2],
                        "quantity": result[3],
                        "price_at_order": result[4]
                    }
                return None
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            pg_client.release_connection(conn)

    def list_by_order(self, order_id: int) -> List[Dict]:
        conn = pg_client.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    f"SELECT id, order_id, menu_item_id, quantity, price_at_order FROM {self.table} WHERE order_id = %s ORDER BY id DESC",
                    (order_id,)
                )
                results = cur.fetchall()
                return [
                    {"id": row[0], "order_id": row[1], "menu_item_id": row[2], "quantity": row[3], "price_at_order": row[4]}
                    for row in results
                ]
        finally:
            pg_client.release_connection(conn)