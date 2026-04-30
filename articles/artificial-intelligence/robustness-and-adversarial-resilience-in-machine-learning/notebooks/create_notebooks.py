#!/usr/bin/env python3
"""
Create advanced Jupyter notebooks for:
Robustness and Adversarial Resilience in Machine Learning
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


base_setup = """
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)

n = 2000
d = 12

X = rng.normal(size=(n, d))
true_weights = rng.normal(size=d)
y = ((X @ true_weights) > 0).astype(int)
model_weights = true_weights + rng.normal(scale=0.25, size=d)

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def predict(features):
    return (sigmoid(features @ model_weights) >= 0.5).astype(int)

def accuracy(features, labels):
    return float(np.mean(predict(features) == labels))

def adversarial_perturb(features, labels, epsilon):
    direction = np.where(labels[:, None] == 1, -1.0, 1.0)
    return features + epsilon * direction * np.sign(model_weights)

accuracy(X, y)
"""

write(
    NOTEBOOK_DIR / "01_clean_accuracy_robust_accuracy_and_perturbation_budget_lab.ipynb",
    "Clean Accuracy, Robust Accuracy, and Perturbation Budget Lab",
    [
        md("""
        ## Purpose

        This lab compares clean accuracy and robust accuracy under increasing perturbation budgets.
        """),
        code(base_setup),
        code("""
rows = []

clean_acc = accuracy(X, y)

for epsilon in np.linspace(0.0, 0.50, 11):
    X_attack = adversarial_perturb(X, y, epsilon)
    robust_acc = accuracy(X_attack, y)

    rows.append({
        "epsilon": epsilon,
        "clean_accuracy": clean_acc,
        "robust_accuracy": robust_acc,
        "robustness_gap": clean_acc - robust_acc,
    })

results = pd.DataFrame(rows)
results
        """),
        md("""
        ## Interpretation

        Robustness should be reported as a stress curve, not just a single clean accuracy score.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "02_adversarial_training_and_robust_optimization_lab.ipynb",
    "Adversarial Training and Robust Optimization Lab",
    [
        md("""
        ## Purpose

        This lab illustrates the robust optimization idea using synthetic perturbations.
        """),
        code(base_setup),
        code("""
def evaluate_weights(weights, epsilon_grid):
    def local_predict(features):
        return (sigmoid(features @ weights) >= 0.5).astype(int)

    def local_accuracy(features, labels):
        return float(np.mean(local_predict(features) == labels))

    rows = []
    clean_acc = local_accuracy(X, y)

    for epsilon in epsilon_grid:
        direction = np.where(y[:, None] == 1, -1.0, 1.0)
        X_attack = X + epsilon * direction * np.sign(weights)
        robust_acc = local_accuracy(X_attack, y)

        rows.append({
            "epsilon": epsilon,
            "clean_accuracy": clean_acc,
            "robust_accuracy": robust_acc,
            "robustness_gap": clean_acc - robust_acc,
        })

    return pd.DataFrame(rows)

baseline_results = evaluate_weights(model_weights, np.linspace(0, 0.50, 11))

# Educational proxy for a more conservative robust model:
# shrink weight magnitudes to reduce sensitivity.
robust_proxy_weights = 0.75 * model_weights
robust_proxy_results = evaluate_weights(robust_proxy_weights, np.linspace(0, 0.50, 11))
robust_proxy_results["model_type"] = "robust_proxy"
baseline_results["model_type"] = "baseline"

pd.concat([baseline_results, robust_proxy_results], ignore_index=True)
        """),
        md("""
        ## Interpretation

        Robust training changes the optimization target. It can improve some stress conditions while changing clean-data behavior.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "03_distribution_shift_corruption_and_runtime_monitoring_lab.ipynb",
    "Distribution Shift, Corruption, and Runtime Monitoring Lab",
    [
        md("""
        ## Purpose

        This lab simulates non-adversarial stress: corruption, distribution shift, and monitoring signals.
        """),
        code(base_setup),
        code("""
rows = []

for shift_strength in np.linspace(0.0, 1.0, 11):
    X_shifted = X + rng.normal(loc=shift_strength, scale=0.15, size=X.shape)
    shifted_accuracy = accuracy(X_shifted, y)

    rows.append({
        "shift_strength": shift_strength,
        "accuracy_under_shift": shifted_accuracy,
        "accuracy_drop": accuracy(X, y) - shifted_accuracy,
    })

shift_results = pd.DataFrame(rows)

shift_results["alert"] = shift_results["accuracy_drop"] > 0.15
shift_results
        """),
        md("""
        ## Interpretation

        Runtime resilience should track performance degradation and trigger review when shift indicators exceed thresholds.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "04_threat_models_governance_and_resilience_audit_lab.ipynb",
    "Threat Models, Governance, and Resilience Audit Lab",
    [
        md("""
        ## Purpose

        This lab frames robustness as a governance and audit problem.
        """),
        code("""
import pandas as pd

threat_models = pd.DataFrame([
    {
        "threat_model": "bounded_evasion_linf",
        "attacker_goal": "misclassification",
        "attacker_knowledge": "white_box",
        "lifecycle_stage": "inference",
        "tested": True,
    },
    {
        "threat_model": "training_data_poisoning",
        "attacker_goal": "model_behavior_change",
        "attacker_knowledge": "gray_box",
        "lifecycle_stage": "training",
        "tested": False,
    },
    {
        "threat_model": "physical_world_input_attack",
        "attacker_goal": "sensor_misclassification",
        "attacker_knowledge": "black_box",
        "lifecycle_stage": "deployment",
        "tested": False,
    },
    {
        "threat_model": "model_extraction",
        "attacker_goal": "steal_model_behavior",
        "attacker_knowledge": "query_access",
        "lifecycle_stage": "inference",
        "tested": False,
    },
])

governance_summary = threat_models.groupby(["lifecycle_stage", "tested"]).size().reset_index(name="count")

threat_models, governance_summary
        """),
        md("""
        ## Interpretation

        A robustness program should document not only test results, but which threat models remain untested.
        """),
    ],
)
