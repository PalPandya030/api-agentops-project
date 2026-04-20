import asyncio
import httpx
from ranking import score_api

async def call_api(api, payload):
    async with httpx.AsyncClient() as client:
        try:
            res = await client.post(api.name, json=payload, timeout=5)
            return {"api": api.name, "result": res.json(), "score": score_api(api)}
        except:
            return None

async def orchestrate(apis, payload):
    tasks = [call_api(api, payload) for api in apis]
    results = await asyncio.gather(*tasks)
    results = [r for r in results if r]
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[0] if results else None