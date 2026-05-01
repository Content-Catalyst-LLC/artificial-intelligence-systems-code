"""
Create advanced Jupyter notebooks for Artificial Intelligence in Environmental Monitoring.
"""

from pathlib import Path
import json

ARTICLE_DIR = Path(__file__).resolve().parent
NOTEBOOK_DIR = ARTICLE_DIR / "notebooks"
NOTEBOOK_DIR.mkdir(exist_ok=True)


def markdown_cell(source: str) -> dict:
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": source.strip().splitlines(True),
    }


def code_cell(source: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source.strip().splitlines(True),
    }


def notebook(cells: list[dict]) -> dict:
    return {
        "cells": cells,
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


notebooks = {
    "01_environmental_sensor_fusion.ipynb": notebook(
        [
            markdown_cell("# Environmental Sensor Fusion"),
            code_cell(
                """
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)

df = pd.DataFrame({
    "zone_id": [f"Z{i:03d}" for i in range(30)],
    "pm25": rng.normal(14, 6, 30).clip(1),
    "water_turbidity": rng.normal(8, 4, 30).clip(0),
    "vegetation_index": rng.normal(0.55, 0.18, 30).clip(0, 1)
})

df["fused_stress_index"] = (
    0.4 * df["pm25"] / df["pm25"].max()
    + 0.3 * df["water_turbidity"] / df["water_turbidity"].max()
    + 0.3 * (1 - df["vegetation_index"])
)

df.head()
                """
            ),
        ]
    ),
    "02_remote_sensing_classification.ipynb": notebook(
        [
            markdown_cell("# Remote Sensing Classification Sketch"),
            code_cell(
                """
import numpy as np
import pandas as pd

rng = np.random.default_rng(7)

pixels = pd.DataFrame({
    "red": rng.uniform(0.05, 0.40, 1000),
    "nir": rng.uniform(0.10, 0.80, 1000)
})

pixels["ndvi"] = (pixels["nir"] - pixels["red"]) / (pixels["nir"] + pixels["red"])
pixels["class"] = np.where(pixels["ndvi"] > 0.45, "vegetated", "non_vegetated")

pixels["class"].value_counts()
                """
            ),
        ]
    ),
    "03_anomaly_detection_early_warning.ipynb": notebook(
        [
            markdown_cell("# Anomaly Detection and Early Warning"),
            code_cell(
                """
import numpy as np
import pandas as pd

rng = np.random.default_rng(11)

time = np.arange(1, 121)
series = 10 + np.sin(time / 9) + rng.normal(0, 0.25, len(time))
series[80:88] += 3.5

z_score = np.abs((series - series.mean()) / series.std())

alerts = pd.DataFrame({
    "time": time,
    "value": series,
    "anomaly_score": z_score,
    "alert": z_score > 2.5
})

alerts[alerts["alert"]].head()
                """
            ),
        ]
    ),
    "04_environmental_governance_register.ipynb": notebook(
        [
            markdown_cell("# Environmental AI Governance Register"),
            code_cell(
                """
import pandas as pd

register = pd.DataFrame({
    "governance_artifact": [
        "sensor_inventory",
        "remote_sensing_product_record",
        "model_validation_report",
        "uncertainty_review",
        "environmental_justice_review",
        "alert_escalation_protocol"
    ],
    "status": [
        "complete",
        "complete",
        "in_review",
        "planned",
        "in_review",
        "complete"
    ],
    "owner": [
        "Monitoring Team",
        "Earth Observation Team",
        "ML Validation",
        "Science Review",
        "Public Accountability",
        "Emergency Response"
    ]
})

register
                """
            ),
        ]
    ),
}

for filename, nb in notebooks.items():
    path = NOTEBOOK_DIR / filename
    path.write_text(json.dumps(nb, indent=2))
    print(f"Created {path}")
