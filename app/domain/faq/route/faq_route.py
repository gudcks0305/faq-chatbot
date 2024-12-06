from fastapi import APIRouter
router = APIRouter(prefix="/api/v1/faqs", tags=["faq"])


@router.post("/question/")
async def post_question():
    pass
