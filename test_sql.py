from agents.sql_agent import sql_agent

state = {

    "user_query":
    "Compare sales by category in 1997",

    "intent": {

        "business_question":
        "Compare sales by category in 1997",

        "metric": "Sales",

        "dimensions": [
            "Category"
        ],

        "filters": [],

        "time_period": "1997",

        "analysis_type":
        "comparison",

        "required_tables": [
            "products",
            "categories",
            "orders",
            "order_details"
        ]
    },

    "plan": {

        "objective":
        "Compare sales by category in 1997",

        "analysis_steps": [
            "Aggregate Sales by Category",
            "Rank Categories by Sales",
            "Compare Sales Performance"
        ],

        "required_tables": [
            "products",
            "categories",
            "orders",
            "order_details"
        ],

        "group_by": [
            "Category"
        ],

        "required_kpis": [
            "Sales"
        ]
    }
}

result = sql_agent(state)

print("\n" + "="*50)
print("SQL QUERY")
print("="*50)
print(result["sql_query"])

print("\n" + "="*50)
print("SQL EXPLANATION")
print("="*50)
print(result["sql_explanation"])

print("\n" + "="*50)
print("VALIDATION")
print("="*50)
print(result["sql_validation"])

print("\n" + "="*50)
print("ROWS RETURNED")
print("="*50)
print(len(result["query_results"]))

print("\n" + "="*50)
print("FIRST 5 RECORDS")
print("="*50)

for row in result["query_results"][:5]:
    print(row)