#!/usr/bin/env python3
"""
Create advanced Jupyter notebooks for:
Data Quality, Bias, and Measurement in Machine Learning
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
            {"cell_type": "markdown", "metadata": {}, "source": [f"# {title}\n"]},
            *cells,
        ],
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.x"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def write(path: Path, title: str, cells: list[dict]) -> None:
    path.write_text(json.dumps(notebook(title, cells), indent=2), encoding="utf-8")
    print(f"created {path}")


setup_code = """
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)

n = 5000

data = pd.DataFrame({
    "unit_id": [f"unit_{i:05d}" for i in range(1, n + 1)],
    "group": rng.choice(["A", "B"], size=n, p=[0.82, 0.18]),
    "feature_signal": rng.normal(0, 1, size=n),
    "measurement_quality": rng.choice(
        ["high", "medium", "low"],
        size=n,
        p=[0.55, 0.30, 0.15],
    ),
})

data["measurement_error_sd"] = np.where(data["group"] == "B", 0.45, 0.20)

data["measured_feature"] = (
    data["feature_signal"]
    + rng.normal(0, data["measurement_error_sd"], size=n)
)

data.head()
"""

write(
    NOTEBOOK_DIR / "01_measurement_theory_construct_validity_and_proxy_variables_lab.ipynb",
    "Measurement Theory, Construct Validity, and Proxy Variables Lab",
    [
        md("""
        ## Purpose

        This lab shows how observed proxy measurements can differ from latent constructs.
        """),
        code(setup_code),
        code("""
measurement_summary = (
    data
    .groupby("group")
    .agg(
        units=("unit_id", "count"),
        mean_latent_signal=("feature_signal", "mean"),
        mean_observed_measurement=("measured_feature", "mean"),
        observed_measurement_sd=("measured_feature", "std"),
        measurement_error_sd=("measurement_error_sd", "mean"),
    )
    .reset_index()
)

measurement_summary
        """),
        md("""
        ## Interpretation

        Measurement quality may vary by group, making the same observed variable less reliable for some populations than others.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "02_missingness_label_noise_and_data_quality_diagnostics_lab.ipynb",
    "Missingness, Label Noise, and Data Quality Diagnostics Lab",
    [
        md("""
        ## Purpose

        This lab simulates missingness and noisy labels as data-quality failure modes.
        """),
        code(setup_code),
        code("""
logit = -0.10 + 1.20 * data["feature_signal"] + np.where(data["group"] == "B", -0.15, 0)
probability = 1 / (1 + np.exp(-logit))
data["true_label"] = rng.binomial(1, probability)

label_flip_probability = np.where(
    data["measurement_quality"] == "low",
    0.18,
    np.where(data["measurement_quality"] == "medium", 0.08, 0.03),
)

label_flip = rng.binomial(1, label_flip_probability)
data["observed_label"] = np.where(label_flip == 1, 1 - data["true_label"], data["true_label"])

missing_probability = np.where(data["group"] == "B", 0.20, 0.06)
data["measured_feature_missing"] = rng.binomial(1, missing_probability)

quality_summary = (
    data
    .groupby(["group", "measurement_quality"])
    .agg(
        units=("unit_id", "count"),
        missing_rate=("measured_feature_missing", "mean"),
        true_label_rate=("true_label", "mean"),
        observed_label_rate=("observed_label", "mean"),
    )
    .reset_index()
)

quality_summary
        """),
        md("""
        ## Interpretation

        Missingness and label noise can vary across groups and measurement-quality levels, creating downstream bias.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "03_representation_bias_fairness_metrics_and_subgroup_error_lab.ipynb",
    "Representation Bias, Fairness Metrics, and Subgroup Error Lab",
    [
        md("""
        ## Purpose

        This lab evaluates subgroup representation, prediction error, and statistical parity difference.
        """),
        code(setup_code),
        code("""
logit = -0.10 + 1.20 * data["feature_signal"] + np.where(data["group"] == "B", -0.15, 0)
probability = 1 / (1 + np.exp(-logit))
data["true_label"] = rng.binomial(1, probability)

missing_probability = np.where(data["group"] == "B", 0.20, 0.06)
data["measured_feature_missing"] = rng.binomial(1, missing_probability)
data.loc[data["measured_feature_missing"] == 1, "measured_feature"] = np.nan

imputed_feature = data["measured_feature"].fillna(data["measured_feature"].mean())
score = 1 / (1 + np.exp(-(-0.05 + 1.05 * imputed_feature)))

data["predicted_label"] = (score >= 0.50).astype(int)
data["prediction_error"] = (data["predicted_label"] != data["true_label"]).astype(int)

group_summary = (
    data
    .groupby("group")
    .agg(
        units=("unit_id", "count"),
        share=("unit_id", lambda x: len(x) / len(data)),
        positive_prediction_rate=("predicted_label", "mean"),
        error_rate=("prediction_error", "mean"),
        missing_rate=("measured_feature_missing", "mean"),
    )
    .reset_index()
)

rate_a = group_summary.loc[group_summary["group"] == "A", "positive_prediction_rate"].iloc[0]
rate_b = group_summary.loc[group_summary["group"] == "B", "positive_prediction_rate"].iloc[0]

statistical_parity_difference = rate_a - rate_b

group_summary, statistical_parity_difference
        """),
        md("""
        ## Interpretation

        Aggregate performance can hide subgroup differences in representation, missingness, positive prediction rates, and error.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "04_dataset_documentation_data_governance_and_bias_auditing_lab.ipynb",
    "Dataset Documentation, Data Governance, and Bias Auditing Lab",
    [
        md("""
        ## Purpose

        This lab frames data quality as a governance and documentation problem.
        """),
        code("""
import pandas as pd

documentation_review = pd.DataFrame([
    {
        "area": "construct_validity",
        "question": "Is the latent construct clearly defined?",
        "status": "partial",
        "owner": "Research / Domain Team",
    },
    {
        "area": "proxy_variable",
        "question": "Is the observed proxy appropriate for the construct?",
        "status": "partial",
        "owner": "Data Science",
    },
    {
        "area": "representation",
        "question": "Are underrepresented groups documented?",
        "status": "missing",
        "owner": "Data Steward",
    },
    {
        "area": "label_quality",
        "question": "Are label sources and annotation procedures documented?",
        "status": "partial",
        "owner": "ML Operations",
    },
    {
        "area": "appropriate_use",
        "question": "Are appropriate and inappropriate uses stated?",
        "status": "missing",
        "owner": "Governance",
    },
])

documentation_review.groupby("status").size().reset_index(name="count")
        """),
        md("""
        ## Interpretation

        Dataset documentation makes quality limits, proxy assumptions, representation gaps, and appropriate-use constraints auditable.
        """),
    ],
)
