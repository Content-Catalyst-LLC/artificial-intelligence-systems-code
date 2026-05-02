# Human Oversight, Contestability, and AI Accountability

This repository folder supports the article:

**Human Oversight, Contestability, and AI Accountability**

It provides reproducible examples for oversight triage, contestability monitoring, appeal analytics, accountability documentation, reviewer workload analysis, incident reporting, audit checklists, and governance reporting.

## Purpose

AI-assisted decisions require more than model accuracy. They require human review, contestability, auditability, correction, monitoring, and institutional responsibility. This repository treats AI accountability as a sociotechnical governance system rather than a simple technical compliance task.

The examples here examine:

- when AI-assisted decisions should be escalated to human review;
- how risk, uncertainty, rights sensitivity, and vulnerability affect routing;
- how appeals and corrections can be monitored;
- how reviewer workload can weaken meaningful oversight;
- how decision records support auditability;
- how incident reports, appeal templates, and audit checklists support governance.

## Contents

- `python/oversight_triage.py` — risk-weighted human review routing simulation
- `python/requirements.txt` — Python dependencies
- `r/contestability_monitoring.R` — appeal and correction monitoring workflow
- `sql/accountability_schema.sql` — governance database schema and sample queries
- `rust/` — command-line threshold checker
- `go/` — lightweight governance monitoring service example
- `julia/oversight_thresholds.jl` — threshold sensitivity analysis
- `typescript/` — oversight dashboard data validator
- `cpp/` — high-throughput risk scoring example
- `docs/templates/` — oversight, appeal, incident, audit, decision-record, and workload templates
- `notebooks/` — notebook placeholder for expanded analysis
- `scripts/run_all.sh` — runs available workflows and smoke checks
- `outputs/` — generated workflow outputs

## Repository URL

https://github.com/Content-Catalyst-LLC/artificial-intelligence-systems-code/tree/main/articles/artificial-intelligence/human-oversight-contestability-ai-accountability

## Data Policy

Do not commit sensitive, personal, regulated, clinical, legal, government-benefits, financial, employment, immigration, or confidential data. The included examples use synthetic data only.
