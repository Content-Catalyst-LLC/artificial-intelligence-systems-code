# AI Risk Registers, Model Cards, and Audit Documentation

This repository folder supports the article:

**AI Risk Registers, Model Cards, and Audit Documentation**

It provides reproducible examples for risk-register scoring, model-card completeness checks, audit evidence tracking, lifecycle traceability, governance documentation, incident records, corrective-action tracking, and accountable AI operations.

## Purpose

AI governance requires durable evidence infrastructure. Risk registers, model cards, system cards, data documentation, audit records, incident reports, monitoring logs, and lifecycle traces help organizations understand what an AI system is, what risks it creates, who owns those risks, what controls exist, and what happened when the system changed or failed.

The examples here examine:

- how to score residual risk;
- how to prioritize documentation gaps;
- how to evaluate audit-evidence completeness;
- how to track model-card and system-card status;
- how to connect risks, owners, incidents, controls, and corrective actions;
- how to structure lifecycle traceability across data, model, evaluation, deployment, and monitoring;
- how documentation becomes governance infrastructure rather than paperwork.

## Contents

- `python/risk_register_documentation_scoring.py` — risk register, documentation completeness, and priority workflow
- `python/requirements.txt` — Python dependencies
- `r/audit_evidence_gap_analysis.R` — audit evidence and documentation-gap workflow
- `sql/ai_documentation_governance_schema.sql` — governance schema for systems, model cards, risk registers, evidence links, lifecycle versions, incidents, corrective actions, and documentation reviews
- `rust/` — command-line residual-risk and documentation-priority checker
- `go/` — lightweight documentation-governance status service
- `julia/documentation_sensitivity.jl` — documentation-completeness sensitivity analysis
- `typescript/` — model-card and audit-record validator
- `cpp/` — high-throughput documentation-priority scoring example
- `docs/templates/` — risk register, model card, system card, datasheet, audit evidence, incident, corrective-action, and review templates
- `notebooks/` — notebook placeholder for expanded analysis
- `scripts/run_all.sh` — runs available workflows and smoke checks
- `outputs/` — generated workflow outputs

## Repository URL

https://github.com/Content-Catalyst-LLC/artificial-intelligence-systems-code/tree/main/articles/artificial-intelligence/ai-risk-registers-model-cards-audit-documentation

## Data Policy

Do not commit sensitive, personal, regulated, protected, confidential, proprietary, production, credential, incident-confidential, legal, clinical, employment, public-benefits, financial, student, or security-sensitive data. The included examples use synthetic data only.
