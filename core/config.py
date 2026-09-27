import os
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
HINDSIGHT_API_KEY = os.getenv("HINDSIGHT_API_KEY", "").strip()
HINDSIGHT_BASE_URL = os.getenv("HINDSIGHT_BASE_URL", "https://api.hindsight.vectorize.io").strip()
HINDSIGHT_BANK_ID = os.getenv("HINDSIGHT_BANK_ID", "dealmind-memory").strip()

def validate_config():
    missing = []
    if not GROQ_API_KEY:
        missing.append("GROQ_API_KEY")
    if not HINDSIGHT_API_KEY:
        missing.append("HINDSIGHT_API_KEY")
    if missing:
        raise ValueError(f"Missing required environment variables in .env: {', '.join(missing)}")