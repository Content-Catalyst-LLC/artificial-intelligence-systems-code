# AI Ethics, Human Rights, and Public Accountability

This repository folder supports the article:

**AI Ethics, Human Rights, and Public Accountability**

It provides reproducible examples for rights-impact scoring, disparity monitoring, remedy tracking, public-accountability documentation, governance review, human-rights impact assessment, and AI ethics workflows.

## Purpose

AI systems increasingly affect access to work, education, healthcare, housing, credit, public benefits, public services, speech, labor, and democratic participation. This repository treats AI ethics as an operational governance problem rather than a set of abstract principles.

The examples here examine:

- how to score rights impact across AI use cases;
- how residual ethical risk changes when governance controls improve;
- how adverse outcomes, appeals, remedies, and time to remedy can be monitored;
- how disparate burden may appear across groups;
- how public-accountability reports can be structured;
- how human-rights impact assessments can be documented;
- how audit, remedy, and decommissioning workflows support accountability.

## Contents

- `python/rights_impact_scoring.py` — rights-impact, burden, and accountability scoring workflow
- `python/requirements.txt` — Python dependencies
- `r/disparity_remedy_monitoring.R` — group disparity, appeal, remedy, and burden monitoring workflow
- `sql/ai_rights_accountability_schema.sql` — governance schema for rights impact, remedies, public reporting, audits, participation, vendors, and decommissioning
- `rust/` — command-line residual ethical-risk checker
- `go/` — lightweight public-accountability monitoring service
- `julia/governance_control_sensitivity.jl` — governance-control sensitivity analysis
- `typescript/` — rights-governance record validator
- `cpp/` — high-throughput rights-risk scoring example
- `docs/templates/` — human rights impact assessment, public accountability, remedy, participation, vendor, decommissioning, and audit templates
- `notebooks/` — notebook placeholder for expanded analysis
- `scripts/run_all.sh` — runs available workflows and smoke checks
- `outputs/` — generated workflow outputs

## Repository URL

https://github.com/Content-Catalyst-LLC/artificial-intelligence-systems-code/tree/main/articles/artificial-intelligence/ai-ethics-human-rights-public-accountability

## Data Policy

Do not commit sensitive, personal, regulated, protected, confidential, clinical, legal, employment, public-benefits, immigration, financial, student, health, or rights-impact case data. The included examples use synthetic data only.
