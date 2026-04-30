"""
Natural Language Processing and Computational Language Systems Mini-Workflow

This script demonstrates:
- simple tokenization
- bigram language statistics
- synthetic embedding similarity
- retrieval-style ranking

It is educational and does not require private text data.
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path
import re

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


OUTPUT_DIR = Path("../outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

RANDOM_SEED = 42
rng = np.random.default_rng(RANDOM_SEED)


DOCUMENTS = [
    "Language models estimate probabilities over token sequences.",
    "Transformers use attention to build contextual representations.",
    "Retrieval can ground generation in external documents.",
    "Evaluation is necessary because fluent language is not always true.",
]


def tokenize(text: str) -> list[str]:
    """Simple lowercase tokenizer for demonstration."""
    return re.findall(r"[a-z]+", text.lower())


def normalized_random_embeddings(n_items: int, dimension: int) -> np.ndarray:
    """Create normalized synthetic embeddings."""
    embeddings = rng.normal(size=(n_items, dimension))
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    return embeddings / np.maximum(norms, 1e-12)


def main() -> None:
    tokenized = [tokenize(doc) for doc in DOCUMENTS]

    bigrams = Counter()

    for tokens in tokenized:
        for left, right in zip(tokens[:-1], tokens[1:]):
            bigrams[(left, right)] += 1

    bigram_table = pd.DataFrame(
        [
            {"left_token": left, "right_token": right, "count": count}
            for (left, right), count in bigrams.items()
        ]
    ).sort_values("count", ascending=False)

    query_embedding = normalized_random_embeddings(1, 128)
    document_embeddings = normalized_random_embeddings(len(DOCUMENTS), 128)

    similarities = cosine_similarity(query_embedding, document_embeddings).ravel()

    retrieval_table = pd.DataFrame(
        {
            "document": DOCUMENTS,
            "cosine_similarity": similarities,
        }
    ).sort_values("cosine_similarity", ascending=False)

    bigram_table.to_csv(OUTPUT_DIR / "bigram_counts.csv", index=False)
    retrieval_table.to_csv(OUTPUT_DIR / "synthetic_retrieval_similarity.csv", index=False)

    print("Bigram counts:")
    print(bigram_table.head())
    print()
    print("Synthetic retrieval ranking:")
    print(retrieval_table)


if __name__ == "__main__":
    main()
