from functools import lru_cache

from nest.core import Injectable


class QuestionHistory:
    def __init__(
        self, user_id: str, vector: list[float], question: str, role: str = "user"
    ):
        self.user_id = user_id
        self.vector = vector
        self.question = question
        self.role = role


@Injectable
class QuestionHistoryRepository:
    def __init__(self):
        self.history: dict[str, list[QuestionHistory]] = {}

    def add_history(
        self, user_id: str, vector: list[float], question: str, role: str = "user"
    ):
        if user_id not in self.history:
            self.history[user_id] = []
        self.history[user_id].append(QuestionHistory(user_id, vector, question, role))

        return self.history[user_id]

    def get_history(self, user_id: str) -> list[QuestionHistory]:
        return self.history.get(user_id, [])

    def clear_history(self, user_id: str):
        self.history[user_id] = []
