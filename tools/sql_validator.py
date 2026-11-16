import sqlite3

DB_PATH = "database/northwind.db"

FORBIDDEN_KEYWORDS = [
    "DROP",
    "DELETE",
    "UPDATE",
    "INSERT",
    "ALTER",
    "TRUNCATE",
    "CREATE",
    "REPLACE",
    "ATTACH",
    "DETACH",
    "PRAGMA"
]


def validate_sql(sql_query: str):
    """
    Validate generated SQL before execution.

    Checks:
    1. Dangerous operations
    2. SQL syntax
    3. Table existence
    4. Column existence

    Returns:
        (True, None)
        (False, error_message)
    """

    sql_upper = sql_query.upper()

    # --------------------------------------------------
    # Forbidden Operation Check
    # --------------------------------------------------
    for keyword in FORBIDDEN_KEYWORDS:

        if keyword in sql_upper:

            return (
                False,
                f"Forbidden SQL operation detected: {keyword}"
            )

    conn = sqlite3.connect(DB_PATH)

    try:

        cursor = conn.cursor()

        # Parse SQL without executing full query
        cursor.execute(
            f"EXPLAIN QUERY PLAN {sql_query}"
        )

        conn.close()

        return True, None

    except Exception as e:

        conn.close()

        return False, str(e)