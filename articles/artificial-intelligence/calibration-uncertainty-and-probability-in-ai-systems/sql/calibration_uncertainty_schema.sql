-- Calibration, Uncertainty, and Probability in AI Systems
-- SQL schema for probability predictions, calibration bins, uncertainty signals,
-- thresholds, abstention, human review, incidents, recalibration reviews,
-- and governance records.

CREATE TABLE IF NOT EXISTS probability_model_registry (
    model_id TEXT PRIMARY KEY,
    model_name TEXT NOT NULL,
    model_version TEXT NOT NULL,
    model_type TEXT NOT NULL,
    intended_use TEXT NOT NULL,
    owner TEXT NOT NULL,
    deployment_status TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS prediction_log (
    prediction_id TEXT PRIMARY KEY,
    model_id TEXT NOT NULL,
    case_id_hash TEXT NOT NULL,
    source_system TEXT,
    predicted_probability REAL NOT NULL,
    predicted_label TEXT,
    prediction_entropy REAL,
    uncertainty_zone TEXT,
    model_version TEXT NOT NULL,
    predicted_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (model_id) REFERENCES probability_model_registry(model_id)
);

CREATE TABLE IF NOT EXISTS observed_label (
    observed_label_id TEXT PRIMARY KEY,
    prediction_id TEXT NOT NULL,
    observed_label TEXT NOT NULL,
    label_source TEXT,
    label_quality_score REAL,
    observed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (prediction_id) REFERENCES prediction_log(prediction_id)
);

CREATE TABLE IF NOT EXISTS calibration_bin_metric (
    calibration_bin_id TEXT PRIMARY KEY,
    model_id TEXT NOT NULL,
    evaluation_period_start DATE NOT NULL,
    evaluation_period_end DATE NOT NULL,
    bin_lower REAL NOT NULL,
    bin_upper REAL NOT NULL,
    cases INTEGER NOT NULL,
    mean_confidence REAL NOT NULL,
    observed_rate REAL NOT NULL,
    absolute_calibration_gap REAL NOT NULL,
    slice_name TEXT,
    slice_value TEXT,
    measured_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (model_id) REFERENCES probability_model_registry(model_id)
);

CREATE TABLE IF NOT EXISTS probability_evaluation_metric (
    evaluation_metric_id TEXT PRIMARY KEY,
    model_id TEXT NOT NULL,
    metric_name TEXT NOT NULL,
    metric_value REAL NOT NULL,
    warning_threshold REAL,
    action_threshold REAL,
    metric_status TEXT NOT NULL,
    slice_name TEXT,
    slice_value TEXT,
    measured_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (model_id) REFERENCES probability_model_registry(model_id)
);

CREATE TABLE IF NOT EXISTS uncertainty_signal (
    uncertainty_signal_id TEXT PRIMARY KEY,
    model_id TEXT NOT NULL,
    prediction_id TEXT,
    signal_name TEXT NOT NULL,
    signal_value REAL NOT NULL,
    signal_category TEXT NOT NULL,
    signal_status TEXT NOT NULL,
    measured_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (model_id) REFERENCES probability_model_registry(model_id),
    FOREIGN KEY (prediction_id) REFERENCES prediction_log(prediction_id)
);

CREATE TABLE IF NOT EXISTS threshold_policy (
    threshold_policy_id TEXT PRIMARY KEY,
    model_id TEXT NOT NULL,
    policy_name TEXT NOT NULL,
    lower_bound REAL,
    upper_bound REAL,
    action_name TEXT NOT NULL,
    requires_human_review INTEGER DEFAULT 0,
    requires_abstention INTEGER DEFAULT 0,
    policy_status TEXT NOT NULL,
    approved_by TEXT,
    approved_at TIMESTAMP,
    FOREIGN KEY (model_id) REFERENCES probability_model_registry(model_id)
);

CREATE TABLE IF NOT EXISTS human_review_event (
    human_review_event_id TEXT PRIMARY KEY,
    prediction_id TEXT NOT NULL,
    review_reason TEXT NOT NULL,
    reviewer TEXT,
    review_decision TEXT NOT NULL,
    review_notes TEXT,
    reviewed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (prediction_id) REFERENCES prediction_log(prediction_id)
);

CREATE TABLE IF NOT EXISTS recalibration_review (
    recalibration_review_id TEXT PRIMARY KEY,
    model_id TEXT NOT NULL,
    trigger_signal TEXT NOT NULL,
    trigger_rationale TEXT NOT NULL,
    calibration_method TEXT,
    review_decision TEXT NOT NULL,
    decision_rationale TEXT NOT NULL,
    approved_by TEXT,
    reviewed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (model_id) REFERENCES probability_model_registry(model_id)
);

CREATE TABLE IF NOT EXISTS uncertainty_incident (
    incident_id TEXT PRIMARY KEY,
    model_id TEXT NOT NULL,
    incident_type TEXT NOT NULL,
    severity TEXT NOT NULL,
    incident_status TEXT NOT NULL,
    description TEXT NOT NULL,
    remediation_summary TEXT,
    detected_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP,
    FOREIGN KEY (model_id) REFERENCES probability_model_registry(model_id)
);

CREATE TABLE IF NOT EXISTS uncertainty_governance_review (
    governance_review_id TEXT PRIMARY KEY,
    model_id TEXT NOT NULL,
    review_type TEXT NOT NULL,
    reviewer TEXT NOT NULL,
    review_date DATE NOT NULL,
    decision TEXT NOT NULL,
    decision_rationale TEXT NOT NULL,
    required_actions TEXT,
    next_review_date DATE,
    FOREIGN KEY (model_id) REFERENCES probability_model_registry(model_id)
);

CREATE INDEX IF NOT EXISTS idx_prediction_log_model_time
ON prediction_log(model_id, predicted_at);

CREATE INDEX IF NOT EXISTS idx_observed_label_prediction
ON observed_label(prediction_id, observed_at);

CREATE INDEX IF NOT EXISTS idx_calibration_bin_model_slice
ON calibration_bin_metric(model_id, slice_name, slice_value);

CREATE INDEX IF NOT EXISTS idx_probability_eval_model_metric
ON probability_evaluation_metric(model_id, metric_name, metric_status);

CREATE INDEX IF NOT EXISTS idx_uncertainty_signal_model_status
ON uncertainty_signal(model_id, signal_status, signal_category);

CREATE VIEW IF NOT EXISTS v_probability_metrics_requiring_review AS
SELECT
    m.model_name,
    m.model_version,
    e.metric_name,
    e.metric_value,
    e.warning_threshold,
    e.action_threshold,
    e.metric_status,
    e.slice_name,
    e.slice_value
FROM probability_evaluation_metric e
JOIN probability_model_registry m
    ON e.model_id = m.model_id
WHERE e.metric_status IN ('warning', 'action', 'incident');

CREATE VIEW IF NOT EXISTS v_uncertain_predictions_requiring_review AS
SELECT
    p.prediction_id,
    m.model_name,
    m.model_version,
    p.source_system,
    p.predicted_probability,
    p.prediction_entropy,
    p.uncertainty_zone,
    p.predicted_at
FROM prediction_log p
JOIN probability_model_registry m
    ON p.model_id = m.model_id
WHERE p.uncertainty_zone IN ('human_review', 'abstain', 'urgent_review')
   OR p.prediction_entropy >= 0.62;
