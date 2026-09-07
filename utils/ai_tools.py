import requests
from data.config import ai_api_token, ai_model


def send_prompt(prompt: str):
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
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code != 200:
            print(f"Puter HTTP Error: {response.status_code}")
            return None

        data = response.json()
        if not data.get("success"):
            print(f"Puter API Error: {data.get("error")}")
            return None

        return data["result"]["message"]["content"]

    except Exception as err_:
        print(f"Puter Exception: {err_}")
        return None


def parse_recipes_list(recipes: str):
    return recipes.split("|")