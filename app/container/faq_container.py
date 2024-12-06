from functools import lru_cache

from app.container.milvus_container import MilvusSearchClient
from app.domain.faq.repository.faq_search_repository import FaqSearchRepository

@lru_cache
def get_faq_repository(
    milvus_search_client: MilvusSearchClient
):
    return FaqSearchRepository(
        milvus_client=milvus_search_client
    )