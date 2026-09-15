# RediCorp Department of Repeated Questions (DoRQ)

A small semantic FAQ search demo built with **Redis 8**, **RedisVL**, and a local **sentence-transformers** embedding model — no LLM involved. Ask a question in your own words and get back the closest matching FAQ, ranked by vector similarity instead of exact keyword matching.

This is the advanced RedisVL lab that follows the introductory "RediCafé" coffee-shop Redis lab.

## How it works

1. `faq_data.py` holds five hardcoded FAQ entries (question, answer, category) as the knowledge base.
2. `faq_index.py` defines the Redis index schema: `question`/`answer` as text fields, `category` as a tag field, and `embedding` as a 384-dimension vector field (HNSW algorithm, cosine distance).
3. `ingest_faqs.py` embeds each FAQ with the `all-MiniLM-L6-v2` sentence-transformer model, creates the index in Redis, and writes each FAQ as a hash (`faq:1` … `faq:5`) with its embedding packed as a binary vector.
4. `query_faqs.py` embeds a typed question the same way and runs a KNN vector search against the index, returning the 3 closest FAQs.
5. `sample_queries.py` is a non-interactive version of the same query flow, useful for quickly testing a batch of questions and seeing each match's `vector_distance`.

## Prerequisites

- Python 3.9+
- A Redis instance with vector search support (Redis 8+, either via Docker or Redis Cloud)

## Setup

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill in your real Redis connection string:

```
REDIS_URL=redis://default:<password>@<host>:<port>
```

`.env` is gitignored — never commit real credentials.

## Usage

Build the index and load the FAQ data (safe to re-run; it recreates the index each time):

```bash
python ingest_faqs.py
```

Ask questions interactively:

```bash
python query_faqs.py
```

Or run a fixed batch of test questions and see the vector distances behind each match:

```bash
python sample_queries.py
```

## Project structure

```
.
├── faq_data.py                        # The FAQ knowledge base
├── faq_index.py                       # RedisVL index schema + connection helper
├── ingest_faqs.py                     # Embeds FAQs and loads them into Redis
├── query_faqs.py                      # Interactive semantic search over the FAQs
├── sample_queries.py                  # Non-interactive test queries with distances
├── requirements.txt
├── .env.example
└── Advanced Lab - RediCorp DoRQ/      # Lab write-up: markdown report, PDF, and screenshots
```

## Lab write-up

The full deliverables write-up — how the index was configured, example queries with results, productionization notes, limitations, and a proposed next iteration — is in [`Advanced Lab - RediCorp DoRQ/lab_report.md`](<Advanced Lab - RediCorp DoRQ/lab_report.md>), with a formatted PDF version alongside it.
