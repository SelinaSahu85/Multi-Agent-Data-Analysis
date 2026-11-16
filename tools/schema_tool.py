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
    Returns complete schema as dictionary
    """

    conn = get_connection()
    cursor = conn.cursor()

    tables = get_tables()

    schema = {}

    for table_name in tables:

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
    Returns entire schema as LLM-friendly text
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
    Returns schema only for required tables
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


def get_relationships():
    """
    Known Northwind relationships.

    Helps SQL Agent generate
    proper JOIN statements.
    """

    return """
Northwind Relationships:

customers.CustomerID = orders.CustomerID

employees.EmployeeID = orders.EmployeeID

orders.OrderID = order_details.OrderID

products.ProductID = order_details.ProductID

products.CategoryID = categories.CategoryID

products.SupplierID = suppliers.SupplierID

employee_territory.EmployeeID = employees.EmployeeID

employee_territory.TerritoryID = territories.TerritoryID

territories.RegionID = region.RegionID

orders.ShipVia = shippers.ShipperID

Important Notes:

OrderDate exists only in orders table.

Sales Revenue can be calculated using:

UnitPrice * Quantity * (1 - Discount)

Date filters should use:

orders.OrderDate
"""


def get_sql_context(required_tables):
    """
    Complete context passed to SQL Agent.

    Includes:
    1. Relevant schema
    2. Relationship information
    """

    schema_text = get_required_schema(
        required_tables
    )

    relationships = get_relationships()

    return f"""
DATABASE SCHEMA

{schema_text}

--------------------------------------------------

RELATIONSHIPS

{relationships}
"""


def print_schema():

    pprint(get_schema())


if __name__ == "__main__":

    print("\nTABLES\n")
    print(get_tables())

    print("\nFULL SCHEMA\n")
    print_schema()

    print("\nCOMPLETE SCHEMA TEXT\n")
    print(get_schema_text())

    print("\nSQL CONTEXT\n")
    print(
        get_sql_context([
            "products",
            "categories",
            "orders",
            "order_details"
        ])
    )