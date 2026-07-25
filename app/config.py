
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
MAX_REQUEST_LIMIT = 10
RATE_LIMIT_WINDOW = 60

client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com")

