from dotenv import load_dotenv
import os

load_dotenv()

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "llama3.2"
)

DB_PATH = os.getenv(
    "DB_PATH",
    "database/northwind.db"
)

MAX_SQL_RETRIES = int(
    os.getenv(
        "MAX_SQL_RETRIES",
        3
    )
)