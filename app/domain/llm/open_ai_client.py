from openai import OpenAI


class OpenAIClient:
    def __init__(self, open_ai_key: str):
        self.api_key = open_ai_key

    def get_client(self) -> OpenAI:
        return OpenAI(api_key=self.api_key)

    def get_text_embedding_ada2_vectors(self, text: str)->list[float]:
        return self.get_client().embeddings.create(
            model="text-embedding-ada-002",
            input=text
        ).data[0].embedding

    def request_chat_completion(self, model: str = "gpt-4o-mini",question: str="")->str:
        return self.get_client().chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": question}
            ]
        )