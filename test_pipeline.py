from agents.intent_agent import intent_agent
from agents.planning_agent import planning_agent
from agents.sql_agent import sql_agent


state = {
    "user_query": "Why did beverage sales decline in 1997?"
}

print("\n" + "="*80)
print("INTENT AGENT")
print("="*80)

state = intent_agent(state)

print(state["intent"])

print("\n" + "="*80)
print("PLANNING AGENT")
print("="*80)

state = planning_agent(state)

print(state["plan"])

print("\n" + "="*80)
print("SQL AGENT")
print("="*80)

state = sql_agent(state)

print("\nSQL QUERY\n")
print(state["sql_query"])

print("\nSQL VALIDATION\n")
print(state["sql_validation"])

print("\nRESULT COUNT\n")
print(len(state["query_results"]))

print("\nFIRST 5 RESULTS\n")

for row in state["query_results"][:5]:
    print(row)