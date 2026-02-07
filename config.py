# config.py
import os
from dotenv import load_dotenv

# Carrega .env
load_dotenv()

def get_env(name: str, required: bool = True, default=None):
    value = os.getenv(name, default)
    if required and not value:
        raise RuntimeError(f"Variável de ambiente '{name}' não configurada.")
    return value

# Trello
TRELLO_API_KEY = get_env("TRELLO_API_KEY", required=False)
TRELLO_TOKEN = get_env("TRELLO_TOKEN", required=False)
TRELLO_LIST_ID = get_env("TRELLO_LIST_ID", required=False)
TRELLO_NEXT_LIST_ID = get_env("TRELLO_NEXT_LIST_ID", required=False)

# Webhook
WEBHOOK_URL = get_env("WEBHOOK_URL", required=False)
WEBHOOK_PORT = int(get_env("WEBHOOK_PORT", default="5000"))

# LLM
LLM_API_KEY = get_env("LLM_API_KEY", required=False)
LLM_MODEL = get_env("LLM_MODEL", default="sabiazinho-3")
LLM_BASE_URL = get_env("LLM_BASE_URL", required=False, default="https://chat.maritaca.ai/api")

# Logging
LOG_LEVEL = get_env("LOG_LEVEL", default="INFO")
