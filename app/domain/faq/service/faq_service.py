from pymilvus import Hits

from app.domain.faq.repository.faq_search_repository import FaqSearchRepository
from app.domain.llm.open_ai_client import OpenAIClient
from app.domain.llm.prompt.question_promt import get_question_prompt


class FaqService:
    def __init__(self, faq_repository: FaqSearchRepository,
        openai_client: OpenAIClient):
        self.faq_repository = faq_repository
        self.openai_client = openai_client

    def chat_request(self, question: str):
        made_prompt = self.make_rag_request(question)
        response_chat_completion = self.openai_client.request_chat_completion(
            question=made_prompt)

        return response_chat_completion

    def chat_request_stream(self, question: str):
        made_prompt = self.make_rag_request(question)
        response_chat_completion = self.openai_client.request_chat_completion_stream(
            question=made_prompt)

        return response_chat_completion

    def make_rag_request(self, question):
        question_text_embedding = self.openai_client.get_text_embedding_ada2_vectors(
            question)
        ranked_faq_list: list[Hits] = self.faq_repository.search_faq(
            [question_text_embedding], top_k=3, search_param={},
            output_fields=["faq"], anns_field="embedding")
        faq_list: list = [fa.entity.faq for fa in ranked_faq_list[0]]
        faqs = "\n".join(str(faq) for faq in faq_list)
        made_prompt: str = get_question_prompt(
            question=question,
            search_data=faqs
        )
        print(made_prompt)
        return made_prompt
