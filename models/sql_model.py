from pydantic import BaseModel


class SQLOutput(BaseModel):

    sql_query: str

    explanation: str
