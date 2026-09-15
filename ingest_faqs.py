from typing import List
from sentence_transformers import SentenceTransformer
from redisvl.index import SearchIndex
from redisvl.redis.utils import array_to_buffer
from faq_data import FAQ_DOCS
from faq_index import get_faq_index
def build_embeddings(texts: List[str]) -> List[list]:
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    vectors = model.encode(texts)
    return vectors.tolist()  # RedisVL wants plain Python lists
def main():
    # 1) Connect / create index
    index: SearchIndex = get_faq_index()
    # Drop index if it exists (to make reruns easy)
    index.create(overwrite=True, drop=True)
    print("Created index:", index.name)
    # 2) Prepare texts to embed (question + answer)
    texts = [
        f"{doc['question']} {doc['answer']}"
        for doc in FAQ_DOCS
    ]
    vectors = build_embeddings(texts)
# 3) Build RedisVL documents
    docs = []
    keys = []
    for doc, vec in zip(FAQ_DOCS, vectors):
        docs.append({
            "question": doc["question"],
            "answer": doc["answer"],
            "category": doc["category"],
            "embedding": array_to_buffer(vec, dtype="float32")
        })
        keys.append(doc["id"])  # e.g. "faq:1" -- already includes the index prefix
# 4) Add to Redis
    index.load(docs, keys=keys)
    print(f"Ingested {len(docs)} FAQ documents into Redis.")
if __name__ == "__main__":
    main()