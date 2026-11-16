from tools.schema_tool import (
    get_tables,
    get_schema,
    get_schema_text,
    get_required_schema
)

print("\nTABLES\n")
print(get_tables())

print("\nFULL SCHEMA\n")
print(get_schema())

print("\nLLM SCHEMA\n")
print(get_schema_text())

print("\nFILTERED SCHEMA\n")
print(
    get_required_schema([
        "products",
        "categories",
        "orders",
        "order_details"
    ])
)