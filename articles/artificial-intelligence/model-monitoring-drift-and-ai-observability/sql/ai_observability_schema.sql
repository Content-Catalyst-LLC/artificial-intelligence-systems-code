-- Model Monitoring, Drift, and AI Observability
-- SQL schema for model registries, feature monitoring, prediction monitoring,
-- labels, drift metrics, incidents, retraining reviews, rollback records,
-- and governance review.

CREATE TABLE IF NOT EXISTS ai_model_registry (
    model_id TEXT PRIMARY KEY,
    model_name TEXT NOT NULL,
    model_version TEXT NOT NULL,
    model_type TEXT NOT NULL,
    intended_use TEXT NOT NULL,
    owner TEXT NOT NULL,
    deployment_status TEXT NOT NULL,
    deployed_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS monitoring_reference_dataset (
    reference_dataset_id TEXT PRIMARY KEY,
    model_id TEXT NOT NULL,
    dataset_name TEXT NOT NULL,
    dataset_version TEXT NOT NULL,
    reference_period_start DATE,
    reference_period_end DATE,
    checksum TEXT,
    approved_by TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (model_id) REFERENCES ai_model_registry(model_id)
);

CREATE TABLE IF NOT EXISTS production_batch (
    production_batch_id TEXT PRIMARY KEY,
    model_id TEXT NOT NULL,
    batch_start TIMESTAMP NOT NULL,
    batch_end TIMESTAMP NOT NULL,
    record_count INTEGER NOT NULL,
    source_system TEXT,
    pipeline_version TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (model_id) REFERENCES ai_model_registry(model_id)
);

CREATE TABLE IF NOT EXISTS feature_monitoring_metric (
    feature_metric_id TEXT PRIMARY KEY,
    production_batch_id TEXT NOT NULL,
    feature_name TEXT NOT NULL,
    metric_name TEXT NOT NULL,
    metric_value REAL NOT NULL,
    warning_threshold REAL,
    action_threshold REAL,
    metric_status TEXT NOT NULL,
    measured_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (production_batch_id) REFERENCES production_batch(production_batch_id)
);

CREATE TABLE IF NOT EXISTS prediction_monitoring_metric (
    prediction_metric_id TEXT PRIMARY KEY,
    production_batch_id TEXT NOT NULL,
    metric_name TEXT NOT NULL,
    metric_value REAL NOT NULL,
    warning_threshold REAL,
    action_threshold REAL,
    metric_status TEXT NOT NULL,
    measured_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (production_batch_id) REFERENCES production_batch(production_batch_id)
);

CREATE TABLE IF NOT EXISTS label_observation (
    label_observation_id TEXT PRIMARY KEY,
    production_batch_id TEXT NOT NULL,
    example_id_hash TEXT NOT NULL,
    predicted_value REAL,
    predicted_label TEXT,
    observed_label TEXT,
    label_observed_at TIMESTAMP,
    label_source TEXT,
    FOREIGN KEY (production_batch_id) REFERENCES production_batch(production_batch_id)
);

CREATE TABLE IF NOT EXISTS performance_monitoring_metric (
    performance_metric_id TEXT PRIMARY KEY,
    production_batch_id TEXT NOT NULL,
    metric_name TEXT NOT NULL,
    metric_value REAL NOT NULL,
    slice_name TEXT,
    slice_value TEXT,
    warning_threshold REAL,
    action_threshold REAL,
    metric_status TEXT NOT NULL,
    measured_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (production_batch_id) REFERENCES production_batch(production_batch_id)
);

CREATE TABLE IF NOT EXISTS ai_observability_signal (
    observability_signal_id TEXT PRIMARY KEY,
    model_id TEXT NOT NULL,
    production_batch_id TEXT,
    signal_name TEXT NOT NULL,
    signal_value REAL NOT NULL,
    signal_category TEXT NOT NULL,
    signal_status TEXT NOT NULL,
    owner TEXT,
    measured_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (model_id) REFERENCES ai_model_registry(model_id),
    FOREIGN KEY (production_batch_id) REFERENCES production_batch(production_batch_id)
);

CREATE TABLE IF NOT EXISTS monitoring_alert (
    alert_id TEXT PRIMARY KEY,
    model_id TEXT NOT NULL,
    production_batch_id TEXT,
    alert_level TEXT NOT NULL,
    alert_type TEXT NOT NULL,
    alert_status TEXT NOT NULL,
    alert_message TEXT NOT NULL,
    assigned_owner TEXT,
    opened_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP,
    resolution_summary TEXT,
    FOREIGN KEY (model_id) REFERENCES ai_model_registry(model_id),
    FOREIGN KEY (production_batch_id) REFERENCES production_batch(production_batch_id)
);

CREATE TABLE IF NOT EXISTS ai_incident_record (
    incident_id TEXT PRIMARY KEY,
    model_id TEXT NOT NULL,
    alert_id TEXT,
    incident_type TEXT NOT NULL,
    severity TEXT NOT NULL,
    incident_status TEXT NOT NULL,
    description TEXT NOT NULL,
    remediation_summary TEXT,
    detected_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP,
    FOREIGN KEY (model_id) REFERENCES ai_model_registry(model_id),
    FOREIGN KEY (alert_id) REFERENCES monitoring_alert(alert_id)
);

CREATE TABLE IF NOT EXISTS retraining_review (
    retraining_review_id TEXT PRIMARY KEY,
    model_id TEXT NOT NULL,
    trigger_signal TEXT NOT NULL,
    trigger_rationale TEXT NOT NULL,
    review_decision TEXT NOT NULL,
    decision_rationale TEXT NOT NULL,
    approved_by TEXT,
    reviewed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (model_id) REFERENCES ai_model_registry(model_id)
);

CREATE TABLE IF NOT EXISTS rollback_record (
    rollback_id TEXT PRIMARY KEY,
    model_id TEXT NOT NULL,
    from_model_version TEXT NOT NULL,
    to_model_version TEXT NOT NULL,
    rollback_reason TEXT NOT NULL,
    rollback_status TEXT NOT NULL,
    executed_by TEXT,
    executed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (model_id) REFERENCES ai_model_registry(model_id)
);

CREATE TABLE IF NOT EXISTS observability_governance_review (
    governance_review_id TEXT PRIMARY KEY,
    model_id TEXT NOT NULL,
    review_type TEXT NOT NULL,
    reviewer TEXT NOT NULL,
    review_date DATE NOT NULL,
    decision TEXT NOT NULL,
    decision_rationale TEXT NOT NULL,
    required_actions TEXT,
    next_review_date DATE,
    FOREIGN KEY (model_id) REFERENCES ai_model_registry(model_id)
);

CREATE INDEX IF NOT EXISTS idx_production_batch_model_time
ON production_batch(model_id, batch_start, batch_end);

CREATE INDEX IF NOT EXISTS idx_feature_metric_batch_status
ON feature_monitoring_metric(production_batch_id, metric_status);

CREATE INDEX IF NOT EXISTS idx_prediction_metric_batch_status
ON prediction_monitoring_metric(production_batch_id, metric_status);

CREATE INDEX IF NOT EXISTS idx_performance_metric_batch_slice
ON performance_monitoring_metric(production_batch_id, slice_name, slice_value);

CREATE INDEX IF NOT EXISTS idx_monitoring_alert_model_status
ON monitoring_alert(model_id, alert_status, alert_level);

CREATE VIEW IF NOT EXISTS v_open_ai_observability_alerts AS
SELECT
    a.alert_id,
    m.model_name,
    m.model_version,
    a.alert_level,
    a.alert_type,
    a.alert_status,
    a.alert_message,
    a.assigned_owner,
    a.opened_at
FROM monitoring_alert a
JOIN ai_model_registry m
    ON a.model_id = m.model_id
WHERE a.alert_status IN ('open', 'investigating', 'requires_action');

CREATE VIEW IF NOT EXISTS v_model_batches_requiring_review AS
SELECT
    pb.production_batch_id,
    m.model_name,
    m.model_version,
    pb.batch_start,
    pb.batch_end,
    COUNT(a.alert_id) AS open_alerts
FROM production_batch pb
JOIN ai_model_registry m
    ON pb.model_id = m.model_id
LEFT JOIN monitoring_alert a
    ON pb.production_batch_id = a.production_batch_id
   AND a.alert_status IN ('open', 'investigating', 'requires_action')
GROUP BY
    pb.production_batch_id,
    m.model_name,
    m.model_version,
    pb.batch_start,
    pb.batch_end
HAVING COUNT(a.alert_id) > 0;
