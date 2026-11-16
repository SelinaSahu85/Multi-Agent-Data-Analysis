import pandas as pd
import sqlite3

conn = sqlite3.connect("database/northwind.db")

df = pd.read_sql(
    "SELECT * FROM customers LIMIT 5",
    conn
)

print(df)

conn.close()