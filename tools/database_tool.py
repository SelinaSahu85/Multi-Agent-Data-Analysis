import sqlite3
import pandas as pd

DB_PATH = "database/northwind.db"


def execute_query(sql_query: str):
    """
    Execute SQL query and return Pandas DataFrame
    """

    conn = sqlite3.connect(DB_PATH)

    try:

        df = pd.read_sql_query(
            sql_query,
            conn
        )

        return df

    finally:

        conn.close()


def get_connection():
    """
    Return SQLite connection
    """

    return sqlite3.connect(DB_PATH)