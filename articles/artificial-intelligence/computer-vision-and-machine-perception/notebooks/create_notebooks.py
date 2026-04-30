#!/usr/bin/env python3
"""
Create advanced Jupyter notebooks for:
Computer Vision and Machine Perception
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
    NOTEBOOK_DIR / "01_image_representation_and_convolution_lab.ipynb",
    "Image Representation and Convolution Lab",
    [
        md("""
        ## Purpose

        This lab shows how images become tensors and how convolutional filters extract local structure.

        Learning goals:

        - Create a synthetic image.
        - Apply Sobel-style convolution filters.
        - Interpret edge magnitude as a feature map.
        - Understand why convolution encodes local visual structure.
        """),
        code("""
        import numpy as np
        import matplotlib.pyplot as plt
        from scipy.signal import convolve2d

        def make_synthetic_image(size=64):
            image = np.zeros((size, size), dtype=float)
            image[18:46, 18:46] = 1.0

            rng = np.random.default_rng(42)
            image += 0.05 * rng.normal(size=image.shape)

            return np.clip(image, 0.0, 1.0)

        image = make_synthetic_image()

        plt.figure(figsize=(5, 5))
        plt.imshow(image, cmap="gray")
        plt.title("Synthetic Image")
        plt.axis("off")
        plt.show()
        """),
        code("""
        sobel_x = np.array([
            [-1, 0, 1],
            [-2, 0, 2],
            [-1, 0, 1],
        ])

        sobel_y = np.array([
            [-1, -2, -1],
            [0, 0, 0],
            [1, 2, 1],
        ])

        edge_x = convolve2d(image, sobel_x, mode="same", boundary="symm")
        edge_y = convolve2d(image, sobel_y, mode="same", boundary="symm")
        edge_magnitude = np.sqrt(edge_x ** 2 + edge_y ** 2)

        plt.figure(figsize=(5, 5))
        plt.imshow(edge_magnitude, cmap="gray")
        plt.title("Edge Magnitude")
        plt.axis("off")
        plt.show()
        """),
        md("""
        ## Interpretation

        The edge map is a feature representation. A CNN learns filters like this from data rather than using only hand-designed filters.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "02_feature_hierarchies_and_cnn_intuition_lab.ipynb",
    "Feature Hierarchies and CNN Intuition Lab",
    [
        md("""
        ## Purpose

        This lab builds intuition for visual feature hierarchies using synthetic filters.

        CNNs build increasingly abstract features from local patterns.
        """),
        code("""
        import numpy as np
        import pandas as pd

        layers = pd.DataFrame([
            {"layer": "early", "typical_features": "edges, corners, simple gradients", "spatial_scale": "local"},
            {"layer": "middle", "typical_features": "textures, parts, repeated motifs", "spatial_scale": "regional"},
            {"layer": "deep", "typical_features": "objects, scenes, semantic patterns", "spatial_scale": "global"},
        ])

        layers
        """),
        code("""
        def parameter_count(kernel_height, kernel_width, in_channels, out_channels):
            return kernel_height * kernel_width * in_channels * out_channels + out_channels

        comparison = pd.DataFrame([
            {
                "layer_type": "3x3 convolution",
                "parameters": parameter_count(3, 3, 64, 128),
            },
            {
                "layer_type": "fully connected over 32x32x64",
                "parameters": (32 * 32 * 64) * 128 + 128,
            },
        ])

        comparison
        """),
        md("""
        ## Interpretation

        Convolution reduces parameter count by reusing local filters across the image.

        This is one reason CNNs are efficient for visual data.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "03_iou_segmentation_and_structured_outputs_lab.ipynb",
    "IoU, Segmentation, and Structured Outputs Lab",
    [
        md("""
        ## Purpose

        This lab introduces structured visual outputs.

        Classification predicts one label. Segmentation predicts a label for each pixel.
        """),
        code("""
        import numpy as np
        import matplotlib.pyplot as plt
        import pandas as pd

        size = 64

        reference = np.zeros((size, size), dtype=bool)
        reference[18:46, 18:46] = True

        prediction = np.zeros((size, size), dtype=bool)
        prediction[20:48, 16:44] = True

        def iou(mask_a, mask_b):
            intersection = np.logical_and(mask_a, mask_b).sum()
            union = np.logical_or(mask_a, mask_b).sum()
            return intersection / max(union, 1)

        score = iou(reference, prediction)

        pd.DataFrame([{"intersection_over_union": score}])
        """),
        code("""
        plt.figure(figsize=(5, 5))
        plt.imshow(reference.astype(int) + prediction.astype(int), cmap="viridis")
        plt.title("Reference and Predicted Masks")
        plt.axis("off")
        plt.show()
        """),
        md("""
        ## Interpretation

        IoU measures overlap between predicted and reference regions.

        It is central to detection and segmentation evaluation.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "04_robustness_perturbation_and_error_diagnostics_lab.ipynb",
    "Robustness, Perturbation, and Error Diagnostics Lab",
    [
        md("""
        ## Purpose

        This lab simulates robustness and grouped diagnostics for computer vision systems.

        Aggregate accuracy can hide failures across lighting, camera, domain, or subgroup conditions.
        """),
        code("""
        import numpy as np
        import pandas as pd

        rng = np.random.default_rng(42)
        n = 1500

        data = pd.DataFrame({
            "image_group": rng.choice(["A", "B", "C"], size=n, p=[0.5, 0.3, 0.2]),
            "lighting_condition": rng.choice(["normal", "low_light", "harsh_light"], size=n),
            "target": rng.binomial(1, 0.4, size=n),
        })

        lighting_error = data["lighting_condition"].map({
            "normal": 0.08,
            "low_light": 0.18,
            "harsh_light": 0.14,
        })

        group_error = data["image_group"].map({
            "A": 1.00,
            "B": 1.20,
            "C": 1.35,
        })

        error_probability = np.minimum(lighting_error * group_error, 0.90)
        is_error = rng.binomial(1, error_probability)

        data["prediction"] = np.where(is_error == 1, 1 - data["target"], data["target"])
        data["error"] = data["prediction"] != data["target"]

        summary = (
            data
            .groupby(["image_group", "lighting_condition"], as_index=False)
            .agg(
                sample_size=("error", "size"),
                classification_error_rate=("error", "mean"),
            )
        )

        summary
        """),
        code("""
        summary.to_csv("../outputs/notebook_vision_error_diagnostics.csv", index=False)
        summary
        """),
        md("""
        ## Governance Extension

        Before deployment, ask:

        - Which conditions show the highest error?
        - Are those conditions common in deployment?
        - Are vulnerable groups or critical contexts affected?
        - Is human review available?
        - What monitoring will detect model degradation?
        """),
    ],
)
