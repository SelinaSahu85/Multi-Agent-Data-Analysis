import sqlite3
import sqlglot
from sqlglot import exp

DB_PATH = "database/northwind.db"

# ----------------------------------------
# Dangerous Operations
# ----------------------------------------

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

# ----------------------------------------
# Unsupported SQL Functions
# ----------------------------------------

FORBIDDEN_FUNCTIONS = [
    "JSON_AGG",
    "JSON_OBJECT",
    "JSON_OBJECT_AGG",
    "JSON_BUILD_OBJECT",
    "JSONBUILDOBJECT",
    "ARRAY_AGG"
]


def extract_tables(sql_query: str):
    """
    Extract table names from query using SQLGlot
    """

    tree = sqlglot.parse_one(
        sql_query,
        dialect="sqlite"
    )

    return {
        table.name.lower()
        for table in tree.find_all(exp.Table)
    }


def format_sql(sql_query: str):
    """
    Format SQL nicely
    """

    try:

        return sqlglot.transpile(
            sql_query,
            read="sqlite",
            pretty=True
        )[0]

    except Exception:

        return sql_query


def validate_sql(
    sql_query: str,
    required_tables: list = None
):
    """
    Validation Flow

    1. Forbidden keyword check
    2. Forbidden function check
    3. SQLGlot parse check
    4. Required table check
    5. SQLite EXPLAIN validation

    Returns:
        (True, None)
        (False, error_message)
    """

    sql_upper = sql_query.upper()

    # ----------------------------------------
    # Dangerous SQL
    # ----------------------------------------

    for keyword in FORBIDDEN_KEYWORDS:

        if keyword in sql_upper:

            return (
                False,
                f"Forbidden SQL operation detected: {keyword}"
            )

    # ----------------------------------------
    # Unsupported Functions
    # ----------------------------------------

    for function in FORBIDDEN_FUNCTIONS:

        if function in sql_upper:

            return (
                False,
                f"Forbidden SQL function detected: {function}"
            )

    for column in FORBIDDEN_KEYWORDS:

      if column in sql_upper:

        return (
            False,
            f"Invalid column usage detected: {column}"
        )
    # ----------------------------------------
    # SQLGlot Validation
    # ----------------------------------------

    try:

        sqlglot.parse_one(
            sql_query,
            dialect="sqlite"
        )

    except Exception as e:

        return (
            False,
            f"SQLGlot Syntax Error: {e}"
        )

    # ----------------------------------------
    # Required Tables Validation
    # ----------------------------------------

    if required_tables:

        try:

            used_tables = extract_tables(
                sql_query
            )

            required = {
                table.lower()
                for table in required_tables
            }

            missing_tables = (
                required - used_tables
            )

            if missing_tables:

                return (
                    False,
                    f"Missing required tables: {missing_tables}"
                )

        except Exception as e:

            return (
                False,
                f"Table extraction failed: {e}"
            )

    # ----------------------------------------
    # SQLite Validation
    # ----------------------------------------

    conn = sqlite3.connect(DB_PATH)

    try:

        cursor = conn.cursor()

        cursor.execute(
            f"EXPLAIN QUERY PLAN {sql_query}"
        )

        conn.close()

        return True, None

    except Exception as e:

        conn.close()

        return False, str(e)