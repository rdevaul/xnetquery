import os
from dotenv import load_dotenv

load_dotenv()

CONFIG = {
    "API_BASE_URL": os.getenv("API_BASE_URL"),
    "LLM_PROVIDER": os.getenv("LLM_PROVIDER"),
    "LLM_MODEL": os.getenv("LLM_MODEL"),
    "LLM_LOCAL_ENDPOINT": os.getenv("LLM_LOCAL_ENDPOINT"),
    "TERMINAL_TIMEOUT": int(os.getenv("TERMINAL_TIMEOUT", 3600)),
    "REFRESH_WINDOW": int(os.getenv("REFRESH_WINDOW", 300)),
}
