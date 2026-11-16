import json
from pathlib import Path

from tools.llm import get_json_llm
from models.intent_model import IntentOutput


llm = get_json_llm()


def intent_agent(state: dict):

    prompt_path = Path("prompts/intent_prompt.txt")

    system_prompt = prompt_path.read_text(
        encoding="utf-8"
    )

    prompt = f"""
    {system_prompt}

    Question:

    {state["user_query"]}

    Return ONLY JSON.
    """

    response = llm.invoke(prompt)

    response_text = response.content.strip()

    # Remove markdown fences if model returns them
    response_text = response_text.replace(
        "```json", ""
    ).replace(
        "```", ""
    ).strip()

    try:
        data = json.loads(response_text)

        validated_output = IntentOutput(
            **data
        )

        state["intent"] = (
            validated_output.model_dump()
        )

        return state

    except Exception as e:

        print("\nIntent Parsing Error\n")
        print(response.content)

        raise e