def requirement_agent(query):

    requirements = {
        "service": None,
        "cost_priority": False,
        "latency_priority": False,
        "reliability_priority": False
    }

    query = query.lower()

    # detect service type
    if "translation" in query:
        requirements["service"] = "translation"

    if "payment" in query:
        requirements["service"] = "payment"

    if "nlp" in query:
        requirements["service"] = "nlp"

    # detect cost priority
    if "low cost" in query or "cheap" in query:
        requirements["cost_priority"] = True

    # detect latency priority
    if "fast" in query or "low latency" in query:
        requirements["latency_priority"] = True

    # detect reliability priority
    if "reliable" in query or "high uptime" in query:
        requirements["reliability_priority"] = True

    return requirements