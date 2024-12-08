from nest.core import Injectable
from pymilvus import Hits

from src.domain.faq.faq_search_repository import FaqSearchRepository
from src.domain.faq.question_history_repository import QuestionHistoryRepository
from src.domain.llm.open_ai_client import OpenAIClient, chat_stream_generator
from src.domain.llm.prompt.question_promt import get_question_prompt


@Injectable
class FaqService:
    def __init__(
        self,
        faq_repository: FaqSearchRepository,
        openai_client: OpenAIClient,
        question_history_repository: QuestionHistoryRepository,
    ):
        self.faq_repository = faq_repository
        self.openai_client = openai_client
        self.question_history_repository = question_history_repository

    def chat_request(self, question: str):
        made_prompt, _ = self._prepare_prompt_and_embedding(question)
        return self.openai_client.request_chat_completion(question=made_prompt)

    def chat_request_stream(self, question: str):
        made_prompt, question_text_embedding = self._prepare_prompt_and_embedding(question)
        response_stream = self.openai_client.request_chat_completion_stream(question=made_prompt)

        stream_data = []
        for chunk in chat_stream_generator(response_stream):
            stream_data.append(chunk)
            yield chunk  # Yield stream data in real-time

        self._update_question_history("test", question_text_embedding, question, "".join(stream_data))

    def _prepare_prompt_and_embedding(self, question: str) -> tuple[str, list[float]]:
        question_text_embedding = self.openai_client.get_text_text_embedding_small_vectors(question)
        ranked_faq_list = self.faq_repository.search_faq(
            [question_text_embedding],
            top_k=3,
            search_param={},
            output_fields=["faq_index", "answer"],
            anns_field="embedding",
        )

        grouped_faq_list = self._group_faqs_by_index(ranked_faq_list)
        faqs = "\n".join(str(answer) for answer in self._extract_answers(grouped_faq_list))

        made_prompt = get_question_prompt(
            question=question,
            question_history=[],  # Placeholder for question history
            search_data=faqs,
        )
        return made_prompt, question_text_embedding

    def _group_faqs_by_index(self, ranked_faq_list: list[Hits]) -> dict:
        grouped_faq_list = {}
        for faq in ranked_faq_list[0]:
            faq_index = faq.entity.faq_index
            grouped_faq_list.setdefault(faq_index, []).append(faq)
        return grouped_faq_list

    def _extract_answers(self, grouped_faq_list: dict) -> list[dict]:
        return [
            {"faq_index": faq_index, "answer": faqs[0].entity.answer}
            for faq_index, faqs in grouped_faq_list.items()
        ]

    def _update_question_history(self, user_id: str, question_vector: list[float], question: str, response: str):
        self.question_history_repository.add_history(
            user_id=user_id,
            vector=question_vector,
            question=question,
            role="user",
        )
        self.question_history_repository.add_history(
            user_id=user_id,
            vector=[],  # Add other data if necessary
            question=response,
            role="assistant",
        )