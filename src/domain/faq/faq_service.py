import json

from nest.core import Injectable
from pymilvus import Hits

from src.domain.faq.faq_search_repository import FaqSearchRepository
from src.domain.faq.question_history_repository import QuestionHistoryRepository
from src.domain.llm.open_ai_client import OpenAIClient, chat_stream_generator
from src.domain.llm.prompt.question_promt import generate_question_prompt


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

    def chat_request_stream(self, question: str):
        made_prompt, question_text_embedding = self._prepare_prompt_and_embedding(question)
        response_stream = self.openai_client.request_chat_completion_stream(question=made_prompt)

        stream_data = []
        for chunk in chat_stream_generator(response_stream):
            stream_data.append(chunk)
            yield chunk

        self._update_question_history("test", question_text_embedding, question, "".join(stream_data))

    def _prepare_prompt_and_embedding(self, question: str) -> tuple[str, list[float]]:
        last_answer = self.question_history_repository.get_last_answer_by_user_id("test") or ""
        question_last_answer_text_embedding = self.openai_client.get_text_text_embedding_small_vectors(question + last_answer)
        question_text_embedding = self.openai_client.get_text_text_embedding_small_vectors(question)
        ranked_faq_list = self.faq_repository.search_faq(
            [question_last_answer_text_embedding],
            top_k=3,
            search_param={"metric_type": "IP", "params": {"nprobe": 10}},
            output_fields=["faq_index","question","answer"],
            anns_field="embedding",
        )
        if last_answer:
            ranked_faq_list.extend(self.faq_repository.search_faq(
                [question_text_embedding],
                top_k=3,
                search_param={"metric_type": "IP", "params": {"nprobe": 10}},
                output_fields=["faq_index","question","answer"],
                anns_field="embedding",
            ))


        grouped_faq_list = self._group_faqs_by_index(ranked_faq_list)
        faqs = "\n".join(json.dumps(answer, ensure_ascii=False) for answer in self._extract_answers_question(grouped_faq_list))
        question_history_llm_message = self.question_history_repository.generate_llm_history_message_by_user_id("test", limit=5)

        made_prompt = generate_question_prompt(
            question=question,
            search_data=faqs,
            question_history_llm_message=question_history_llm_message,
        )
        return made_prompt, question_last_answer_text_embedding

    def _group_faqs_by_index(self, ranked_faq_list: list[Hits]) -> dict:
        grouped_faq_list = {}
        for faq in ranked_faq_list:
            for faq_ in faq:
                faq_index = faq_["entity"]["faq_index"]
                grouped_faq_list.setdefault(faq_index, []).append(faq_)
        return grouped_faq_list

    def _extract_answers_question(self, grouped_faq_list: dict) -> list[dict]:
        return [
            {"faq_index": faq_index, "answer": faqs[0]["entity"]["answer"], "question": faqs[0]["entity"]["question"], "distance": faqs[0]["distance"]}
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