from nest.core import Controller, Post
from starlette.responses import StreamingResponse

from src.domain.faq.faq_service import FaqService
from src.domain.faq.question import QuestionRequest


@Controller("/api/v1/faqs", tag="faq")
class FaqController:
    def __init__(self, service: FaqService):
        self.service = service

    @Post("/question/stream")
    def post_question_stream(self, question_request: QuestionRequest):
        stream = self.service.chat_request_stream(question_request.question)
        return StreamingResponse(stream, media_type="text/event-stream")
