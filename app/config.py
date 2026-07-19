
import os
from openai import OpenAI

MAX_REQUEST_LIMIT = 2
RATE_LIMIT_WINDOW = 60

client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com")

