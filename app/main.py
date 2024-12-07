from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from app.domain.faq.route.faq_route import router as faq_router

app = FastAPI(docs_url=("/docs"), redoc_url="/redoc")
app.include_router(router=faq_router)
