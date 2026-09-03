from dotenv import load_dotenv
import os

load_dotenv()

bot_token = os.getenv('BOT_TOKEN')
ai_api_token = os.getenv('AI_API_TOKEN')

db_data = {
    "user": os.getenv('USER'),
    "database": os.getenv('DATABASE'),
    "host": os.getenv('HOST'),
    "port": os.getenv('PORT'),
    "password": os.getenv('PASSWORD')
}

base_url = os.getenv('BASE_URL')
webhook_url = f"{base_url}/webhook"

admin = os.getenv('ADMIN')

__all__ = ['bot_token', 'ai_api_token', 'db_data', 'webhook_url', 'base_url', 'admin']
