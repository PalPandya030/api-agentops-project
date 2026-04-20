import os
import requests

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def get_ai_explanation(requirements, selected_api, top_apis):
    try:
        if not OPENROUTER_API_KEY:
            return "⚠️ API key missing"

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "meta-llama/llama-3-8b-instruct",  # ✅ WORKING
                "messages": [
                    {
                        "role": "user",
                        "content": f"""
User Requirements: {requirements}
Top APIs: {top_apis}
Selected API: {selected_api}

Explain why this API is best in simple terms.
"""
                    }
                ]
            }
        )

        data = response.json()
        print("OpenRouter response:", data)

        if "choices" not in data:
            return f"⚠️ OpenRouter error: {data}"

        return data["choices"][0]["message"]["content"]

    except Exception as e:
        return f"⚠️ Exception: {str(e)}"