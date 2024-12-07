from fastapi import FastAPI
from app.domain.faq.route.faq_route import router as faq_router
app = FastAPI(
    docs_url=(
        "/docs"
    )
)

app.include_router(router=faq_router)
