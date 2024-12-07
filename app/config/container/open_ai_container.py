from functools import lru_cache

from openai import OpenAI

from app.config.env_variable import get_settings

settings = get_settings()
OPEN_API_KEY = settings.OPEN_API_KEY
class OpenAIClient:
    def __init__(self):
        self.api_key = OPEN_API_KEY

    def get_client(self):
        return OpenAI(api_key=self.api_key)

    def get_text_embedding_ada2_vectors(self, text: str)->list[float]:
        return self.get_client().embeddings.create(
            model="text-embedding-ada-002",
            input=text
        ).data[0].embedding

@lru_cache
def get_openai_client():
    return OpenAIClient()