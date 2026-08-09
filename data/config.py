from dotenv import load_dotenv
import os

load_dotenv()

bot_token = os.getenv('BOT_TOKEN')
ai_api_token = os.getenv('AI_API_TOKEN')
proxy_server = os.getenv('PROXY_SERVER')

db_data = {
    "user": os.getenv('USER'),
    "database": os.getenv('DATABASE'),
    "host": os.getenv('HOST'),
    "port": os.getenv('PORT'),
    "password": os.getenv('PASSWORD')
}

__all__ = ['bot_token', 'ai_api_token', 'proxy_server', 'db_data']
