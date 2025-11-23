import mysql.connector
from mysql.connector import pooling


class Database:
    """
    Small wrapper around mysql-connector-python with a connection pool.

    This class is responsible for talking to MySQL: opening connections,
    running queries, and returning results as dictionaries.
    """

    def __init__(self):
        # Direct credentials for MySQL as you requested.
        self.pool = pooling.MySQLConnectionPool(
            pool_name="rental_pool",
            pool_size=5,
            host="localhost",
            user="root",
            password="1234",
            database="rentaldb",
        )

    def get_connection(self):
        """
        Get a connection from the pool.
        Caller must close it when done.
        """
        return self.pool.get_connection()

    def query_one(self, sql: str, params=None):
        """
        Run a SELECT query expected to return a single row.
        Returns a dict or None.
        """
        conn = self.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, params or ())
            row = cursor.fetchone()
            return row
        finally:
            cursor.close()
            conn.close()

    def query_all(self, sql: str, params=None):
        """
        Run a SELECT query expected to return multiple rows.
        Returns a list of dicts.
        """
        conn = self.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, params or ())
            rows = cursor.fetchall()
            return rows
        finally:
            cursor.close()
            conn.close()

    def execute(self, sql: str, params=None) -> int:
        """
        Run an INSERT/UPDATE/DELETE query.
        Returns lastrowid for INSERT or 0 for others.
        """
        conn = self.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, params or ())
            conn.commit()
            last_id = cursor.lastrowid
            return last_id
        finally:
            cursor.close()
            conn.close()

    def init_app(self, app):
        """
        Placeholder to match Flask extension pattern.
        We don't actually need 'app' here, but this keeps the interface
        similar to many Flask extensions.
        """
        # Nothing complex here; pool is created at __init__ time already.
        pass


# Single shared database object used by all models and services.
db = Database()
