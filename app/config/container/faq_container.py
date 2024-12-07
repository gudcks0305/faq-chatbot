from functools import lru_cache

from app.config.container.milvus_container import MilvusSearchClient, \
    get_milvus_client
from app.config.container.open_ai_container import get_openai_client
from app.domain.faq.repository.faq_search_repository import FaqSearchRepository
from app.domain.faq.repository.question_history_repository import \
    get_question_history_repository
from app.domain.faq.service.faq_service import FaqService
from app.domain.llm.open_ai_client import OpenAIClient


@lru_cache
def get_faq_repository(
):
    return FaqSearchRepository(
        get_milvus_client()
    )


@lru_cache
def get_faq_service():
    return FaqService(
        faq_repository=get_faq_repository(), openai_client=get_openai_client(),
        question_history_repository=get_question_history_repository()
    )
