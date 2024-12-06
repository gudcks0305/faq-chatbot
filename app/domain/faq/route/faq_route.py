from fastapi import APIRouter
from starlette.responses import StreamingResponse

router = APIRouter(prefix="/api/v1/faqs", tags=["faq"])


@router.post("/question/")
async def post_question():
    pass