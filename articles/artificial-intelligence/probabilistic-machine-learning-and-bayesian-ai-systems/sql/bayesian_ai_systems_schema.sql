-- Probabilistic Machine Learning and Bayesian AI Systems
-- SQL schema for Bayesian model records, priors, likelihoods, posterior summaries,
-- prediction logs, calibration audits, decision thresholds, and governance review.

CREATE TABLE IF NOT EXISTS bayesian_model (
    bayesian_model_id TEXT PRIMARY KEY,
    model_name TEXT NOT NULL,
    model_version TEXT NOT NULL,
    model_family TEXT NOT NULL,
    intended_use TEXT NOT NULL,
    prohibited_use TEXT,
    owner TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS prior_record (
    prior_id TEXT PRIMARY KEY,
    bayesian_model_id TEXT NOT NULL,
    parameter_name TEXT NOT NULL,
    prior_distribution TEXT NOT NULL,
    prior_parameters TEXT NOT NULL,
    prior_justification TEXT NOT NULL,
    reviewer TEXT,
    review_status TEXT NOT NULL,
    FOREIGN KEY (bayesian_model_id) REFERENCES bayesian_model(bayesian_model_id)
);

CREATE TABLE IF NOT EXISTS likelihood_record (
    likelihood_id TEXT PRIMARY KEY,
    bayesian_model_id TEXT NOT NULL,
    likelihood_family TEXT NOT NULL,
    observed_variable TEXT NOT NULL,
    measurement_assumptions TEXT,
    missing_data_strategy TEXT,
    review_status TEXT NOT NULL,
    FOREIGN KEY (bayesian_model_id) REFERENCES bayesian_model(bayesian_model_id)
);

CREATE TABLE IF NOT EXISTS inference_run (
    inference_run_id TEXT PRIMARY KEY,
    bayesian_model_id TEXT NOT NULL,
    inference_method TEXT NOT NULL,
    dataset_uri TEXT,
    run_status TEXT NOT NULL,
    convergence_status TEXT,
    diagnostic_summary TEXT,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    FOREIGN KEY (bayesian_model_id) REFERENCES bayesian_model(bayesian_model_id)
);

CREATE TABLE IF NOT EXISTS posterior_summary (
    posterior_summary_id TEXT PRIMARY KEY,
    inference_run_id TEXT NOT NULL,
    parameter_name TEXT NOT NULL,
    posterior_mean REAL,
    posterior_median REAL,
    posterior_sd REAL,
    ci_lower REAL,
    ci_upper REAL,
    effective_sample_size REAL,
    rhat REAL,
    FOREIGN KEY (inference_run_id) REFERENCES inference_run(inference_run_id)
);

CREATE TABLE IF NOT EXISTS predictive_record (
    prediction_id TEXT PRIMARY KEY,
    bayesian_model_id TEXT NOT NULL,
    case_id TEXT NOT NULL,
    predicted_probability REAL,
    predictive_mean REAL,
    predictive_sd REAL,
    interval_lower REAL,
    interval_upper REAL,
    uncertainty_type TEXT,
    predicted_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (bayesian_model_id) REFERENCES bayesian_model(bayesian_model_id)
);

CREATE TABLE IF NOT EXISTS calibration_audit (
    calibration_audit_id TEXT PRIMARY KEY,
    bayesian_model_id TEXT NOT NULL,
    audit_dataset_uri TEXT,
    calibration_metric TEXT NOT NULL,
    metric_value REAL NOT NULL,
    subgroup_name TEXT,
    audit_status TEXT NOT NULL,
    audited_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (bayesian_model_id) REFERENCES bayesian_model(bayesian_model_id)
);

CREATE TABLE IF NOT EXISTS decision_threshold (
    threshold_id TEXT PRIMARY KEY,
    bayesian_model_id TEXT NOT NULL,
    decision_name TEXT NOT NULL,
    threshold_type TEXT NOT NULL,
    threshold_value REAL NOT NULL,
    loss_assumption TEXT,
    approval_status TEXT NOT NULL,
    approved_by TEXT,
    approved_at TIMESTAMP,
    FOREIGN KEY (bayesian_model_id) REFERENCES bayesian_model(bayesian_model_id)
);

CREATE TABLE IF NOT EXISTS probabilistic_decision_log (
    decision_log_id TEXT PRIMARY KEY,
    bayesian_model_id TEXT NOT NULL,
    prediction_id TEXT NOT NULL,
    decision_action TEXT NOT NULL,
    expected_loss_no_action REAL,
    expected_loss_action REAL,
    human_override INTEGER DEFAULT 0,
    override_reason TEXT,
    decided_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (bayesian_model_id) REFERENCES bayesian_model(bayesian_model_id),
    FOREIGN KEY (prediction_id) REFERENCES predictive_record(prediction_id)
);

CREATE TABLE IF NOT EXISTS bayesian_governance_review (
    governance_review_id TEXT PRIMARY KEY,
    bayesian_model_id TEXT NOT NULL,
    review_type TEXT NOT NULL,
    reviewer TEXT NOT NULL,
    review_date DATE NOT NULL,
    decision TEXT NOT NULL,
    decision_rationale TEXT NOT NULL,
    required_actions TEXT,
    next_review_date DATE,
    FOREIGN KEY (bayesian_model_id) REFERENCES bayesian_model(bayesian_model_id)
);

CREATE TABLE IF NOT EXISTS uncertainty_monitoring_record (
    monitoring_id TEXT PRIMARY KEY,
    bayesian_model_id TEXT NOT NULL,
    monitoring_signal TEXT NOT NULL,
    signal_value REAL NOT NULL,
    threshold_warning REAL,
    threshold_action REAL,
    monitoring_status TEXT NOT NULL,
    measured_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (bayesian_model_id) REFERENCES bayesian_model(bayesian_model_id)
);

CREATE INDEX IF NOT EXISTS idx_bayesian_model_family
ON bayesian_model(model_family, model_version);

CREATE INDEX IF NOT EXISTS idx_inference_model_status
ON inference_run(bayesian_model_id, run_status, convergence_status);

CREATE INDEX IF NOT EXISTS idx_posterior_run_parameter
ON posterior_summary(inference_run_id, parameter_name);

CREATE INDEX IF NOT EXISTS idx_prediction_model_time
ON predictive_record(bayesian_model_id, predicted_at);

CREATE INDEX IF NOT EXISTS idx_calibration_model_metric
ON calibration_audit(bayesian_model_id, calibration_metric, subgroup_name);

CREATE VIEW IF NOT EXISTS v_bayesian_models_requiring_review AS
SELECT
    bm.bayesian_model_id,
    bm.model_name,
    bm.model_version,
    bm.model_family,
    ca.calibration_metric,
    ca.metric_value,
    ca.subgroup_name,
    ca.audit_status
FROM bayesian_model bm
LEFT JOIN calibration_audit ca
    ON bm.bayesian_model_id = ca.bayesian_model_id
WHERE ca.audit_status IN ('warning', 'action', 'requires_review')
   OR ca.metric_value > 0.10;

CREATE VIEW IF NOT EXISTS v_inference_diagnostic_warnings AS
SELECT
    ir.inference_run_id,
    bm.model_name,
    ir.inference_method,
    ir.convergence_status,
    ps.parameter_name,
    ps.effective_sample_size,
    ps.rhat
FROM inference_run ir
JOIN bayesian_model bm
    ON ir.bayesian_model_id = bm.bayesian_model_id
LEFT JOIN posterior_summary ps
    ON ir.inference_run_id = ps.inference_run_id
WHERE ir.convergence_status NOT IN ('passed', 'not_applicable')
   OR ps.rhat > 1.01
   OR ps.effective_sample_size < 400;
