# tools/schema_tool.py

import sqlite3
from pprint import pprint

DB_PATH = "database/northwind.db"


def get_connection():
    """
    Create SQLite connection
    """
    return sqlite3.connect(DB_PATH)


def get_tables():
    """
    Returns list of all table names
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table';
    """)

    tables = [
        row[0]
        for row in cursor.fetchall()
    ]

    conn.close()

    return tables


def get_table_columns(table_name):
    """
    Returns columns for a specific table
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        f"PRAGMA table_info({table_name})"
    )

    columns = [
        column[1]
        for column in cursor.fetchall()
    ]

    conn.close()

    return columns


def get_schema():
    """
    Returns entire schema as dictionary

    Example:

    {
        "customers": [
            "CustomerID",
            "CompanyName"
        ],
        "orders": [
            "OrderID",
            "OrderDate"
        ]
    }
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table';
    """)

    tables = cursor.fetchall()

    schema = {}

    for table in tables:

        table_name = table[0]

        cursor.execute(
            f"PRAGMA table_info({table_name})"
        )

        columns = cursor.fetchall()

        schema[table_name] = [
            column[1]
            for column in columns
        ]

    conn.close()

    return schema


def get_schema_text():
    """
    Convert schema into LLM-friendly text
    """

    schema = get_schema()

    schema_text = ""

    for table, columns in schema.items():

        schema_text += f"\nTable: {table}\n"

        for column in columns:
            schema_text += f"  - {column}\n"

    return schema_text.strip()


def get_required_schema(required_tables):
    """
    Return schema only for tables needed
    by the current query.

    Example:
    required_tables = [
        "orders",
        "order_details"
    ]
    """

    schema = get_schema()

    schema_text = ""

    for table in required_tables:

        if table not in schema:
            continue

        schema_text += f"\nTable: {table}\n"

        for column in schema[table]:
            schema_text += f"  - {column}\n"

    return schema_text.strip()


def print_schema():
    """
    Pretty print schema
    """

    pprint(get_schema())


if __name__ == "__main__":

    print("\nALL TABLES\n")
    print(get_tables())

    print("\nFULL SCHEMA\n")
    print_schema()

    print("\nSCHEMA TEXT\n")
    print(get_schema_text())