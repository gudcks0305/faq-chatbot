from nest.core import Module

from src.domain.milvus.milvus_search_client import MilvusSearchClient


@Module(imports=[], controllers=[], providers=[], exports=[MilvusSearchClient])
class MilvusModule:
    pass
