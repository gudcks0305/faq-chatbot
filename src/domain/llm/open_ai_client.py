import json
from typing import AsyncGenerator, Generator

from nest.core import Injectable
from openai import OpenAI, Stream
from openai.types.chat import ChatCompletionChunk

from src.config.env_variable import get_settings


def chat_stream_generator(stream: Stream[ChatCompletionChunk]) -> Generator:
    for chunk in stream:
        chunk_dict = chunk.model_dump()
        chunk_content = chunk_dict["choices"][0]["delta"].get("content")
        if chunk_content is None:
            continue
        yield chunk_content


async def chat_stream_generator_async(stream):
    async for chunk in stream:  # 비동기로 청크를 기다림
        chunk_dict = chunk.model_dump()
        chunk_content = chunk_dict["choices"][0]["delta"].get("content")
        if chunk_content is None:
            continue
        yield chunk_content

settings = get_settings()

@Injectable
class OpenAIClient:
    def __init__(self):
        self.api_key = settings.OPEN_API_KEY

    def get_client(self) -> OpenAI:
        return OpenAI(api_key=self.api_key)

    def get_text_embedding_ada2_vectors(self, text: str) -> list[float]:
        return (
            self.get_client()
            .embeddings.create(model="text-embedding-ada-002", input=text)
            .data[0]
            .embedding
        )

    def get_text_text_embedding_small_vectors(self, text: str) -> list[float]:
        return (
            self.get_client()
            .embeddings.create(model="text-embedding-3-small", input=text)
            .data[0]
            .embedding
        )

    def request_chat_completion(
        self, model: str = "gpt-4o-mini", question: str = ""
    ):
        return self.get_client().chat.completions.create(
            model=model, messages=[{"role": "user", "content": question}], temperature=0
        )

    def request_chat_completion_stream(
        self, model: str = "gpt-4o-mini", question: str = "", history: list[dict] = []
    ) -> Stream[ChatCompletionChunk]:
        return self.get_client().chat.completions.create(
            model=model,
            messages=[*history,{"role": "user", "content": question}],
            stream=True,
            temperature=0,
        )

    def request_chat_completions_stream(
        self, model: str = "gpt-4o-mini", messages: list[dict[str, str]] = []
    ) -> Stream[ChatCompletionChunk]:
        return self.get_client().chat.completions.create(
            model=model, messages=messages, stream=True, temperature=0
        )
