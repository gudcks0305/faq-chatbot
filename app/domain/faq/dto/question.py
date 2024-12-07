from openai import BaseModel

from app.domain.base.pydantic_base import Schema


class QuestionRequest(Schema):
    question: str
