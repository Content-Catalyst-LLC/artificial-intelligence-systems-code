#!/usr/bin/env python3
"""
Create advanced Jupyter notebooks for:
Speech Recognition and Multimodal AI Systems
"""

from __future__ import annotations

import json
from pathlib import Path
from textwrap import dedent


NOTEBOOK_DIR = Path(".")
OUTPUT_DIR = Path("../outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


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
    NOTEBOOK_DIR / "01_audio_signal_and_spectrogram_lab.ipynb",
    "Audio Signal and Spectrogram Lab",
    [
        md("""
        ## Purpose

        This lab shows how a continuous audio signal becomes a time-frequency representation.

        Learning goals:

        - Generate a synthetic waveform.
        - Compute a spectrogram.
        - Interpret time-frequency structure.
        - Understand why speech recognition begins with representation.
        """),
        code("""
        import numpy as np
        import pandas as pd
        import matplotlib.pyplot as plt
        from scipy.signal import spectrogram

        sample_rate_hz = 16_000
        duration_seconds = 1.0

        time = np.linspace(
            0,
            duration_seconds,
            int(sample_rate_hz * duration_seconds),
            endpoint=False,
        )

        rng = np.random.default_rng(42)

        audio = (
            0.6 * np.sin(2 * np.pi * 220 * time)
            + 0.3 * np.sin(2 * np.pi * 440 * time)
            + 0.02 * rng.normal(size=len(time))
        )

        plt.figure(figsize=(10, 4))
        plt.plot(time[:1000], audio[:1000])
        plt.title("Synthetic Audio Waveform")
        plt.xlabel("Time (seconds)")
        plt.ylabel("Amplitude")
        plt.show()
        """),
        code("""
        frequencies, times, power = spectrogram(
            audio,
            fs=sample_rate_hz,
            nperseg=512,
            noverlap=256,
        )

        plt.figure(figsize=(10, 5))
        plt.pcolormesh(times, frequencies, 10 * np.log10(power + 1e-12), shading="auto")
        plt.title("Synthetic Audio Spectrogram")
        plt.xlabel("Time (seconds)")
        plt.ylabel("Frequency (Hz)")
        plt.ylim(0, 2000)
        plt.colorbar(label="Power (dB)")
        plt.show()

        summary = pd.DataFrame([{
            "sample_rate_hz": sample_rate_hz,
            "duration_seconds": duration_seconds,
            "frequency_bins": len(frequencies),
            "time_bins": len(times),
            "spectrogram_shape": str(power.shape),
        }])

        summary
        """),
        md("""
        ## Interpretation

        A spectrogram turns sound into a structured representation that models can process.

        In real speech recognition, this representation may be a raw waveform, log-Mel spectrogram, MFCCs, or a learned latent representation.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "02_ctc_alignment_intuition_lab.ipynb",
    "CTC Alignment Intuition Lab",
    [
        md("""
        ## Purpose

        This lab gives a toy explanation of CTC alignment.

        CTC is useful when the transcript is known but the frame-level alignment between audio and tokens is unknown.
        """),
        code("""
        from itertools import product

        tokens = ["_", "a", "b"]
        target = "ab"
        time_steps = 4

        def collapse(path):
            collapsed = []
            previous = None

            for symbol in path:
                if symbol != previous:
                    collapsed.append(symbol)
                previous = symbol

            return "".join(symbol for symbol in collapsed if symbol != "_")

        valid_paths = []

        for path in product(tokens, repeat=time_steps):
            if collapse(path) == target:
                valid_paths.append(path)

        print("Number of valid paths:", len(valid_paths))
        valid_paths[:10]
        """),
        md("""
        ## Interpretation

        CTC sums over possible paths that collapse to the same output sequence.

        The model does not need to know exactly which audio frame corresponds to which output character.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "03_multimodal_embedding_similarity_lab.ipynb",
    "Multimodal Embedding Similarity Lab",
    [
        md("""
        ## Purpose

        This lab demonstrates the basic geometry behind multimodal retrieval.

        Audio, text, image, or video encoders can map different inputs into embedding vectors. Similarity search can then retrieve related items across modalities.
        """),
        code("""
        import numpy as np
        import pandas as pd
        from sklearn.metrics.pairwise import cosine_similarity

        rng = np.random.default_rng(42)

        def normalize(matrix):
            return matrix / np.maximum(np.linalg.norm(matrix, axis=1, keepdims=True), 1e-12)

        audio_embeddings = normalize(rng.normal(size=(3, 128)))
        text_embeddings = normalize(rng.normal(size=(6, 128)))

        similarity = cosine_similarity(audio_embeddings, text_embeddings)

        similarity_table = pd.DataFrame(
            similarity,
            index=[f"audio_{i}" for i in range(audio_embeddings.shape[0])],
            columns=[f"text_{j}" for j in range(text_embeddings.shape[0])],
        )

        similarity_table
        """),
        code("""
        top_matches = []

        for audio_id, row in similarity_table.iterrows():
            best_text = row.idxmax()
            top_matches.append({
                "audio_id": audio_id,
                "best_text_match": best_text,
                "cosine_similarity": row.max(),
            })

        pd.DataFrame(top_matches)
        """),
        md("""
        ## Governance Extension

        Similarity is not meaning. A retrieval system should document:

        - what data trained the encoders;
        - whether modalities are equally represented;
        - how retrieval errors are evaluated;
        - whether users can contest or correct matches;
        - whether embeddings leak sensitive information.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "04_speech_error_diagnostics_and_governance_lab.ipynb",
    "Speech Error Diagnostics and Governance Lab",
    [
        md("""
        ## Purpose

        This lab simulates speech recognition error diagnostics.

        The central point: aggregate WER can hide uneven error burdens across groups and conditions.
        """),
        code("""
        import numpy as np
        import pandas as pd

        rng = np.random.default_rng(42)
        n = 1000

        data = pd.DataFrame({
            "speaker_group": rng.choice(["A", "B", "C"], size=n, p=[0.5, 0.3, 0.2]),
            "noise_condition": rng.choice(["clean", "moderate_noise", "high_noise"], size=n),
            "reference_words": rng.integers(5, 31, size=n),
        })

        noise_multiplier = data["noise_condition"].map({
            "clean": 0.05,
            "moderate_noise": 0.12,
            "high_noise": 0.22,
        })

        group_multiplier = data["speaker_group"].map({
            "A": 1.00,
            "B": 1.15,
            "C": 1.35,
        })

        expected_errors = data["reference_words"] * noise_multiplier * group_multiplier

        data["substitutions"] = rng.poisson(expected_errors * 0.45)
        data["deletions"] = rng.poisson(expected_errors * 0.35)
        data["insertions"] = rng.poisson(expected_errors * 0.20)

        data["wer"] = (
            data["substitutions"] +
            data["deletions"] +
            data["insertions"]
        ) / data["reference_words"]

        summary = (
            data
            .groupby(["speaker_group", "noise_condition"], as_index=False)
            .agg(
                sample_size=("wer", "size"),
                mean_wer=("wer", "mean"),
                median_wer=("wer", "median"),
            )
        )

        summary
        """),
        code("""
        summary.to_csv("../outputs/notebook_speech_error_diagnostics.csv", index=False)
        summary
        """),
        md("""
        ## Review Questions

        - Which group-condition pair has the highest WER?
        - Is the difference practically meaningful?
        - Would this system be acceptable for accessibility use?
        - What additional evaluation data would be required?
        - Who should review deployment?
        """),
    ],
)
