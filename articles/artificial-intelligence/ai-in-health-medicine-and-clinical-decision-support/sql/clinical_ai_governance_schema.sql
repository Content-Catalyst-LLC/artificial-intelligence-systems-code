-- AI in Health, Medicine, and Clinical Decision Support
-- SQL schema for clinical AI systems, intended use, validation evidence,
-- model outputs, monitoring, subgroup review, incidents, change control,
-- and governance review.

CREATE TABLE IF NOT EXISTS clinical_ai_system_registry (
    clinical_ai_system_id TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    system_version TEXT NOT NULL,
    system_type TEXT NOT NULL,
    intended_use TEXT NOT NULL,
    prohibited_use TEXT,
    clinical_owner TEXT NOT NULL,
    technical_owner TEXT NOT NULL,
    deployment_status TEXT NOT NULL,
    regulatory_status TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS clinical_ai_intended_use (
    intended_use_id TEXT PRIMARY KEY,
    clinical_ai_system_id TEXT NOT NULL,
    clinical_context TEXT NOT NULL,
    user_group TEXT NOT NULL,
    patient_population TEXT NOT NULL,
    decision_supported TEXT NOT NULL,
    action_triggered TEXT,
    human_oversight_required INTEGER DEFAULT 1,
    FOREIGN KEY (clinical_ai_system_id) REFERENCES clinical_ai_system_registry(clinical_ai_system_id)
);

CREATE TABLE IF NOT EXISTS clinical_validation_study (
    validation_study_id TEXT PRIMARY KEY,
    clinical_ai_system_id TEXT NOT NULL,
    study_name TEXT NOT NULL,
    validation_type TEXT NOT NULL,
    site_count INTEGER,
    patient_count INTEGER,
    validation_period_start DATE,
    validation_period_end DATE,
    validation_status TEXT NOT NULL,
    reviewer TEXT,
    reviewed_at TIMESTAMP,
    FOREIGN KEY (clinical_ai_system_id) REFERENCES clinical_ai_system_registry(clinical_ai_system_id)
);

CREATE TABLE IF NOT EXISTS clinical_ai_metric (
    metric_id TEXT PRIMARY KEY,
    validation_study_id TEXT,
    clinical_ai_system_id TEXT NOT NULL,
    metric_name TEXT NOT NULL,
    metric_value REAL NOT NULL,
    threshold_value REAL,
    subgroup_name TEXT,
    subgroup_value TEXT,
    metric_status TEXT NOT NULL,
    measured_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (validation_study_id) REFERENCES clinical_validation_study(validation_study_id),
    FOREIGN KEY (clinical_ai_system_id) REFERENCES clinical_ai_system_registry(clinical_ai_system_id)
);

CREATE TABLE IF NOT EXISTS clinical_prediction_log (
    prediction_id TEXT PRIMARY KEY,
    clinical_ai_system_id TEXT NOT NULL,
    patient_case_hash TEXT NOT NULL,
    site TEXT,
    unit TEXT,
    model_version TEXT NOT NULL,
    predicted_probability REAL,
    predicted_label TEXT,
    decision_threshold REAL,
    action_triggered TEXT,
    human_review_recommended INTEGER DEFAULT 0,
    predicted_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (clinical_ai_system_id) REFERENCES clinical_ai_system_registry(clinical_ai_system_id)
);

CREATE TABLE IF NOT EXISTS clinical_outcome_label (
    outcome_label_id TEXT PRIMARY KEY,
    prediction_id TEXT NOT NULL,
    outcome_name TEXT NOT NULL,
    outcome_value TEXT NOT NULL,
    label_source TEXT,
    label_quality_score REAL,
    observed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (prediction_id) REFERENCES clinical_prediction_log(prediction_id)
);

CREATE TABLE IF NOT EXISTS clinical_subgroup_review (
    subgroup_review_id TEXT PRIMARY KEY,
    clinical_ai_system_id TEXT NOT NULL,
    subgroup_name TEXT NOT NULL,
    subgroup_value TEXT NOT NULL,
    cases INTEGER NOT NULL,
    sensitivity REAL,
    specificity REAL,
    calibration_error REAL,
    alert_rate REAL,
    false_negative_rate REAL,
    review_status TEXT NOT NULL,
    reviewer TEXT,
    reviewed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (clinical_ai_system_id) REFERENCES clinical_ai_system_registry(clinical_ai_system_id)
);

CREATE TABLE IF NOT EXISTS clinical_ai_monitoring_signal (
    monitoring_signal_id TEXT PRIMARY KEY,
    clinical_ai_system_id TEXT NOT NULL,
    signal_name TEXT NOT NULL,
    signal_value REAL NOT NULL,
    signal_category TEXT NOT NULL,
    warning_threshold REAL,
    action_threshold REAL,
    signal_status TEXT NOT NULL,
    measured_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (clinical_ai_system_id) REFERENCES clinical_ai_system_registry(clinical_ai_system_id)
);

CREATE TABLE IF NOT EXISTS clinical_ai_incident (
    incident_id TEXT PRIMARY KEY,
    clinical_ai_system_id TEXT NOT NULL,
    incident_type TEXT NOT NULL,
    severity TEXT NOT NULL,
    incident_status TEXT NOT NULL,
    description TEXT NOT NULL,
    patient_safety_review_required INTEGER DEFAULT 1,
    remediation_summary TEXT,
    detected_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP,
    FOREIGN KEY (clinical_ai_system_id) REFERENCES clinical_ai_system_registry(clinical_ai_system_id)
);

CREATE TABLE IF NOT EXISTS clinical_ai_change_control (
    change_control_id TEXT PRIMARY KEY,
    clinical_ai_system_id TEXT NOT NULL,
    from_model_version TEXT NOT NULL,
    to_model_version TEXT NOT NULL,
    change_type TEXT NOT NULL,
    change_rationale TEXT NOT NULL,
    validation_required INTEGER DEFAULT 1,
    approval_status TEXT NOT NULL,
    approved_by TEXT,
    approved_at TIMESTAMP,
    FOREIGN KEY (clinical_ai_system_id) REFERENCES clinical_ai_system_registry(clinical_ai_system_id)
);

CREATE TABLE IF NOT EXISTS clinical_ai_governance_review (
    governance_review_id TEXT PRIMARY KEY,
    clinical_ai_system_id TEXT NOT NULL,
    review_type TEXT NOT NULL,
    reviewer TEXT NOT NULL,
    review_date DATE NOT NULL,
    decision TEXT NOT NULL,
    decision_rationale TEXT NOT NULL,
    required_actions TEXT,
    next_review_date DATE,
    FOREIGN KEY (clinical_ai_system_id) REFERENCES clinical_ai_system_registry(clinical_ai_system_id)
);

CREATE INDEX IF NOT EXISTS idx_clinical_ai_system_status
ON clinical_ai_system_registry(system_type, deployment_status, regulatory_status);

CREATE INDEX IF NOT EXISTS idx_clinical_metric_system_status
ON clinical_ai_metric(clinical_ai_system_id, metric_name, metric_status);

CREATE INDEX IF NOT EXISTS idx_prediction_log_system_time
ON clinical_prediction_log(clinical_ai_system_id, predicted_at);

CREATE INDEX IF NOT EXISTS idx_subgroup_review_system_status
ON clinical_subgroup_review(clinical_ai_system_id, review_status);

CREATE INDEX IF NOT EXISTS idx_monitoring_signal_status
ON clinical_ai_monitoring_signal(clinical_ai_system_id, signal_status, signal_category);

CREATE VIEW IF NOT EXISTS v_clinical_ai_systems_requiring_review AS
SELECT
    s.clinical_ai_system_id,
    s.system_name,
    s.system_version,
    s.system_type,
    s.deployment_status,
    m.signal_name,
    m.signal_value,
    m.signal_status
FROM clinical_ai_system_registry s
LEFT JOIN clinical_ai_monitoring_signal m
    ON s.clinical_ai_system_id = m.clinical_ai_system_id
WHERE s.deployment_status IN ('review_required', 'suspended', 'restricted')
   OR m.signal_status IN ('warning', 'action', 'incident');

CREATE VIEW IF NOT EXISTS v_open_clinical_ai_incidents AS
SELECT
    s.system_name,
    s.system_version,
    i.incident_id,
    i.incident_type,
    i.severity,
    i.incident_status,
    i.patient_safety_review_required,
    i.detected_at
FROM clinical_ai_incident i
JOIN clinical_ai_system_registry s
    ON i.clinical_ai_system_id = s.clinical_ai_system_id
WHERE i.incident_status IN ('open', 'investigating', 'requires_action');
