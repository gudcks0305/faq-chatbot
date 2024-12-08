from nest.core import Injectable

from src.domain.milvus.milvus_search_client import MilvusSearchClient


@Injectable
class FaqSearchRepository:
    def __init__(self, milvus_client: MilvusSearchClient):
        self.collection_name = "faq_collection"
        self.milvus_client = milvus_client
        milvus_client.client.load_collection(self.collection_name)

    def search_faq(
        self,
        vectors: list[list[float]],
        top_k: int,
        search_param: dict[str, str],
        output_fields: list[str],
        anns_field: str,
        expr,
    ):
        return self.milvus_client.get_client().search(
            collection_name=self.collection_name,
            data=vectors,
            limit=top_k,
            param=search_param,
            output_fields=output_fields,
            anns_field=anns_field,
            expression=expr,
        )
