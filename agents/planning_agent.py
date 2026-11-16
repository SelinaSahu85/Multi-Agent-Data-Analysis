import json
from pathlib import Path

from tools.llm import get_json_llm
from models.planning_model import PlanOutput

llm = get_json_llm()


def planning_agent(state):

    intent = state["intent"]

    prompt_template = Path(
        "prompts/planning_prompt.txt"
    ).read_text(encoding="utf-8")

    prompt = f"""
{prompt_template}

Intent Information:

{json.dumps(intent, indent=2)}

Create the execution plan.
"""

    response = llm.invoke(prompt)

    try:

        data = json.loads(response.content)

        plan = PlanOutput(**data)

        state["plan"] = plan.model_dump()

        return state

    except Exception:

        print("\nRAW RESPONSE:\n")
        print(response.content)

        raise