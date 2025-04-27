from typing import Dict, List, Optional
from src.database.utils.helpers import sanitize_input
from src.database.client import pg_client
import bcrypt

class UserModel:
    def __init__(self):
        self.table = "users"

    def create(self, username: str, password: str, total_amount: float = 0.00, orders: int = 0) -> Optional[Dict]:
        data = sanitize_input({"username": username, "password": bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode(), "total_amount": total_amount, "orders": orders})
        conn = pg_client.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    f"INSERT INTO {self.table} (username, password, total_amount, orders) VALUES (%s, %s, %s, %s) RETURNING id, username, password, total_amount, orders",
                    (data["username"], data["password"], data["total_amount"], data["orders"])
                )
                conn.commit()
                result = cur.fetchone()
                if result:
                    return {
                        "id": result[0],
                        "username": result[1],
                        "password": result[2],
                        "total_amount": result[3],
                        "orders": result[4]
                    }
                return None
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            pg_client.release_connection(conn)

    def read(self, username: str) -> Optional[Dict]:
        conn = pg_client.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    f"SELECT id, username, password, total_amount, orders FROM {self.table} WHERE username = %s",
                    (username,)
                )
                result = cur.fetchone()
                if result:
                    return {
                        "id": result[0],
                        "username": result[1],
                        "password": result[2],
                        "total_amount": result[3],
                        "orders": result[4]
                    }
                return None
        finally:
            pg_client.release_connection(conn)

    def increment_orders(self, user_id: int) -> Optional[Dict]:
        conn = pg_client.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    f"UPDATE {self.table} SET orders = orders + 1 WHERE id = %s RETURNING id, username, password, total_amount, orders",
                    (user_id,)
                )
                conn.commit()
                result = cur.fetchone()
                if result:
                    return {
                        "id": result[0],
                        "username": result[1],
                        "password": result[2],
                        "total_amount": result[3],
                        "orders": result[4]
                    }
                return None
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            pg_client.release_connection(conn)
            
    def auth_login(self, username: str, password: str) -> Optional[Dict]:
        conn = pg_client.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    f"SELECT id, username, password, total_amount, orders FROM {self.table} WHERE username = %s",
                    (username,)
                )
                result = cur.fetchone()
                if result and bcrypt.checkpw(password.encode(), result[2].encode()):
                    return {
                        "id": result[0],
                        "username": result[1],
                        "password": result[2],  # You can omit this if you don't want to return it
                        "total_amount": result[3],
                        "orders": result[4]
                    }
                return None
        finally:
            pg_client.release_connection(conn)
            
            
    def add_amount(self, username: str, amount_to_add: float) -> Optional[Dict]:
        conn = pg_client.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    f"""
                    UPDATE {self.table}
                    SET amount = amount + %s
                    WHERE username = %s
                    RETURNING id, username, password, total_amount, orders
                    """,
                    (amount_to_add, username)
                )
                conn.commit()
                result = cur.fetchone()
                if result:
                    return {
                        "id": result[0],
                        "username": result[1],
                        "password": result[2],
                        "total_amount": result[3],
                        "orders": result[4]
                    }
                return None
        finally:
            pg_client.release_connection(conn)

