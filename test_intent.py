from agents.intent_agent import intent_agent

state = {
    "user_query":
    "Compare sales by category in 1997"
}

result = intent_agent(state)

print(result["intent"])