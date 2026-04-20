import random

def evaluate_apis(apis, req):
    scored = []

    # ------------------- FILTER STEP -------------------
    filtered_apis = []

    for api in apis:
        # Budget filter
        if api.get("price", 0) > req.get("budget", 0) * 2:
            continue

        # Latency filter
        if api.get("latency", 0) > req.get("latency", 0) * 2:
            continue

        # Accuracy filter
        if api.get("accuracy", 0) < req.get("accuracy", 0) - 10:
            continue

        filtered_apis.append(api)

    # If nothing passes filter, fallback to all
    if not filtered_apis:
        filtered_apis = apis

    # ------------------- SCORING STEP -------------------
    for api in filtered_apis:
        score = 0
        priority = req.get("priority", "balanced")

        # 🔥 COST PRIORITY
        if priority == "cost":
            score += api.get("price", 0) * 0.6
            score += api.get("latency", 0) * 0.2
            score -= api.get("accuracy", 0) * 0.1

        # ⚡ SPEED PRIORITY
        elif priority == "speed":
            score += api.get("latency", 0) * 0.6
            score += api.get("price", 0) * 0.2
            score -= api.get("throughput", 0) * 0.2

        # ⚖️ BALANCED PRIORITY
        else:
            score += api.get("price", 0) * 0.4
            score += api.get("latency", 0) * 0.3
            score -= api.get("accuracy", 0) * 0.3

        # 🌍 REGION MATCH BONUS
        if api.get("region") == req.get("region"):
            score -= 5

        # 🎲 RANDOMNESS (prevents same output every time)
        score += random.uniform(-2, 2)

        scored.append((api, score))

    # ------------------- SORT -------------------
    scored_sorted = sorted(scored, key=lambda x: x[1])

    return scored_sorted