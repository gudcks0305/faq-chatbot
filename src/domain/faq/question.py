from src.domain.base.pydantic_base import Schema


class QuestionRequest(Schema):
    question: str
