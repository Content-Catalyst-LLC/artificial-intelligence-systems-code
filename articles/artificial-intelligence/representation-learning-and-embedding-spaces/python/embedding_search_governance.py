"""
Representation Learning and Embedding Spaces

Python workflow:
- lightweight hashed embeddings
- cosine similarity
- semantic retrieval
- retrieval scoring
- governance summary generation
"""

from __future__ import annotations

from pathlib import Path
import hashlib
import re

import numpy as np
import pandas as pd


ARTICLE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ARTICLE_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

EMBEDDING_DIM = 128


DOCUMENTS = [
    {
        "doc_id": "D001",
        "title": "AI Safety and System Reliability",
        "category": "AI Systems",
        "authority_score": 0.92,
        "text": "AI safety depends on reliability, monitoring, evaluation, incident response, and lifecycle assurance.",
    },
    {
        "doc_id": "D002",
        "title": "Data Governance and Provenance",
        "category": "AI Systems",
        "authority_score": 0.89,
        "text": "Data lineage, metadata, provenance, audit trails, and stewardship support trustworthy AI systems.",
    },
    {
        "doc_id": "D003",
        "title": "Environmental Monitoring",
        "category": "Sustainability",
        "authority_score": 0.86,
        "text": "Environmental monitoring uses sensors, satellite data, uncertainty, and governance to track ecological change.",
    },
    {
        "doc_id": "D004",
        "title": "Generative AI and Synthetic Content",
        "category": "AI Systems",
        "authority_score": 0.84,
        "text": "Generative AI systems produce synthetic content and require provenance, disclosure, review, and governance.",
    },
    {
        "doc_id": "D005",
        "title": "Vector Search and Semantic Retrieval",
        "category": "Knowledge Systems",
        "authority_score": 0.88,
        "text": "Embedding spaces allow semantic search, nearest-neighbor retrieval, vector databases, and relevance ranking.",
    },
    {
        "doc_id": "D006",
        "title": "Infrastructure and Smart Networks",
        "category": "Infrastructure",
        "authority_score": 0.82,
        "text": "Smart infrastructure uses sensors, prediction, optimization, networks, and monitoring to improve resilience.",
    },
]


def tokenize(text: str) -> list[str]:
    """Tokenize text into simple lowercase word units."""
    return re.findall(r"[a-zA-Z][a-zA-Z0-9_-]*", text.lower())


def stable_hash(token: str) -> int:
    """Create a stable integer hash for a token."""
    digest = hashlib.sha256(token.encode("utf-8")).hexdigest()
    return int(digest[:12], 16)


def hashed_embedding(text: str, dim: int = EMBEDDING_DIM) -> np.ndarray:
    """Create a simple normalized hashed bag-of-words embedding."""
    vector = np.zeros(dim, dtype=float)

    for token in tokenize(text):
        index = stable_hash(token) % dim
        sign = 1 if stable_hash(token + "_sign") % 2 == 0 else -1
        vector[index] += sign

    norm = np.linalg.norm(vector)

    if norm == 0:
        return vector

    return vector / norm


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Compute cosine similarity for normalized or unnormalized vectors."""
    denominator = np.linalg.norm(a) * np.linalg.norm(b)

    if denominator == 0:
        return 0.0

    return float(np.dot(a, b) / denominator)


def build_embedding_index(documents: list[dict]) -> pd.DataFrame:
    """Embed each document and return a searchable table."""
    rows = []

    for document in documents:
        embedding = hashed_embedding(document["title"] + " " + document["text"])

        rows.append(
            {
                **document,
                "embedding": embedding,
                "embedding_norm": float(np.linalg.norm(embedding)),
            }
        )

    return pd.DataFrame(rows)


def search(index: pd.DataFrame, query: str, top_k: int = 4) -> pd.DataFrame:
    """Search documents using cosine similarity."""
    query_embedding = hashed_embedding(query)

    results = index.copy()
    results["similarity"] = results["embedding"].apply(
        lambda embedding: cosine_similarity(query_embedding, embedding)
    )

    results["retrieval_score"] = (
        0.75 * results["similarity"]
        + 0.25 * results["authority_score"]
    )

    results["review_flag"] = (
        (results["similarity"] < 0.10)
        | (results["embedding_norm"] < 0.95)
    )

    columns = [
        "doc_id",
        "title",
        "category",
        "authority_score",
        "similarity",
        "retrieval_score",
        "review_flag",
    ]

    return results.sort_values("retrieval_score", ascending=False)[columns].head(top_k)


def create_governance_summary(index: pd.DataFrame, queries: list[str]) -> pd.DataFrame:
    """Create governance diagnostics for representative queries."""
    rows = []

    for query in queries:
        results = search(index, query, top_k=3)

        rows.append(
            {
                "query": query,
                "top_result": results.iloc[0]["title"],
                "top_similarity": results.iloc[0]["similarity"],
                "mean_top3_similarity": results["similarity"].mean(),
                "review_flags": int(results["review_flag"].sum()),
            }
        )

    return pd.DataFrame(rows)


def main() -> None:
    """Run embedding search and governance review."""
    index = build_embedding_index(DOCUMENTS)

    queries = [
        "How do AI systems monitor reliability and incidents?",
        "What supports data lineage and provenance?",
        "How does semantic retrieval use vector embeddings?",
        "How should synthetic content be governed?",
    ]

    all_results = []

    for query in queries:
        results = search(index, query, top_k=4)
        results.insert(0, "query", query)
        all_results.append(results)

    retrieval_results = pd.concat(all_results, ignore_index=True)
    governance_summary = create_governance_summary(index, queries)

    export_index = index.drop(columns=["embedding"])

    export_index.to_csv(OUTPUT_DIR / "python_embedding_index_metadata.csv", index=False)
    retrieval_results.to_csv(OUTPUT_DIR / "python_embedding_search_results.csv", index=False)
    governance_summary.to_csv(OUTPUT_DIR / "python_embedding_governance_summary.csv", index=False)

    memo = f"""# Embedding Search Governance Memo

Documents indexed: {len(index)}
Queries reviewed: {len(queries)}
Mean top-result similarity: {governance_summary["top_similarity"].mean():.4f}
Queries with review flags: {int((governance_summary["review_flags"] > 0).sum())}

Interpretation:
- Embedding-based retrieval should be evaluated with representative queries.
- Similarity should be combined with metadata and authority signals where appropriate.
- Low-similarity retrieval should trigger review rather than automatic trust.
- Embedding model version, chunking, metadata, and vector index status should be documented.
"""

    (OUTPUT_DIR / "python_embedding_governance_memo.md").write_text(memo)

    print(retrieval_results)
    print(governance_summary)
    print(memo)


if __name__ == "__main__":
    main()
