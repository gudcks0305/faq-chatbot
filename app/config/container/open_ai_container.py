from functools import lru_cache
from app.config.env_variable import get_settings
from app.domain.llm.open_ai_client import OpenAIClient

settings = get_settings()
OPEN_API_KEY = settings.OPEN_API_KEY


@lru_cache
def get_openai_client():
    return OpenAIClient(OPEN_API_KEY)