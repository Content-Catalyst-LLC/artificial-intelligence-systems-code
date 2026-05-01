-- Self-Supervised Learning and Foundation Models
-- SQL schema for pretraining runs, datasets, objectives, evaluation,
-- adaptation records, monitoring, and foundation-model governance.

CREATE TABLE IF NOT EXISTS foundation_model (
    foundation_model_id TEXT PRIMARY KEY,
    model_name TEXT NOT NULL,
    model_version TEXT NOT NULL,
    modality_scope TEXT NOT NULL,
    parameter_count INTEGER,
    architecture_summary TEXT,
    intended_base_use TEXT,
    prohibited_use TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS pretraining_dataset (
    dataset_id TEXT PRIMARY KEY,
    dataset_name TEXT NOT NULL,
    modality TEXT NOT NULL,
    data_source_summary TEXT NOT NULL,
    provenance_score REAL,
    data_quality_score REAL,
    licensing_review_status TEXT,
    privacy_review_status TEXT,
    bias_review_status TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS self_supervised_objective (
    objective_id TEXT PRIMARY KEY,
    objective_name TEXT NOT NULL,
    objective_type TEXT NOT NULL,
    mask_strategy TEXT,
    contrastive_strategy TEXT,
    reconstruction_target TEXT,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS pretraining_run (
    pretraining_run_id TEXT PRIMARY KEY,
    foundation_model_id TEXT NOT NULL,
    dataset_id TEXT NOT NULL,
    objective_id TEXT NOT NULL,
    compute_environment TEXT,
    compute_cost_index REAL,
    run_status TEXT NOT NULL,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    training_artifact_uri TEXT,
    FOREIGN KEY (foundation_model_id) REFERENCES foundation_model(foundation_model_id),
    FOREIGN KEY (dataset_id) REFERENCES pretraining_dataset(dataset_id),
    FOREIGN KEY (objective_id) REFERENCES self_supervised_objective(objective_id)
);

CREATE TABLE IF NOT EXISTS pretraining_evaluation (
    evaluation_id TEXT PRIMARY KEY,
    pretraining_run_id TEXT NOT NULL,
    evaluation_type TEXT NOT NULL,
    metric_name TEXT NOT NULL,
    metric_value REAL NOT NULL,
    evaluation_dataset_uri TEXT,
    evaluated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    FOREIGN KEY (pretraining_run_id) REFERENCES pretraining_run(pretraining_run_id)
);

CREATE TABLE IF NOT EXISTS foundation_model_risk_review (
    risk_review_id TEXT PRIMARY KEY,
    foundation_model_id TEXT NOT NULL,
    review_type TEXT NOT NULL,
    reviewer TEXT,
    risk_category TEXT NOT NULL,
    risk_score REAL,
    finding_summary TEXT NOT NULL,
    mitigation_actions TEXT,
    review_status TEXT NOT NULL,
    reviewed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (foundation_model_id) REFERENCES foundation_model(foundation_model_id)
);

CREATE TABLE IF NOT EXISTS foundation_model_adaptation (
    adaptation_id TEXT PRIMARY KEY,
    foundation_model_id TEXT NOT NULL,
    adaptation_method TEXT NOT NULL,
    downstream_domain TEXT NOT NULL,
    downstream_task TEXT NOT NULL,
    adaptation_artifact_uri TEXT,
    approval_status TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (foundation_model_id) REFERENCES foundation_model(foundation_model_id)
);

CREATE TABLE IF NOT EXISTS foundation_model_monitoring (
    monitoring_id TEXT PRIMARY KEY,
    foundation_model_id TEXT NOT NULL,
    monitoring_signal TEXT NOT NULL,
    signal_value REAL,
    threshold_warning REAL,
    threshold_action REAL,
    status TEXT NOT NULL,
    measured_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    FOREIGN KEY (foundation_model_id) REFERENCES foundation_model(foundation_model_id)
);

CREATE TABLE IF NOT EXISTS foundation_model_incident (
    incident_id TEXT PRIMARY KEY,
    foundation_model_id TEXT NOT NULL,
    incident_type TEXT NOT NULL,
    severity TEXT NOT NULL,
    incident_status TEXT NOT NULL,
    description TEXT NOT NULL,
    detected_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP,
    remediation_summary TEXT,
    FOREIGN KEY (foundation_model_id) REFERENCES foundation_model(foundation_model_id)
);

CREATE TABLE IF NOT EXISTS foundation_model_governance_review (
    governance_review_id TEXT PRIMARY KEY,
    foundation_model_id TEXT NOT NULL,
    review_type TEXT NOT NULL,
    reviewer TEXT NOT NULL,
    review_date DATE NOT NULL,
    decision TEXT NOT NULL,
    decision_rationale TEXT NOT NULL,
    required_actions TEXT,
    next_review_date DATE,
    FOREIGN KEY (foundation_model_id) REFERENCES foundation_model(foundation_model_id)
);

CREATE INDEX IF NOT EXISTS idx_pretraining_run_model
ON pretraining_run(foundation_model_id, run_status);

CREATE INDEX IF NOT EXISTS idx_pretraining_eval_run
ON pretraining_evaluation(pretraining_run_id, metric_name);

CREATE INDEX IF NOT EXISTS idx_foundation_model_risk
ON foundation_model_risk_review(foundation_model_id, risk_category, review_status);

CREATE INDEX IF NOT EXISTS idx_foundation_monitoring_status
ON foundation_model_monitoring(foundation_model_id, status);

CREATE VIEW IF NOT EXISTS v_foundation_models_requiring_review AS
SELECT
    fm.foundation_model_id,
    fm.model_name,
    fm.model_version,
    fm.modality_scope,
    rr.risk_category,
    rr.risk_score,
    rr.review_status
FROM foundation_model fm
JOIN foundation_model_risk_review rr
    ON fm.foundation_model_id = rr.foundation_model_id
WHERE rr.risk_score >= 0.45
   OR rr.review_status IN ('open', 'requires_action');

CREATE VIEW IF NOT EXISTS v_pretraining_runs_with_data_risk AS
SELECT
    pr.pretraining_run_id,
    fm.model_name,
    ds.dataset_name,
    ds.provenance_score,
    ds.privacy_review_status,
    ds.bias_review_status,
    pr.compute_cost_index
FROM pretraining_run pr
JOIN foundation_model fm
    ON pr.foundation_model_id = fm.foundation_model_id
JOIN pretraining_dataset ds
    ON pr.dataset_id = ds.dataset_id
WHERE ds.provenance_score < 0.50
   OR ds.privacy_review_status NOT IN ('approved', 'not_applicable')
   OR ds.bias_review_status NOT IN ('approved', 'not_applicable');
