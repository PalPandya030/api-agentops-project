from fastapi import FastAPI

from api_marketplace_agents.agents.requirement_agent import requirement_agent
from api_marketplace_agents.agents.evaluation_agent import evaluate_api
from api_marketplace_agents.agents.negotiation_agent import negotiate_api
from api_marketplace_agents.agents.monitoring_agent import monitor_api

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API Marketplace AgentOps System Running"}

@app.post("/select-api")
def select_api(query: str):

    requirements = requirement_agent(query)

    best_api = evaluate_api()

    negotiated_api = negotiate_api()

    status = monitor_api(negotiated_api)

    return {
        "requirements": requirements,
        "selected_api": negotiated_api["API"],
        "monitoring_status": status
    }