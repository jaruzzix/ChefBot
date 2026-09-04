import requests
from data.config import ai_api_token, ai_model
from app import logger


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
            logger.error(f"Puter HTTP Error: {response.status_code}")
            return None

        data = response.json()
        if not data.get("success"):
            logger.error(f"Puter API Error: {data.get("error")}")
            return None

        return data["result"]["message"]["content"]

    except Exception as err_:
        logger.error(f"Puter Exception: {err_}")
        return None

