from sentence_transformers import SentenceTransformer
from redisvl.query import VectorQuery
from faq_index import get_faq_index

test_queries = [
    "Is Redis only a cache?",
    "How do I keep my data if Redis is in memory?",
    "What's the difference between a cache and a database?",
]

def main():
    index = get_faq_index()
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    for q in test_queries:
        vec = model.encode([q]).tolist()[0]
        query = VectorQuery(
            vector=vec,
            vector_field_name="embedding",
            num_results=3,
            return_fields=["question", "answer", "category"],
        )
        results = index.query(query)
        print(f"\n=== Query: {q!r} ===")
        for i, doc in enumerate(results, start=1):
            score = doc.get("vector_distance", "n/a")
            print(f"[{i}] dist={score}  category={doc.get('category')}")
            print(f"    Q: {doc['question']}")

if __name__ == "__main__":
    main()
