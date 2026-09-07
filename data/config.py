from dotenv import load_dotenv
import os

load_dotenv()

bot_token = os.getenv('BOT_TOKEN')

ai_api_token = os.getenv('AI_API_TOKEN')
ai_model = os.getenv('AI_MODEL')

db_data = {
    "user": os.getenv('USER'),
    "database": os.getenv('DATABASE'),
    "host": os.getenv('HOST'),
    "port": os.getenv('PORT'),
    "password": os.getenv('PASSWORD')
}

base_url = os.getenv('BASE_URL')
webhook_url = f"{base_url}/webhook"

prompts_dir = f"{os.path.dirname(os.path.abspath(__file__))}/ai/prompts"

max_page_length = int(os.getenv('MAX_PAGE_LENGTH'))
max_recipes_count = int(os.getenv('MAX_RECIPES_COUNT'))

__all__ = ['bot_token',
           'ai_api_token',
           'ai_model',
           'db_data',
           'webhook_url',
           'base_url',
           'prompts_dir',
           'max_page_length',
           'max_recipes_count']
