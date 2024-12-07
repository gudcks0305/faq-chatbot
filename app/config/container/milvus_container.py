from functools import lru_cache
from typing import Any

from pymilvus import Milvus

from app.config.env_variable import get_settings

settings = get_settings()
MILVUS_HOST, MILVUS_PORT = settings.MILVUS_HOST, settings.MILVUS_PORT


class MilvusSearchClient:
    def __init__(self):
        self.client = Milvus(MILVUS_HOST, MILVUS_PORT)
        self.default_search_param = {
            "metric_type": "IP",
            "params": {"nprobe": 10}
        }

    def search_vectors(self, collection_name: str, vectors: list[list[float]],
        top_k: int,
        param: dict[str, Any] = None,
        anns_field: str = "embedding"):
        return self.client.search(
            collection_name=
            collection_name,
            data=vectors,
            limit=top_k,
            param=self.default_search_param if not param else param,
            anns_field=anns_field
        )


@lru_cache
def get_milvus_client():
    return MilvusSearchClient()
