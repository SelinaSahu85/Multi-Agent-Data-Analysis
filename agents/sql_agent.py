import json
from pathlib import Path

from tools.llm import get_json_llm
from tools.schema_tool import get_required_schema
from tools.sql_validator import validate_sql
from tools.database_tool import execute_query

from models.sql_model import SQLOutput


llm = get_json_llm()


def sql_agent(state):

    intent = state["intent"]
    plan = state["plan"]

    required_tables = plan["required_tables"]

    schema_context = get_required_schema(
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

Previous Validation Error:

{validation_error}
"""

        response = llm.invoke(prompt)

        try:

            data = json.loads(
                response.content
            )

            sql_output = SQLOutput(
                **data
            )

        except Exception:

            print("\nInvalid JSON Returned:\n")
            print(response.content)

            continue

        sql_query = sql_output.sql_query

        is_valid, error = validate_sql(
            sql_query
        )

        if is_valid:

            print("\nSQL Validation Passed\n")

            try:

                result_df = execute_query(
                    sql_query
                )

                state["sql_query"] = (
                    sql_query
                )

                state["sql_explanation"] = (
                    sql_output.explanation
                )

                state["query_results"] = (
                    result_df.to_dict(
                        orient="records"
                    )
                )

                state["sql_validation"] = (
                    "Passed"
                )

                return state

            except Exception as db_error:

                validation_error = (
                    f"Execution Error: {db_error}"
                )

                print(
                    f"\nExecution Failed: {db_error}"
                )

        else:

            validation_error = error

            print(
                f"\nValidation Failed: {error}"
            )

    raise ValueError(
        f"Failed to generate valid SQL after {max_retries} attempts."
    )