#!/usr/bin/env python3
"""
Create advanced Jupyter notebooks for:
Natural Language Processing and Computational Language Systems
"""

from __future__ import annotations

import json
from pathlib import Path
from textwrap import dedent


NOTEBOOK_DIR = Path(".")


def md(text: str) -> dict:
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": dedent(text).strip().splitlines(keepends=True),
    }


def code(text: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": dedent(text).strip().splitlines(keepends=True),
    }


def notebook(title: str, cells: list[dict]) -> dict:
    return {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [f"# {title}\n"],
            },
            *cells,
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "name": "python",
                "version": "3.x",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def write(path: Path, title: str, cells: list[dict]) -> None:
    path.write_text(json.dumps(notebook(title, cells), indent=2), encoding="utf-8")
    print(f"created {path}")


write(
    NOTEBOOK_DIR / "01_tokenization_and_ngram_language_model_lab.ipynb",
    "Tokenization and N-Gram Language Model Lab",
    [
        md("""
        ## Purpose

        This lab introduces tokenization and simple n-gram language modeling.

        Learning goals:

        - Convert text into tokens.
        - Count unigrams and bigrams.
        - Estimate simple conditional probabilities.
        - Understand why modern language modeling begins with sequence probability.
        """),
        code("""
        from collections import Counter
        import re
        import pandas as pd

        corpus = [
            "language models estimate probabilities over token sequences",
            "language systems transform tokens into contextual representations",
            "retrieval systems can ground language generation",
            "evaluation matters because fluent text is not always true",
        ]

        def tokenize(text):
            return re.findall(r"[a-z]+", text.lower())

        tokenized = [tokenize(text) for text in corpus]

        unigrams = Counter()
        bigrams = Counter()

        for tokens in tokenized:
            unigrams.update(tokens)
            bigrams.update(zip(tokens[:-1], tokens[1:]))

        rows = []

        for (left, right), count in bigrams.items():
            rows.append({
                "left_token": left,
                "right_token": right,
                "bigram_count": count,
                "conditional_probability": count / unigrams[left],
            })

        bigram_table = pd.DataFrame(rows).sort_values("conditional_probability", ascending=False)
        bigram_table
        """),
        md("""
        ## Interpretation

        N-gram models are limited, but they expose the basic idea of language modeling: estimate the probability of a token from context.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "02_embeddings_similarity_and_retrieval_lab.ipynb",
    "Embeddings, Similarity, and Retrieval Lab",
    [
        md("""
        ## Purpose

        This lab demonstrates the geometry behind embedding-based retrieval.

        Retrieval-augmented language systems depend on representing queries and documents in comparable vector spaces.
        """),
        code("""
        import numpy as np
        import pandas as pd
        from sklearn.metrics.pairwise import cosine_similarity

        rng = np.random.default_rng(42)

        documents = [
            "Transformers use attention to build contextual representations.",
            "Retrieval can ground generation in external documents.",
            "Hallucination occurs when fluent output is unsupported.",
            "Tokenization changes how language is represented.",
            "Evaluation should include domain and subgroup diagnostics.",
        ]

        def normalize(matrix):
            return matrix / np.maximum(np.linalg.norm(matrix, axis=1, keepdims=True), 1e-12)

        query_embedding = normalize(rng.normal(size=(1, 128)))
        document_embeddings = normalize(rng.normal(size=(len(documents), 128)))

        similarities = cosine_similarity(query_embedding, document_embeddings).ravel()

        retrieval_table = pd.DataFrame({
            "document": documents,
            "cosine_similarity": similarities,
        }).sort_values("cosine_similarity", ascending=False)

        retrieval_table
        """),
        md("""
        ## Governance Extension

        Similarity is not truth. A retrieval system should document source quality, chunking, ranking behavior, freshness, and whether the generated answer accurately represents the retrieved material.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "03_attention_and_contextual_representation_lab.ipynb",
    "Attention and Contextual Representation Lab",
    [
        md("""
        ## Purpose

        This lab demonstrates attention as relational computation.

        Attention weights describe how strongly tokens relate to one another inside a context.
        """),
        code("""
        import numpy as np
        import pandas as pd

        rng = np.random.default_rng(42)

        tokens = ["language", "models", "need", "grounding"]

        d_model = 8
        embeddings = rng.normal(size=(len(tokens), d_model))

        Q = embeddings
        K = embeddings
        V = embeddings

        scores = Q @ K.T / np.sqrt(d_model)

        def softmax(matrix):
            shifted = matrix - matrix.max(axis=1, keepdims=True)
            exp = np.exp(shifted)
            return exp / exp.sum(axis=1, keepdims=True)

        attention_weights = softmax(scores)

        pd.DataFrame(attention_weights, index=tokens, columns=tokens)
        """),
        code("""
        contextual_representations = attention_weights @ V

        pd.DataFrame(
            contextual_representations,
            index=tokens,
            columns=[f"dim_{i}" for i in range(d_model)]
        )
        """),
        md("""
        ## Interpretation

        This toy example does not train a transformer, but it shows the core mechanism: tokens update their representations by attending to other tokens.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "04_nlp_evaluation_hallucination_and_governance_lab.ipynb",
    "NLP Evaluation, Hallucination, and Governance Lab",
    [
        md("""
        ## Purpose

        This lab simulates evaluation records for an NLP system.

        The central point: language systems require evaluation beyond fluency.
        """),
        code("""
        import numpy as np
        import pandas as pd

        rng = np.random.default_rng(42)
        n = 1200

        data = pd.DataFrame({
            "document_domain": rng.choice(["general", "technical", "legal"], size=n, p=[0.45, 0.35, 0.20]),
            "language_variety": rng.choice(["standard", "specialized", "informal"], size=n),
            "requires_citation": rng.choice([True, False], size=n, p=[0.60, 0.40]),
        })

        domain_risk = data["document_domain"].map({
            "general": 0.06,
            "technical": 0.12,
            "legal": 0.18,
        })

        variety_risk = data["language_variety"].map({
            "standard": 1.00,
            "specialized": 1.25,
            "informal": 1.10,
        })

        citation_risk = np.where(data["requires_citation"], 1.30, 1.00)

        hallucination_probability = np.minimum(domain_risk * variety_risk * citation_risk, 0.90)

        data["unsupported_claim"] = rng.binomial(1, hallucination_probability).astype(bool)

        summary = (
            data
            .groupby(["document_domain", "language_variety"], as_index=False)
            .agg(
                sample_size=("unsupported_claim", "size"),
                unsupported_claim_rate=("unsupported_claim", "mean"),
            )
        )

        summary
        """),
        code("""
        summary.to_csv("../outputs/notebook_nlp_hallucination_diagnostics.csv", index=False)
        summary
        """),
        md("""
        ## Governance Questions

        - Which domains have the highest unsupported-claim rate?
        - Are citations required for high-risk domains?
        - Does the system distinguish retrieved evidence from generated prose?
        - Is there human review for consequential use?
        - How are errors logged and corrected?
        """),
    ],
)
