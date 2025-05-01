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

# Instance global
pg_client = PostgresClient()