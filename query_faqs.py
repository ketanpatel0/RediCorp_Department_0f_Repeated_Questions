from sentence_transformers import SentenceTransformer
from redisvl.query import VectorQuery
from faq_index import get_faq_index
def pretty_print_results(results):
    print("\nTop matches:")
    for i, doc in enumerate(results, start=1):
        print(f"\n[{i}] Question: {doc['question']}")
        print(f"   Category: {doc.get('category', 'n/a')}")
        print(f"   Answer: {doc['answer']}")
def main():
    index = get_faq_index()
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    while True:
        user_query = input("\nAsk RediCorp DoRQ a question (or type 'quit'):").strip()
        if user_query.lower() in ("quit", "exit"):
            break
        # 1) Embed the query locally (no LLM, just a sentence-transformer)
        q_vec = model.encode([user_query]).tolist()[0]
        # 2) Vector search against Redis
        query = VectorQuery(
            vector=q_vec,
            vector_field_name="embedding",
            num_results=3,
            return_fields=["question", "answer", "category"]
        )
        results = index.query(query)
        # 3) Display results
        pretty_print_results(results)
if __name__ == "__main__":
    main()