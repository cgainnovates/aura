import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("AURA_API_KEY")
MODEL = os.getenv("AURA_MODEL", "openai/gpt-oss-120b")
BASE_URL = os.getenv("AURA_BASE_URL", "https://api.groq.com/openai/v1")

if not API_KEY:
    raise SystemExit("Missing AURA_API_KEY. Set it in your .env file")