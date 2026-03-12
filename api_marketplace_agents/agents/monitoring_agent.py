import random

def monitor_api(api):

    # Simulated latency check
    simulated_latency = random.randint(80, 250)

    print("\nMonitoring API Performance...")
    print("Current Latency:", simulated_latency)

    threshold = 200

    if simulated_latency > threshold:
        print("⚠ API latency too high! Switching provider recommended.")
        status = "Switch API"
    else:
        print("✅ API performance is normal.")
        status = "Continue"

    return status