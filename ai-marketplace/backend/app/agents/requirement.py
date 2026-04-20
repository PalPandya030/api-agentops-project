def parse_requirements(user_input: str):
    # Simple keyword-based parsing (can upgrade to LLM later)

    req = {
        "budget": 10,
        "latency": 200,
        "accuracy": 90,
        "throughput": 100,
        "region": "global",
        "availability": 99,
        "priority": "balanced"
    }

    text = user_input.lower()

    if "cheap" in text:
        req["budget"] = 8
        req["priority"] = "cost"

    if "fast" in text:
        req["latency"] = 100
        req["priority"] = "speed"

    if "high accuracy" in text:
        req["accuracy"] = 95

    if "india" in text:
        req["region"] = "india"

    return req