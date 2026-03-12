import pandas as pd

def negotiate_api():

    data = pd.read_csv("api_marketplace_agents/data/api_dataset.csv")

    # Reward function
    data["reward"] = (
        data["Reliability"] * 0.5
        - data["Cost"] * 20
        - data["Latency"] * 0.1
    )

    best_api = data.sort_values("reward", ascending=False).iloc[0]

    return best_api