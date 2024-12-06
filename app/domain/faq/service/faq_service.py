from app.domain.faq.repository.faq_search_repository import FaqSearchRepository


class FaqService:
    def __init__(self, faq_repository: FaqSearchRepository):
        self.faq_repository = faq_repository

    def chat_request(self, question: str):
        return self.faq_repository.search_faq(question)
