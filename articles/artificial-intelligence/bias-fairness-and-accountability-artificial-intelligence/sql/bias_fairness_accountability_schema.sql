-- Bias, Fairness, and Accountability in AI Metadata Schema

CREATE TABLE IF NOT EXISTS ai_systems (
    system_id TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    system_purpose TEXT NOT NULL,
    owner_team TEXT NOT NULL,
    deployment_status TEXT CHECK(deployment_status IN ('proposed', 'development', 'pilot', 'production', 'paused', 'retired')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS fairness_audits (
    audit_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    audit_date DATE NOT NULL,
    audit_scope TEXT NOT NULL,
    fairness_definition TEXT,
    protected_attributes_reviewed TEXT,
    threshold_policy TEXT,
    reviewer TEXT NOT NULL,
    review_status TEXT CHECK(review_status IN ('draft', 'approved', 'requires_revision', 'rejected')),
    FOREIGN KEY(system_id) REFERENCES ai_systems(system_id)
);

CREATE TABLE IF NOT EXISTS datasets (
    dataset_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    dataset_name TEXT NOT NULL,
    dataset_role TEXT CHECK(dataset_role IN ('train', 'validation', 'test', 'monitoring')),
    data_source TEXT NOT NULL,
    label_source TEXT,
    known_bias_notes TEXT,
    protected_attribute_availability TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(system_id) REFERENCES ai_systems(system_id)
);

CREATE TABLE IF NOT EXISTS fairness_metrics (
    metric_id TEXT PRIMARY KEY,
    audit_id TEXT NOT NULL,
    group_name TEXT NOT NULL,
    group_value TEXT NOT NULL,
    sample_size INTEGER,
    base_rate REAL,
    selection_rate REAL,
    true_positive_rate REAL,
    false_positive_rate REAL,
    false_negative_rate REAL,
    positive_predictive_value REAL,
    calibration_error REAL,
    notes TEXT,
    FOREIGN KEY(audit_id) REFERENCES fairness_audits(audit_id)
);

CREATE TABLE IF NOT EXISTS fairness_gaps (
    gap_id TEXT PRIMARY KEY,
    audit_id TEXT NOT NULL,
    metric_name TEXT NOT NULL,
    group_a TEXT,
    group_b TEXT,
    gap_value REAL,
    approved_tolerance REAL,
    review_required BOOLEAN DEFAULT FALSE,
    FOREIGN KEY(audit_id) REFERENCES fairness_audits(audit_id)
);

CREATE TABLE IF NOT EXISTS mitigation_actions (
    mitigation_id TEXT PRIMARY KEY,
    audit_id TEXT NOT NULL,
    mitigation_stage TEXT CHECK(mitigation_stage IN ('pre_processing', 'in_processing', 'post_processing', 'governance', 'deployment_constraint')),
    action_description TEXT NOT NULL,
    owner TEXT NOT NULL,
    due_date DATE,
    status TEXT CHECK(status IN ('proposed', 'in_progress', 'complete', 'rejected', 'deferred')),
    FOREIGN KEY(audit_id) REFERENCES fairness_audits(audit_id)
);

CREATE TABLE IF NOT EXISTS accountability_reviews (
    review_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    review_date DATE NOT NULL,
    decision_context TEXT NOT NULL,
    explanation_available BOOLEAN DEFAULT FALSE,
    human_oversight_available BOOLEAN DEFAULT FALSE,
    contestation_process_available BOOLEAN DEFAULT FALSE,
    remedy_process_available BOOLEAN DEFAULT FALSE,
    reviewer TEXT NOT NULL,
    findings TEXT,
    FOREIGN KEY(system_id) REFERENCES ai_systems(system_id)
);

CREATE TABLE IF NOT EXISTS fairness_monitoring_events (
    monitoring_event_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    event_date DATE NOT NULL,
    metric_name TEXT NOT NULL,
    metric_value REAL NOT NULL,
    threshold_value REAL,
    alert_level TEXT CHECK(alert_level IN ('none', 'low', 'moderate', 'high', 'critical')),
    remediation_status TEXT,
    FOREIGN KEY(system_id) REFERENCES ai_systems(system_id)
);
