import pandas as pd

def evaluate_api():

    # Load dataset
    data = pd.read_csv("api_marketplace_agents/data/api_dataset.csv")

    # Calculate score (lower is better)
    data["score"] = (
        data["Cost"] * 0.4 +
        data["Latency"] * 0.3 -
        data["Reliability"] * 0.3
    )

    # Select best API
    best_api = data.sort_values("score").iloc[0]

    return best_api