import json
from pathlib import Path

from tools.llm import get_llm
from tools.schema_tool import get_sql_context
from tools.sql_validator import (
    validate_sql,
    format_sql
)
from tools.database_tool import execute_query

llm = get_llm()


def sql_agent(state):

    intent = state["intent"]
    plan = state["plan"]

    required_tables = plan["required_tables"]

    schema_context = get_sql_context(
        required_tables
    )

    prompt_template = Path(
        "prompts/sql_prompt.txt"
    ).read_text(
        encoding="utf-8"
    )

    max_retries = 3

    validation_error = ""

    for attempt in range(max_retries):

        print("\n" + "=" * 80)
        print(f"SQL GENERATION ATTEMPT {attempt + 1}")
        print("=" * 80)

        prompt = f"""
{prompt_template}

DATABASE SCHEMA:

{schema_context}

USER QUESTION:

{state["user_query"]}

INTENT:

{json.dumps(intent, indent=2)}

EXECUTION PLAN:

{json.dumps(plan, indent=2)}

PREVIOUS VALIDATION ERROR:

{validation_error}
"""

        response = llm.invoke(prompt)

        sql_query = response.content.strip()

        # Remove markdown if model returns it
        sql_query = (
            sql_query
            .replace("```sql", "")
            .replace("```", "")
            .strip()
        )

        print("\n" + "=" * 80)
        print("RAW SQL")
        print("=" * 80)
        print(sql_query)

        print("\n" + "=" * 80)
        print("FORMATTED SQL")
        print("=" * 80)
        print(format_sql(sql_query))

        is_valid, error = validate_sql(
            sql_query,
            required_tables=required_tables
        )

        if is_valid:

            print("\n✅ SQL VALIDATION PASSED")

            try:

                result_df = execute_query(
                    sql_query
                )

                print("\n✅ QUERY EXECUTED SUCCESSFULLY")

                print("\nRESULT SHAPE:")
                print(result_df.shape)

                print("\nFIRST 5 ROWS:")
                print(result_df.head())

                state["sql_query"] = sql_query

                state["sql_validation"] = "Passed"

                state["query_results"] = (
                    result_df.to_dict(
                        orient="records"
                    )
                )

                return state

            except Exception as db_error:

                validation_error = (
                    f"Execution Error: {db_error}"
                )

                print("\n❌ QUERY EXECUTION FAILED")
                print(db_error)

        else:

            print("\n❌ SQL VALIDATION FAILED")
            print(error)

            validation_error = f"""
The previous SQL query failed validation.

Validation Error:
{error}

Generate a corrected SQLite query.

Requirements:
- Use SQLite syntax only
- Use only tables from the schema
- Use only columns from the schema
- Do not use PostgreSQL functions
- Do not use JSON_AGG
- Do not use JSON_OBJECT
- Do not use JSON_BUILD_OBJECT
- OrderDate exists only in the orders table
- Return only SQL
"""

    raise ValueError(
        f"Failed to generate valid SQL after {max_retries} attempts."
    )