from nest.core import Module

from src.config.env_variable import get_settings
from src.domain.llm.open_ai_client import OpenAIClient

settings = get_settings()
@Module(
    imports=[],
    controllers=[],
    providers=[

    ],
    exports=[
        OpenAIClient,
    ],
)
class OpenAIModule:
    pass
