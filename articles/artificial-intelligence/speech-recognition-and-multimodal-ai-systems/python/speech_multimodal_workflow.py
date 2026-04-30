"""
Speech Recognition and Multimodal AI Mini-Workflow

This script demonstrates:
- synthetic audio generation
- spectrogram construction
- cosine similarity for multimodal embeddings
- basic output export

It is educational and does not require private audio data.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from scipy.signal import spectrogram
from sklearn.metrics.pairwise import cosine_similarity


OUTPUT_DIR = Path("../outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

RANDOM_SEED = 42
rng = np.random.default_rng(RANDOM_SEED)


def generate_synthetic_audio(
    sample_rate_hz: int = 16_000,
    duration_seconds: float = 1.0,
) -> tuple[np.ndarray, np.ndarray]:
    """Generate a simple synthetic audio signal."""
    time = np.linspace(
        0,
        duration_seconds,
        int(sample_rate_hz * duration_seconds),
        endpoint=False,
    )

    audio = (
        0.6 * np.sin(2 * np.pi * 220 * time)
        + 0.3 * np.sin(2 * np.pi * 440 * time)
        + 0.02 * rng.normal(size=len(time))
    )

    return time, audio


def normalized_random_embeddings(n_items: int, dimension: int) -> np.ndarray:
    """Create normalized synthetic embeddings."""
    embeddings = rng.normal(size=(n_items, dimension))
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    return embeddings / np.maximum(norms, 1e-12)


def main() -> None:
    sample_rate_hz = 16_000
    time, audio = generate_synthetic_audio(sample_rate_hz=sample_rate_hz)

    frequencies, times, power = spectrogram(
        audio,
        fs=sample_rate_hz,
        nperseg=512,
        noverlap=256,
    )

    spectrogram_summary = {
        "sample_rate_hz": sample_rate_hz,
        "duration_seconds": float(time[-1]),
        "n_audio_samples": int(len(audio)),
        "n_frequency_bins": int(len(frequencies)),
        "n_time_bins": int(len(times)),
        "spectrogram_shape": list(power.shape),
    }

    audio_embedding = normalized_random_embeddings(1, 128)
    text_embeddings = normalized_random_embeddings(5, 128)

    similarities = cosine_similarity(audio_embedding, text_embeddings).ravel()
    best_match = int(np.argmax(similarities))

    similarity_table = pd.DataFrame(
        {
            "candidate_id": [f"text_candidate_{i}" for i in range(len(similarities))],
            "cosine_similarity": similarities,
        }
    ).sort_values("cosine_similarity", ascending=False)

    similarity_table.to_csv(OUTPUT_DIR / "multimodal_embedding_similarity.csv", index=False)

    pd.DataFrame([spectrogram_summary]).to_csv(
        OUTPUT_DIR / "spectrogram_summary.csv",
        index=False,
    )

    print("Spectrogram summary:")
    print(spectrogram_summary)
    print()
    print("Best matching text candidate:", best_match)
    print(similarity_table)


if __name__ == "__main__":
    main()
