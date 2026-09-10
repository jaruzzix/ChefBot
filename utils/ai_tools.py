import requests
from data.config import ai_api_token, ai_model
import aiohttp


async def send_prompt(prompt: str, session: aiohttp.ClientSession):
    url = "https://api.puter.com/drivers/call"

    headers = {
        "Authorization": f"Bearer {ai_api_token}",
        "Content-Type": "application/json",
        "Origin": "https://puter.com",
    }

    payload = {
        "interface": "puter-chat-completion",
        "method": "complete",
        "args": {
            "model": ai_model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False
        }
    }

    try:
        async with session.post(url, headers=headers, json=payload) as response:

            if response.status != 200:
                print(f"Puter HTTP Error: {response.status}")
                return None

            data = await response.json()
            if not data.get("success"):
                print(f"Puter API Error: {data.get("error")}")
                return None

            return data["result"]["message"]["content"]

    except Exception as err_:
        print(f"Puter Exception: {err_}")
        return None


def parse_recipes_list(recipes: str):
    if recipes == "no_recipes":
        return None

    return recipes.split("|")

__all__=['send_prompt', 'parse_recipes_list']