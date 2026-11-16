from pathlib import Path
import sqlite3
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_DIR = BASE_DIR / "database" / "northwind"
DB_PATH = BASE_DIR / "database" / "northwind.db"

conn = sqlite3.connect(DB_PATH)

files = [
    "categories",
    "customers",
    "employee_territory",
    "employees",
    "order_details",
    "orders",
    "products",
    "region",
    "shippers",
    "suppliers",
    "territories"
]

for file in files:

    csv_path = DATASET_DIR / f"{file}.csv"

    print(f"Loading {csv_path}")

    df = pd.read_csv(csv_path)

    df.to_sql(
        file,
        conn,
        if_exists="replace",
        index=False
    )

conn.close()

print("Northwind database created successfully!")