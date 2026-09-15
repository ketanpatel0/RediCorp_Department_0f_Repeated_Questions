import os

from dotenv import load_dotenv
from redisvl.index import SearchIndex

load_dotenv()

FAQ_INDEX_SCHEMA = {
    "index": {
        "name": "faq_index",
        "prefix": "faq:"  # all docs will use keys starting with this
    },
    "fields": [
        {"name": "question", "type": "text"},
        {"name": "answer", "type": "text"},
        {"name": "category", "type": "tag"},
        {
            "name": "embedding",
            "type": "vector",
            "attrs": {
                "dims": 384,  # dimension for the embedding model
                "algorithm": "hnsw",  # ANN index type
                "distance_metric": "cosine"
            }
        }
]
}
def get_faq_index(redis_url: str | None = None) -> SearchIndex:
    redis_url = redis_url or os.environ["REDIS_URL"]
    index = SearchIndex.from_dict(FAQ_INDEX_SCHEMA)
    index.connect(redis_url)
    return index