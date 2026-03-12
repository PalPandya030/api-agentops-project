from agents.requirement_agent import requirement_agent
from agents.evaluation_agent import evaluate_api
from agents.negotiation_agent import negotiate_api
from agents.monitoring_agent import monitor_api

query = "I want a translation API with low cost and low latency"

# Step 1
requirements = requirement_agent(query)

print("User Requirements:")
print(requirements)

# Step 2
best_api = evaluate_api()

print("\nEvaluation Agent Selected:")
print(best_api["API"])

# Step 3
negotiated_api = negotiate_api()

print("\nNegotiation Agent Selected:")
print(negotiated_api["API"])

# Step 4
status = monitor_api(negotiated_api)

print("\nMonitoring Status:", status)