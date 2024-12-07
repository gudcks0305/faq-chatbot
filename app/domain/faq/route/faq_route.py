from fastapi import APIRouter, Depends
from starlette.responses import StreamingResponse

from app.config.container.faq_container import get_faq_service
from app.domain.faq.dto.question import QuestionRequest
from app.domain.faq.service.faq_service import FaqService

router = APIRouter(prefix="/api/v1/faqs", tags=["faq"])


@router.post("/question/")
async def post_question(
    question_request: QuestionRequest,
    fqa_service: FaqService  = Depends(get_faq_service)
):
    return fqa_service.chat_request(question_request.question)