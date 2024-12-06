from app.container.milvus_container import MilvusSearchClient

# def define_collection_schema():
#     fields = [
#         FieldSchema(name="faq_id", dtype=DataType.INT64, is_primary=True, auto_id=True),
#         FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=1536),
#         FieldSchema(name="faq", dtype=DataType.JSON),
#     ]
#     return CollectionSchema(fields, description="FAQ collection")
class FaqSearchRepository:
    def __init__(self, milvus_client: MilvusSearchClient):
        self.collection = milvus_client.client.load_collection("faq_collection")

    def search_faq(self, vectors: list[list[float]], top_k: int, search_param: dict[str, str], output_fields: list[str], anns_field: str):
        return self.collection.search(
            data=vectors,
            limit=top_k,
            param=search_param,
            output_fields=output_fields,
            anns_field=anns_field
        )

