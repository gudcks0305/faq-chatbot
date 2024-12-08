from typing import Any

from nest.core import Injectable
from pymilvus import Milvus, MilvusClient

from src.config.env_variable import get_settings

settings = get_settings()

@Injectable
class MilvusSearchClient:
    def __init__(self):
        self.client = MilvusClient("./data/milvus/db/demo.db")
        self.default_search_param = {"metric_type": "IP", "params": {"nprobe": 10}}

    def get_client(self):
        return self.client
