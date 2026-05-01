-- Transfer Learning, Fine-Tuning, and Model Adaptation
-- SQL schema for base models, adapted models, fine-tuning runs, adapters,
-- LoRA records, evaluation results, deployment approvals, and governance review.

CREATE TABLE IF NOT EXISTS base_model (
    base_model_id TEXT PRIMARY KEY,
    model_name TEXT NOT NULL,
    model_version TEXT NOT NULL,
    provider_or_owner TEXT,
    modality TEXT NOT NULL,
    parameter_count INTEGER,
    pretraining_data_summary TEXT,
    intended_base_use TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS target_domain (
    target_domain_id TEXT PRIMARY KEY,
    domain_name TEXT NOT NULL,
    task_name TEXT NOT NULL,
    target_data_summary TEXT,
    sensitive_domain INTEGER NOT NULL DEFAULT 0,
    domain_shift_summary TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS adaptation_run (
    adaptation_run_id TEXT PRIMARY KEY,
    base_model_id TEXT NOT NULL,
    target_domain_id TEXT NOT NULL,
    adaptation_method TEXT NOT NULL,
    training_dataset_uri TEXT,
    validation_dataset_uri TEXT,
    trainable_parameter_share REAL,
    compute_cost_index REAL,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    run_status TEXT NOT NULL,
    FOREIGN KEY (base_model_id) REFERENCES base_model(base_model_id),
    FOREIGN KEY (target_domain_id) REFERENCES target_domain(target_domain_id)
);

CREATE TABLE IF NOT EXISTS adapted_model (
    adapted_model_id TEXT PRIMARY KEY,
    adaptation_run_id TEXT NOT NULL,
    adapted_model_name TEXT NOT NULL,
    adapted_model_version TEXT NOT NULL,
    artifact_uri TEXT,
    deployment_scope TEXT,
    approved_use TEXT,
    prohibited_use TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (adaptation_run_id) REFERENCES adaptation_run(adaptation_run_id)
);

CREATE TABLE IF NOT EXISTS adapter_record (
    adapter_id TEXT PRIMARY KEY,
    adaptation_run_id TEXT NOT NULL,
    adapter_type TEXT NOT NULL,
    rank_value INTEGER,
    parameter_count INTEGER,
    adapter_uri TEXT,
    merge_status TEXT,
    notes TEXT,
    FOREIGN KEY (adaptation_run_id) REFERENCES adaptation_run(adaptation_run_id)
);

CREATE TABLE IF NOT EXISTS adaptation_evaluation (
    evaluation_id TEXT PRIMARY KEY,
    adaptation_run_id TEXT NOT NULL,
    evaluation_set_name TEXT NOT NULL,
    evaluation_type TEXT NOT NULL,
    metric_name TEXT NOT NULL,
    metric_value REAL NOT NULL,
    baseline_value REAL,
    transfer_gain REAL,
    evaluated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    FOREIGN KEY (adaptation_run_id) REFERENCES adaptation_run(adaptation_run_id)
);

CREATE TABLE IF NOT EXISTS forgetting_review (
    forgetting_review_id TEXT PRIMARY KEY,
    adaptation_run_id TEXT NOT NULL,
    source_capability_name TEXT NOT NULL,
    pre_adaptation_score REAL,
    post_adaptation_score REAL,
    retention_score REAL,
    review_status TEXT NOT NULL,
    reviewed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (adaptation_run_id) REFERENCES adaptation_run(adaptation_run_id)
);

CREATE TABLE IF NOT EXISTS adaptation_governance_review (
    governance_review_id TEXT PRIMARY KEY,
    adaptation_run_id TEXT NOT NULL,
    reviewer TEXT NOT NULL,
    review_type TEXT NOT NULL,
    review_date DATE NOT NULL,
    decision TEXT NOT NULL,
    decision_rationale TEXT NOT NULL,
    required_actions TEXT,
    next_review_date DATE,
    FOREIGN KEY (adaptation_run_id) REFERENCES adaptation_run(adaptation_run_id)
);

CREATE TABLE IF NOT EXISTS adapted_model_deployment (
    deployment_id TEXT PRIMARY KEY,
    adapted_model_id TEXT NOT NULL,
    deployment_environment TEXT NOT NULL,
    deployment_status TEXT NOT NULL,
    approved_by TEXT,
    deployed_at TIMESTAMP,
    rollback_plan_uri TEXT,
    monitoring_plan_uri TEXT,
    FOREIGN KEY (adapted_model_id) REFERENCES adapted_model(adapted_model_id)
);

CREATE TABLE IF NOT EXISTS adaptation_drift_monitor (
    drift_record_id TEXT PRIMARY KEY,
    adapted_model_id TEXT NOT NULL,
    drift_metric TEXT NOT NULL,
    drift_value REAL NOT NULL,
    threshold_warning REAL,
    threshold_action REAL,
    drift_status TEXT NOT NULL,
    measured_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (adapted_model_id) REFERENCES adapted_model(adapted_model_id)
);

CREATE INDEX IF NOT EXISTS idx_adaptation_base_target
ON adaptation_run(base_model_id, target_domain_id);

CREATE INDEX IF NOT EXISTS idx_adaptation_method_status
ON adaptation_run(adaptation_method, run_status);

CREATE INDEX IF NOT EXISTS idx_adaptation_evaluation_run
ON adaptation_evaluation(adaptation_run_id, metric_name);

CREATE INDEX IF NOT EXISTS idx_forgetting_review_run
ON forgetting_review(adaptation_run_id, review_status);

CREATE VIEW IF NOT EXISTS v_adaptation_runs_requiring_review AS
SELECT
    ar.adaptation_run_id,
    bm.model_name,
    bm.model_version,
    td.domain_name,
    td.task_name,
    ar.adaptation_method,
    td.sensitive_domain,
    fr.retention_score,
    agr.decision
FROM adaptation_run ar
JOIN base_model bm
    ON ar.base_model_id = bm.base_model_id
JOIN target_domain td
    ON ar.target_domain_id = td.target_domain_id
LEFT JOIN forgetting_review fr
    ON ar.adaptation_run_id = fr.adaptation_run_id
LEFT JOIN adaptation_governance_review agr
    ON ar.adaptation_run_id = agr.adaptation_run_id
WHERE td.sensitive_domain = 1
   OR fr.retention_score < 0.80
   OR agr.decision IS NULL;

CREATE VIEW IF NOT EXISTS v_negative_transfer_results AS
SELECT
    ar.adaptation_run_id,
    ar.adaptation_method,
    ae.evaluation_set_name,
    ae.metric_name,
    ae.metric_value,
    ae.baseline_value,
    ae.transfer_gain
FROM adaptation_run ar
JOIN adaptation_evaluation ae
    ON ar.adaptation_run_id = ae.adaptation_run_id
WHERE ae.transfer_gain < 0;
