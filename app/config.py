import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
MAX_REQUEST_LIMIT = 10
RATE_LIMIT_WINDOW = 60

# Max allowed upload size for audio endpoints (e.g. voice notes).
# Configurable via env var so it isn't a hardcoded magic number scattered across files.
MAX_FILE_SIZE = int(os.environ.get("MAX_FILE_SIZE", 25 * 1024 * 1024))  # 25 MB default

client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com")
