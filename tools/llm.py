from langchain_ollama import ChatOllama
from tools.config import OLLAMA_MODEL


def get_llm():

    return ChatOllama(
        model=OLLAMA_MODEL,
        temperature=0
    )


def get_json_llm():

    return ChatOllama(
        model=OLLAMA_MODEL,
        temperature=0,
        format="json"
    )