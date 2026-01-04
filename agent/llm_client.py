from openai import OpenAI
from config import LLM_API_KEY, LLM_BASE_URL

def get_llm_client():
    if not LLM_API_KEY:
        raise RuntimeError("LLM_API_KEY não configurada")

    return OpenAI(
        api_key=LLM_API_KEY,
        base_url=LLM_BASE_URL
    )
