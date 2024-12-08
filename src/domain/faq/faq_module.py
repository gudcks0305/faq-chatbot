from nest.core import Module

from src.domain.faq.faq_controller import FaqController
from src.domain.faq.faq_search_repository import FaqSearchRepository
from src.domain.faq.faq_service import FaqService
from src.domain.faq.question_history_repository import \
    QuestionHistoryRepository
from src.domain.llm.open_ai_module import OpenAIModule
from src.domain.milvus.milvus_module import MilvusModule


@Module(
    imports=[OpenAIModule, MilvusModule],
    controllers=[FaqController],
    providers=[FaqService, FaqSearchRepository, QuestionHistoryRepository],
)
class FaqModule:
    pass
