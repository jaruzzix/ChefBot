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

__all__ = ['bot_token', 'ai_api_token', 'db_data']
