#!/usr/bin/env python3
"""
Create advanced Jupyter notebooks for:
Causal Inference and Experimental Design in AI Systems
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
    "prior_activity": rng.normal(0, 1, size=n),
    "domain_expertise": rng.normal(0, 1, size=n),
})

data["true_tau"] = (
    0.08
    + 0.04 * (data["prior_activity"] > 0)
    + 0.03 * (data["domain_expertise"] > 0)
)

data["y0"] = (
    0.30
    + 0.08 * data["prior_activity"]
    + 0.04 * data["domain_expertise"]
    + rng.normal(0, 0.05, size=n)
)

data["y1"] = data["y0"] + data["true_tau"]

data.head()
"""

write(
    NOTEBOOK_DIR / "01_prediction_vs_causation_and_potential_outcomes_lab.ipynb",
    "Prediction versus Causation and Potential Outcomes Lab",
    [
        md("""
        ## Purpose

        This lab introduces potential outcomes and shows why observed associations are not automatically causal effects.
        """),
        code(setup_code),
        code("""
true_ate = data["true_tau"].mean()

data["confounded_treatment"] = rng.binomial(
    1,
    1 / (1 + np.exp(-(-0.2 + 1.2 * data["prior_activity"]))),
)

data["observed_outcome"] = np.where(
    data["confounded_treatment"] == 1,
    data["y1"],
    data["y0"],
)

naive_difference = (
    data.loc[data["confounded_treatment"] == 1, "observed_outcome"].mean()
    - data.loc[data["confounded_treatment"] == 0, "observed_outcome"].mean()
)

pd.DataFrame([
    {"quantity": "true_ate", "value": true_ate},
    {"quantity": "naive_observed_difference", "value": naive_difference},
])
        """),
        md("""
        ## Interpretation

        The naive observed difference can be biased when treatment assignment depends on pre-treatment covariates.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "02_randomized_experiments_ab_testing_and_power_lab.ipynb",
    "Randomized Experiments, A/B Testing, and Power Lab",
    [
        md("""
        ## Purpose

        This lab simulates a randomized A/B test and estimates the treatment effect.
        """),
        code(setup_code),
        code("""
data["ab_assignment"] = rng.binomial(1, 0.5, size=len(data))

data["ab_outcome"] = np.where(
    data["ab_assignment"] == 1,
    data["y1"],
    data["y0"],
)

effect_estimate = (
    data.loc[data["ab_assignment"] == 1, "ab_outcome"].mean()
    - data.loc[data["ab_assignment"] == 0, "ab_outcome"].mean()
)

balance = data.groupby("ab_assignment").agg(
    units=("unit_id", "count"),
    mean_prior_activity=("prior_activity", "mean"),
    mean_domain_expertise=("domain_expertise", "mean"),
).reset_index()

effect_estimate, balance
        """),
        md("""
        ## Interpretation

        Randomization supports exchangeability in expectation, but experiments still require balance checks, logging integrity, and valid outcome definitions.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "03_observational_confounding_propensity_scores_and_ipw_lab.ipynb",
    "Observational Confounding, Propensity Scores, and IPW Lab",
    [
        md("""
        ## Purpose

        This lab demonstrates confounding, propensity scores, and inverse probability weighting.
        """),
        code(setup_code),
        code("""
propensity = 1 / (1 + np.exp(-(-0.2 + 1.2 * data["prior_activity"])))
data["propensity"] = propensity
data["observed_treatment"] = rng.binomial(1, propensity)

data["observed_outcome"] = np.where(
    data["observed_treatment"] == 1,
    data["y1"],
    data["y0"],
)

weights = (
    data["observed_treatment"] / data["propensity"]
    + (1 - data["observed_treatment"]) / (1 - data["propensity"])
)

treated_mean = np.average(
    data.loc[data["observed_treatment"] == 1, "observed_outcome"],
    weights=weights[data["observed_treatment"] == 1],
)

control_mean = np.average(
    data.loc[data["observed_treatment"] == 0, "observed_outcome"],
    weights=weights[data["observed_treatment"] == 0],
)

ipw_estimate = treated_mean - control_mean

naive_estimate = (
    data.loc[data["observed_treatment"] == 1, "observed_outcome"].mean()
    - data.loc[data["observed_treatment"] == 0, "observed_outcome"].mean()
)

pd.DataFrame([
    {"estimate": "true_ate", "value": data["true_tau"].mean()},
    {"estimate": "naive_observational", "value": naive_estimate},
    {"estimate": "ipw_estimate", "value": ipw_estimate},
])
        """),
        md("""
        ## Interpretation

        IPW can reduce measured confounding when the propensity model is well-specified and identification assumptions are plausible.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "04_heterogeneous_treatment_effects_transportability_and_governance_lab.ipynb",
    "Heterogeneous Treatment Effects, Transportability, and Governance Lab",
    [
        md("""
        ## Purpose

        This lab frames heterogeneous effects and causal governance documentation.
        """),
        code(setup_code),
        code("""
data["segment"] = np.where(
    (data["prior_activity"] > 0) & (data["domain_expertise"] > 0),
    "high_activity_high_expertise",
    np.where(
        data["prior_activity"] > 0,
        "high_activity",
        "lower_activity"
    )
)

segment_effects = data.groupby("segment").agg(
    units=("unit_id", "count"),
    mean_true_tau=("true_tau", "mean"),
    mean_prior_activity=("prior_activity", "mean"),
    mean_domain_expertise=("domain_expertise", "mean"),
).reset_index()

governance_review = pd.DataFrame([
    {
        "area": "causal_question",
        "question": "Is the intervention question clearly stated?",
        "status": "complete",
        "owner": "Research / Product",
    },
    {
        "area": "estimand",
        "question": "Are treatment, outcome, unit, population, and time horizon documented?",
        "status": "partial",
        "owner": "Causal Analysis",
    },
    {
        "area": "interference",
        "question": "Could one unit's treatment affect another unit's outcome?",
        "status": "partial",
        "owner": "Experimentation",
    },
    {
        "area": "transportability",
        "question": "Can the estimated effect generalize to the target deployment context?",
        "status": "missing",
        "owner": "Governance",
    },
])

segment_effects, governance_review
        """),
        md("""
        ## Interpretation

        Causal machine learning should pair heterogeneous-effect estimation with governance documentation about assumptions, interference, and transportability.
        """),
    ],
)
