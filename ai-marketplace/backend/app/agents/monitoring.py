def monitor(api):
    return {
        "uptime": "99%",
        "latency": api["latency"],
        "status": "Healthy"
    }