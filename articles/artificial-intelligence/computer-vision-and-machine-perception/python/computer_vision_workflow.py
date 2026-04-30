"""
Computer Vision and Machine Perception Mini-Workflow

This script demonstrates:
- synthetic image generation
- convolution with edge filters
- basic visual diagnostics
- simple IoU calculation

It is educational and does not require private image data.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from scipy.signal import convolve2d


OUTPUT_DIR = Path("../outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def make_synthetic_image(size: int = 64) -> np.ndarray:
    """Create a simple synthetic image with a bright square."""
    image = np.zeros((size, size), dtype=float)
    image[18:46, 18:46] = 1.0

    rng = np.random.default_rng(42)
    image += 0.05 * rng.normal(size=image.shape)

    return np.clip(image, 0.0, 1.0)


def intersection_over_union(mask_a: np.ndarray, mask_b: np.ndarray) -> float:
    """Compute intersection over union for binary masks."""
    a = mask_a.astype(bool)
    b = mask_b.astype(bool)

    intersection = np.logical_and(a, b).sum()
    union = np.logical_or(a, b).sum()

    return float(intersection / max(union, 1))


def main() -> None:
    image = make_synthetic_image()

    sobel_x = np.array(
        [
            [-1, 0, 1],
            [-2, 0, 2],
            [-1, 0, 1],
        ]
    )

    sobel_y = np.array(
        [
            [-1, -2, -1],
            [0, 0, 0],
            [1, 2, 1],
        ]
    )

    edge_x = convolve2d(image, sobel_x, mode="same", boundary="symm")
    edge_y = convolve2d(image, sobel_y, mode="same", boundary="symm")
    edge_magnitude = np.sqrt(edge_x**2 + edge_y**2)

    reference_mask = np.zeros_like(image, dtype=bool)
    reference_mask[18:46, 18:46] = True

    predicted_mask = image > 0.50

    iou = intersection_over_union(reference_mask, predicted_mask)

    summary = pd.DataFrame(
        [
            {
                "image_height": image.shape[0],
                "image_width": image.shape[1],
                "mean_intensity": float(image.mean()),
                "max_edge_magnitude": float(edge_magnitude.max()),
                "mean_edge_magnitude": float(edge_magnitude.mean()),
                "synthetic_mask_iou": iou,
            }
        ]
    )

    summary.to_csv(OUTPUT_DIR / "vision_workflow_summary.csv", index=False)

    np.save(OUTPUT_DIR / "synthetic_image.npy", image)
    np.save(OUTPUT_DIR / "edge_magnitude.npy", edge_magnitude)

    print(summary)


if __name__ == "__main__":
    main()
