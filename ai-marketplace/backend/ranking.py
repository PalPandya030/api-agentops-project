def score_api(api):
    return (api.accuracy * 0.4) + (1/api.latency * 0.3) + (api.success_rate * 0.3)