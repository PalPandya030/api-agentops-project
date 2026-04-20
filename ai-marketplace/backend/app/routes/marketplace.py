from fastapi import APIRouter
import random
from app.llm import get_ai_explanation

router = APIRouter()

# ================= GLOBAL DATA =================
history = []
total_revenue = 0
total_requests = 0
api_usage = {}

# ================= DATASET =================
apis = [
    {"name": "FastVision", "price": 12, "latency": 100, "accuracy": 95},
    {"name": "TurboVision", "price": 13, "latency": 85, "accuracy": 93},
    {"name": "CheapVision", "price": 8, "latency": 200, "accuracy": 85},
    {"name": "UltraAI", "price": 15, "latency": 70, "accuracy": 97},
    {"name": "BudgetAI", "price": 6, "latency": 250, "accuracy": 80},
    {"name": "GlobalAI", "price": 10, "latency": 120, "accuracy": 90},
    {"name": "SmartVision", "price": 11, "latency": 110, "accuracy": 92},
]

# ================= SMART EVALUATION =================
def evaluate_apis(requirements):
    scored = []

    for api in apis:
        score = 0

        # Budget
        if api["price"] <= requirements["budget"]:
            score += 30
        else:
            score -= (api["price"] - requirements["budget"]) * 2

        # Latency
        if api["latency"] <= requirements["latency"]:
            score += 25
        else:
            score -= (api["latency"] - requirements["latency"]) * 0.5

        # Accuracy
        if api["accuracy"] >= requirements["accuracy"]:
            score += 35
        else:
            score -= (requirements["accuracy"] - api["accuracy"]) * 2

        # Region bonus
        if requirements["region"] == "global":
            score += 10

        scored.append({**api, "score": round(score, 2)})

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:3]

# ================= NEGOTIATE =================
@router.post("/negotiate")
def negotiate(user_input: str):
    global total_revenue, total_requests, api_usage

    requirements = {
        "budget": 8 if "cheap" in user_input else 15,
        "latency": 80 if "fast" in user_input else 150,
        "accuracy": 95 if "high accuracy" in user_input else 85,
        "region": "global",
        "query": user_input
    }

    top_apis = evaluate_apis(requirements)

    selected_api = top_apis[0]["name"]
    original_price = top_apis[0]["price"]

    discount = random.uniform(0.5, 2.5)
    final_price = round(original_price - discount, 2)

    # TRACKING
    total_requests += 1
    total_revenue += final_price
    api_usage[selected_api] = api_usage.get(selected_api, 0) + 1

    monitoring = {
        "uptime": "99%",
        "latency": top_apis[0]["latency"],
        "status": "Healthy"
    }

    explanation = get_ai_explanation(requirements, selected_api, top_apis)

    history.append({
        "selected_api": selected_api,
        "final_price": final_price,
        "query": user_input
    })

    return {
        "requirements": requirements,
        "selected_api": selected_api,
        "original_price": original_price,
        "final_price": final_price,
        "top_apis": top_apis,
        "monitoring": monitoring,
        "explanation": explanation
    }

# ================= ANALYTICS =================
@router.get("/analytics")
def analytics():
    return {
        "revenue": round(total_revenue, 2),
        "requests": total_requests,
        "usage": api_usage,
        "history": history[-10:]
    }

# ================= BEHAVIOR =================
@router.get("/behavior")
def behavior():
    queries = [h["query"] for h in history]

    return {
        "total_queries": len(queries),
        "popular_queries": list(set(queries))[:5]
    }

# ================= HISTORY =================
@router.get("/history")
def get_history():
    return history