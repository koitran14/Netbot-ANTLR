import os
import psycopg2
from psycopg2 import pool
from dotenv import load_dotenv

load_dotenv()

class PostgresClient:
    def __init__(self):
        self.uri = os.getenv("SUPABASE_DB_URI")
        if not self.uri:
            raise ValueError("SUPABASE_DB_URI must be set in .env")
        self.connection_pool = psycopg2.pool.SimpleConnectionPool(
            minconn=1,
            maxconn=10,
            dsn=self.uri
        )

    def get_connection(self):
        """Get a connection from the pool."""
        return self.connection_pool.getconn()

    def release_connection(self, conn):
        """Return a connection to the pool."""
        self.connection_pool.putconn(conn)

    def close_all(self):
        """Close all connections in the pool."""
        self.connection_pool.closeall()

    def insert(self, query, params):
        """Execute an INSERT query and return the result if available."""
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(query, params)
                conn.commit()
                if cur.description:
                    columns = [desc[0] for desc in cur.description]
                    row = cur.fetchone()
                    return dict(zip(columns, row)) if row else None
        finally:
            self.release_connection(conn)

    def get_order_history(self, user_id=None):
        """Retrieve order history for a specific user or all users."""
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                if user_id:
                    cur.execute("""
                        SELECT o.id, o.created_at, o.total,
                               oi.item_name, oi.quantity, oi.price
                        FROM orders o
                        LEFT JOIN order_items oi ON o.id = oi.order_id
                        WHERE o.user_id = %s
                        ORDER BY o.created_at DESC
                    """, (user_id,))
                else:
                    cur.execute("""
                        SELECT o.id, o.created_at, o.total,
                               oi.item_name, oi.quantity, oi.price
                        FROM orders o
                        LEFT JOIN order_items oi ON o.id = oi.order_id
                        ORDER BY o.created_at DESC
                    """)
                
                rows = cur.fetchall()
                history = {}
                for row in rows:
                    order_id, created_at, total, item_name, quantity, price = row
                    if order_id not in history:
                        history[order_id] = {
                            'order_id': order_id,
                            'created_at': created_at,
                            'total': total,
                            'items': []
                        }
                    history[order_id]['items'].append({
                        'name': item_name,
                        'quantity': quantity,
                        'price': price
                    })

                return list(history.values())
        finally:
            self.release_connection(conn)

# Instance global
pg_client = PostgresClient()