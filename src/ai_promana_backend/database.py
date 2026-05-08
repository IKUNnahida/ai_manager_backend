from typing import Generator
import pymysql
from ai_promana_backend.config import settings

def get_connection() -> pymysql.connections.Connection:
    return pymysql.connect(
        host=settings.MYSQL_HOST,
        port=settings.MYSQL_PORT,
        user=settings.MYSQL_USER,
        password=settings.MYSQL_PASSWORD,
        database=settings.MYSQL_DATABASE,
        charset="utf8mb4",
        autocommit=False,
        cursorclass=pymysql.cursors.DictCursor
    )

def get_db() -> Generator[pymysql.connections.Connection, None, None]:
    """FastAPI dependency that yields a pymysql connection."""
    conn = get_connection()
    try:
        yield conn
    finally:
        try:
            conn.close()
        except Exception:
            pass
