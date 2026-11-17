from agents.analysis_agent import analysis_agent

state = {

    "user_query":
    "Show top 10 best-selling products",

    "intent": {},

    "plan": {},

    "query_results": [
        {
            "ProductName": "Cte de Blaye",
            "Sales": 149984.2
        },
        {
            "ProductName": "Thringer Rostbratwurst",
            "Sales": 87736.4
        },
        {
            "ProductName": "Raclette Courdavault",
            "Sales": 76296.0
        }
    ]
}

state = analysis_agent(state)

print(state["analysis"])