from fastapi import APIRouter, Depends
from starlette.responses import StreamingResponse

from app.config.container.faq_container import get_faq_service
from app.domain.faq.dto.question import QuestionRequest
from app.domain.faq.service.faq_service import FaqService
from app.domain.llm.open_ai_client import chat_stream_generator

router = APIRouter(prefix="/api/v1/faqs", tags=["faq"])


@router.post("/question/")
async def post_question(
    question_request: QuestionRequest,
    fqa_service: FaqService  = Depends(get_faq_service)
):
    return fqa_service.chat_request(question_request.question)

@router.post("/question/stream")
async def post_question_stream(
    question_request: QuestionRequest,
    fqa_service: FaqService  = Depends(get_faq_service)
):
    chunk = chat_stream_generator(fqa_service.chat_request_stream(question_request.question))
    return StreamingResponse(chunk, media_type="text/event-stream")