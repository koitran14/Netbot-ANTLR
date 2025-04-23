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
        # Initialize connection pool
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

pg_client = PostgresClient()