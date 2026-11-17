import json
from pathlib import Path

from tools.llm import get_llm

llm = get_llm()


def analysis_agent(state):

    prompt_template = Path(
        "prompts/analysis_prompt.txt"
    ).read_text(
        encoding="utf-8"
    )

    prompt = f"""
{prompt_template}

USER QUESTION:

{state["user_query"]}

INTENT:

{json.dumps(state["intent"], indent=2)}

EXECUTION PLAN:

{json.dumps(state["plan"], indent=2)}

QUERY RESULTS:

{json.dumps(state["query_results"][:20], indent=2)}
"""

    response = llm.invoke(prompt)

    state["analysis"] = response.content

    return state