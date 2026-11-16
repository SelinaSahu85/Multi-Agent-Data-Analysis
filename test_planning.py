from agents.planning_agent import planning_agent

state = {
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
    }
}

result = planning_agent(state)

print(result["plan"])