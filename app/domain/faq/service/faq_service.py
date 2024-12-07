from pymilvus import Hits
from starlette.responses import StreamingResponse

from app.domain.faq.repository.faq_search_repository import FaqSearchRepository
from app.domain.faq.repository.question_history_repository import \
    QuestionHistoryRepository
from app.domain.llm.open_ai_client import OpenAIClient, chat_stream_generator
from app.domain.llm.prompt.question_promt import get_question_prompt


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
        made_prompt = self.make_rag_request(question)
        response_chat_completion = self.openai_client.request_chat_completion(
            question=made_prompt
        )

        return response_chat_completion

    def chat_request_stream(self, question: str):
        made_prompt, question_text_embedding = self.make_rag_request_and_text_embedding(
            question
        )
        response_chat_completion = self.openai_client.request_chat_completion_stream(
            question=made_prompt
        )

        stream = chat_stream_generator(response_chat_completion)
        stream_data = []

        for chunk in stream:
            stream_data.append(chunk)
            yield chunk  # 스트림 데이터를 실시간으로 반환
        self.question_history_repository.add_history(
            user_id="test",
            vector=question_text_embedding,
            question=question,
            role="user",
        )
        full_response = "".join(stream_data)
        self.question_history_repository.add_history(
            user_id="test",
            vector=[],  # 필요시 다른 데이터 추가
            question=full_response,
            role="assistant",
        )

        return stream

    def make_rag_request_and_text_embedding(self, question) -> tuple[str, list[float]]:
        question_text_embedding = self.openai_client.get_text_text_embedding_small_vectors(
            question
        )
        ranked_faq_list: list[Hits] = self.faq_repository.search_faq(
            [question_text_embedding],
            top_k=3,
            search_param={},
            output_fields=["faq_index", "answer"],
            anns_field="embedding",
        )
        # group by faq_index
        print(ranked_faq_list)
        grouped_faq_list = {}
        for faq in ranked_faq_list[0]:
            faq_index = faq.entity.faq_index
            if faq_index not in grouped_faq_list:
                grouped_faq_list[faq_index] = []
            grouped_faq_list[faq_index].append(faq)

        answer_list: list = []
        for faq_index, faqs in grouped_faq_list.items():
            faq = faqs[0].entity
            answer_list.append({
                "faq_index": faq_index,
                "answer": faq.answer,
            })
        faqs = "\n".join(str(answer) for answer in answer_list)
        # question_history = self.question_history_repository.get_history(user_id="test")
        made_prompt: str = get_question_prompt(
            question=question,
            # question_history=[q.question.join("---------------------") for q in question_history],
            question_history=[],
            search_data=faqs,
        )
        print(made_prompt)
        return made_prompt, question_text_embedding
