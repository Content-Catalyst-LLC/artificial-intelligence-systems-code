-- Advanced AI Safety and System Reliability Schema
--
-- This schema supports lifecycle governance for deployed AI systems:
-- model registry, data lineage, feature contracts, inference logs,
-- monitoring metrics, alert rules, incidents, human review, change control,
-- assurance evidence, and governance review.

CREATE TABLE IF NOT EXISTS ai_system (
    system_id TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    domain TEXT NOT NULL,
    intended_use TEXT NOT NULL,
    prohibited_uses TEXT,
    risk_classification TEXT NOT NULL,
    system_owner TEXT NOT NULL,
    business_owner TEXT,
    technical_owner TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    retired_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ai_model_version (
    model_version_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    model_name TEXT NOT NULL,
    model_version TEXT NOT NULL,
    model_family TEXT,
    training_data_window_start DATE,
    training_data_window_end DATE,
    validation_summary TEXT,
    calibration_summary TEXT,
    robustness_summary TEXT,
    known_limitations TEXT,
    approval_status TEXT NOT NULL,
    approved_by TEXT,
    approved_at TIMESTAMP,
    deployed_at TIMESTAMP,
    retired_at TIMESTAMP,
    FOREIGN KEY (system_id) REFERENCES ai_system(system_id)
);

CREATE TABLE IF NOT EXISTS ai_dataset_lineage (
    dataset_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    dataset_name TEXT NOT NULL,
    dataset_role TEXT NOT NULL,
    source_system TEXT,
    collection_method TEXT,
    measurement_limitations TEXT,
    known_biases TEXT,
    update_frequency TEXT,
    data_owner TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (system_id) REFERENCES ai_system(system_id)
);

CREATE TABLE IF NOT EXISTS ai_feature_contract (
    feature_contract_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    feature_name TEXT NOT NULL,
    data_type TEXT NOT NULL,
    unit TEXT,
    minimum_allowed REAL,
    maximum_allowed REAL,
    allowed_categories TEXT,
    missing_allowed INTEGER NOT NULL DEFAULT 0,
    semantic_definition TEXT NOT NULL,
    validation_rule TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (system_id) REFERENCES ai_system(system_id)
);

CREATE TABLE IF NOT EXISTS ai_inference_log (
    inference_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    model_version_id TEXT NOT NULL,
    inference_timestamp TIMESTAMP NOT NULL,
    input_reference TEXT,
    prediction_score REAL,
    prediction_label TEXT,
    uncertainty_score REAL,
    decision_threshold REAL,
    review_required INTEGER NOT NULL DEFAULT 0,
    automated_action_taken INTEGER NOT NULL DEFAULT 0,
    human_override INTEGER NOT NULL DEFAULT 0,
    observed_outcome REAL,
    outcome_observed_at TIMESTAMP,
    subgroup_key TEXT,
    deployment_context TEXT,
    FOREIGN KEY (system_id) REFERENCES ai_system(system_id),
    FOREIGN KEY (model_version_id) REFERENCES ai_model_version(model_version_id)
);

CREATE TABLE IF NOT EXISTS ai_monitoring_metric (
    metric_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    model_version_id TEXT,
    metric_name TEXT NOT NULL,
    metric_value REAL NOT NULL,
    metric_unit TEXT,
    metric_window_start TIMESTAMP NOT NULL,
    metric_window_end TIMESTAMP NOT NULL,
    threshold_warning REAL,
    threshold_action REAL,
    threshold_status TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (system_id) REFERENCES ai_system(system_id),
    FOREIGN KEY (model_version_id) REFERENCES ai_model_version(model_version_id)
);

CREATE TABLE IF NOT EXISTS ai_alert_rule (
    alert_rule_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    metric_name TEXT NOT NULL,
    warning_condition TEXT NOT NULL,
    action_condition TEXT NOT NULL,
    severity_if_triggered TEXT NOT NULL,
    owner_team TEXT NOT NULL,
    enabled INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (system_id) REFERENCES ai_system(system_id)
);

CREATE TABLE IF NOT EXISTS ai_alert_event (
    alert_event_id TEXT PRIMARY KEY,
    alert_rule_id TEXT NOT NULL,
    system_id TEXT NOT NULL,
    metric_id TEXT,
    alert_timestamp TIMESTAMP NOT NULL,
    severity TEXT NOT NULL,
    alert_status TEXT NOT NULL,
    description TEXT NOT NULL,
    acknowledged_by TEXT,
    acknowledged_at TIMESTAMP,
    resolved_at TIMESTAMP,
    FOREIGN KEY (alert_rule_id) REFERENCES ai_alert_rule(alert_rule_id),
    FOREIGN KEY (system_id) REFERENCES ai_system(system_id),
    FOREIGN KEY (metric_id) REFERENCES ai_monitoring_metric(metric_id)
);

CREATE TABLE IF NOT EXISTS ai_safety_incident (
    incident_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    model_version_id TEXT,
    incident_type TEXT NOT NULL,
    severity TEXT NOT NULL,
    incident_status TEXT NOT NULL,
    detected_at TIMESTAMP NOT NULL,
    contained_at TIMESTAMP,
    resolved_at TIMESTAMP,
    description TEXT NOT NULL,
    affected_users_or_assets TEXT,
    suspected_root_cause TEXT,
    confirmed_root_cause TEXT,
    remediation_summary TEXT,
    rollback_required INTEGER NOT NULL DEFAULT 0,
    external_reporting_required INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (system_id) REFERENCES ai_system(system_id),
    FOREIGN KEY (model_version_id) REFERENCES ai_model_version(model_version_id)
);

CREATE TABLE IF NOT EXISTS ai_human_review (
    review_event_id TEXT PRIMARY KEY,
    inference_id TEXT NOT NULL,
    reviewer_id TEXT NOT NULL,
    review_timestamp TIMESTAMP NOT NULL,
    model_recommendation TEXT,
    human_decision TEXT NOT NULL,
    override_reason TEXT,
    escalation_required INTEGER NOT NULL DEFAULT 0,
    escalation_reason TEXT,
    FOREIGN KEY (inference_id) REFERENCES ai_inference_log(inference_id)
);

CREATE TABLE IF NOT EXISTS ai_model_change_request (
    change_request_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    current_model_version_id TEXT,
    proposed_model_version_id TEXT,
    change_type TEXT NOT NULL,
    change_reason TEXT NOT NULL,
    expected_risk_change TEXT,
    validation_evidence_uri TEXT,
    requested_by TEXT NOT NULL,
    requested_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    decision TEXT,
    decided_by TEXT,
    decided_at TIMESTAMP,
    decision_rationale TEXT,
    FOREIGN KEY (system_id) REFERENCES ai_system(system_id),
    FOREIGN KEY (current_model_version_id) REFERENCES ai_model_version(model_version_id),
    FOREIGN KEY (proposed_model_version_id) REFERENCES ai_model_version(model_version_id)
);

CREATE TABLE IF NOT EXISTS ai_assurance_evidence (
    evidence_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    model_version_id TEXT,
    evidence_type TEXT NOT NULL,
    evidence_uri TEXT NOT NULL,
    evidence_summary TEXT,
    evidence_owner TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    FOREIGN KEY (system_id) REFERENCES ai_system(system_id),
    FOREIGN KEY (model_version_id) REFERENCES ai_model_version(model_version_id)
);

CREATE TABLE IF NOT EXISTS ai_governance_review (
    governance_review_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    model_version_id TEXT,
    review_type TEXT NOT NULL,
    review_date DATE NOT NULL,
    reviewer TEXT NOT NULL,
    decision TEXT NOT NULL,
    decision_rationale TEXT NOT NULL,
    required_actions TEXT,
    next_review_date DATE,
    FOREIGN KEY (system_id) REFERENCES ai_system(system_id),
    FOREIGN KEY (model_version_id) REFERENCES ai_model_version(model_version_id)
);

CREATE INDEX IF NOT EXISTS idx_ai_inference_log_system_time
ON ai_inference_log(system_id, inference_timestamp);

CREATE INDEX IF NOT EXISTS idx_ai_monitoring_metric_system_window
ON ai_monitoring_metric(system_id, metric_window_start, metric_window_end);

CREATE INDEX IF NOT EXISTS idx_ai_incident_system_status
ON ai_safety_incident(system_id, incident_status);

CREATE INDEX IF NOT EXISTS idx_ai_alert_event_status
ON ai_alert_event(system_id, alert_status, severity);

CREATE VIEW IF NOT EXISTS v_open_safety_incidents AS
SELECT
    i.incident_id,
    s.system_name,
    i.incident_type,
    i.severity,
    i.incident_status,
    i.detected_at,
    i.description,
    i.rollback_required,
    i.external_reporting_required
FROM ai_safety_incident i
JOIN ai_system s
    ON i.system_id = s.system_id
WHERE i.incident_status NOT IN ('resolved', 'closed');

CREATE VIEW IF NOT EXISTS v_latest_metric_status AS
SELECT
    m.system_id,
    s.system_name,
    m.model_version_id,
    m.metric_name,
    m.metric_value,
    m.threshold_warning,
    m.threshold_action,
    m.threshold_status,
    m.metric_window_start,
    m.metric_window_end,
    m.created_at
FROM ai_monitoring_metric m
JOIN ai_system s
    ON m.system_id = s.system_id
WHERE m.created_at = (
    SELECT MAX(m2.created_at)
    FROM ai_monitoring_metric m2
    WHERE m2.system_id = m.system_id
      AND m2.metric_name = m.metric_name
);

CREATE VIEW IF NOT EXISTS v_high_risk_inference_events AS
SELECT
    inference_id,
    system_id,
    model_version_id,
    inference_timestamp,
    prediction_score,
    uncertainty_score,
    review_required,
    automated_action_taken,
    human_override,
    subgroup_key,
    deployment_context
FROM ai_inference_log
WHERE uncertainty_score >= 0.30
   OR review_required = 1
   OR human_override = 1;

CREATE VIEW IF NOT EXISTS v_governance_evidence_inventory AS
SELECT
    s.system_id,
    s.system_name,
    s.risk_classification,
    e.evidence_type,
    COUNT(e.evidence_id) AS evidence_count,
    MAX(e.created_at) AS latest_evidence_at
FROM ai_system s
LEFT JOIN ai_assurance_evidence e
    ON s.system_id = e.system_id
GROUP BY
    s.system_id,
    s.system_name,
    s.risk_classification,
    e.evidence_type;
