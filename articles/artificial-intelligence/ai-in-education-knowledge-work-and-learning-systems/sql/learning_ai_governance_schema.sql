-- AI in Education, Knowledge Work, and Learning Systems
-- SQL schema for education AI systems, intended use, learning events,
-- assessment evidence, AI-use disclosure, privacy review, accessibility review,
-- subgroup review, incidents, change control, and governance review.

CREATE TABLE IF NOT EXISTS education_ai_system_registry (
    education_ai_system_id TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    system_version TEXT NOT NULL,
    system_type TEXT NOT NULL,
    intended_use TEXT NOT NULL,
    prohibited_use TEXT,
    educational_owner TEXT NOT NULL,
    technical_owner TEXT NOT NULL,
    deployment_status TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS education_ai_intended_use (
    intended_use_id TEXT PRIMARY KEY,
    education_ai_system_id TEXT NOT NULL,
    learning_context TEXT NOT NULL,
    user_group TEXT NOT NULL,
    learning_goal TEXT NOT NULL,
    ai_role TEXT NOT NULL,
    human_oversight_required INTEGER DEFAULT 1,
    disclosure_required INTEGER DEFAULT 1,
    FOREIGN KEY (education_ai_system_id) REFERENCES education_ai_system_registry(education_ai_system_id)
);

CREATE TABLE IF NOT EXISTS learning_ai_event_log (
    learning_event_id TEXT PRIMARY KEY,
    education_ai_system_id TEXT NOT NULL,
    learner_hash TEXT NOT NULL,
    course_or_workflow TEXT,
    event_type TEXT NOT NULL,
    ai_assistance_type TEXT,
    ai_usage_intensity REAL,
    teacher_or_supervisor_reviewed INTEGER DEFAULT 0,
    event_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (education_ai_system_id) REFERENCES education_ai_system_registry(education_ai_system_id)
);

CREATE TABLE IF NOT EXISTS learning_outcome_metric (
    outcome_metric_id TEXT PRIMARY KEY,
    education_ai_system_id TEXT NOT NULL,
    cohort_or_context TEXT NOT NULL,
    metric_name TEXT NOT NULL,
    metric_value REAL NOT NULL,
    baseline_value REAL,
    independent_transfer_value REAL,
    metric_status TEXT NOT NULL,
    measured_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (education_ai_system_id) REFERENCES education_ai_system_registry(education_ai_system_id)
);

CREATE TABLE IF NOT EXISTS assessment_evidence_record (
    assessment_evidence_id TEXT PRIMARY KEY,
    education_ai_system_id TEXT NOT NULL,
    assessment_name TEXT NOT NULL,
    intended_construct TEXT NOT NULL,
    ai_policy TEXT NOT NULL,
    process_evidence_required INTEGER DEFAULT 0,
    oral_or_live_defense_required INTEGER DEFAULT 0,
    assessment_validity_review_status TEXT NOT NULL,
    reviewed_at TIMESTAMP,
    FOREIGN KEY (education_ai_system_id) REFERENCES education_ai_system_registry(education_ai_system_id)
);

CREATE TABLE IF NOT EXISTS ai_use_disclosure (
    disclosure_id TEXT PRIMARY KEY,
    education_ai_system_id TEXT NOT NULL,
    learner_or_worker_hash TEXT NOT NULL,
    activity_name TEXT NOT NULL,
    ai_use_type TEXT NOT NULL,
    disclosure_text TEXT,
    reviewed_status TEXT NOT NULL,
    disclosed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (education_ai_system_id) REFERENCES education_ai_system_registry(education_ai_system_id)
);

CREATE TABLE IF NOT EXISTS education_ai_privacy_review (
    privacy_review_id TEXT PRIMARY KEY,
    education_ai_system_id TEXT NOT NULL,
    data_category TEXT NOT NULL,
    vendor_or_platform TEXT,
    data_retention_policy TEXT,
    training_on_user_data_allowed INTEGER DEFAULT 0,
    access_control_status TEXT NOT NULL,
    privacy_risk_value REAL,
    review_decision TEXT NOT NULL,
    reviewer TEXT NOT NULL,
    reviewed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (education_ai_system_id) REFERENCES education_ai_system_registry(education_ai_system_id)
);

CREATE TABLE IF NOT EXISTS education_ai_accessibility_review (
    accessibility_review_id TEXT PRIMARY KEY,
    education_ai_system_id TEXT NOT NULL,
    accessibility_feature TEXT NOT NULL,
    learner_context TEXT,
    quality_score REAL,
    review_status TEXT NOT NULL,
    reviewer TEXT,
    reviewed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (education_ai_system_id) REFERENCES education_ai_system_registry(education_ai_system_id)
);

CREATE TABLE IF NOT EXISTS education_ai_subgroup_review (
    subgroup_review_id TEXT PRIMARY KEY,
    education_ai_system_id TEXT NOT NULL,
    subgroup_name TEXT NOT NULL,
    subgroup_value TEXT NOT NULL,
    records INTEGER NOT NULL,
    learning_gain REAL,
    independent_transfer REAL,
    feedback_quality REAL,
    assistance_gap REAL,
    governance_risk REAL,
    review_status TEXT NOT NULL,
    reviewer TEXT,
    reviewed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (education_ai_system_id) REFERENCES education_ai_system_registry(education_ai_system_id)
);

CREATE TABLE IF NOT EXISTS education_ai_monitoring_signal (
    monitoring_signal_id TEXT PRIMARY KEY,
    education_ai_system_id TEXT NOT NULL,
    signal_name TEXT NOT NULL,
    signal_value REAL NOT NULL,
    signal_category TEXT NOT NULL,
    warning_threshold REAL,
    action_threshold REAL,
    signal_status TEXT NOT NULL,
    measured_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (education_ai_system_id) REFERENCES education_ai_system_registry(education_ai_system_id)
);

CREATE TABLE IF NOT EXISTS education_ai_incident (
    incident_id TEXT PRIMARY KEY,
    education_ai_system_id TEXT NOT NULL,
    incident_type TEXT NOT NULL,
    severity TEXT NOT NULL,
    incident_status TEXT NOT NULL,
    description TEXT NOT NULL,
    learner_or_worker_impact_review_required INTEGER DEFAULT 1,
    remediation_summary TEXT,
    detected_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP,
    FOREIGN KEY (education_ai_system_id) REFERENCES education_ai_system_registry(education_ai_system_id)
);

CREATE TABLE IF NOT EXISTS education_ai_change_control (
    change_control_id TEXT PRIMARY KEY,
    education_ai_system_id TEXT NOT NULL,
    from_system_version TEXT NOT NULL,
    to_system_version TEXT NOT NULL,
    change_type TEXT NOT NULL,
    change_rationale TEXT NOT NULL,
    learning_impact_review_required INTEGER DEFAULT 1,
    privacy_review_required INTEGER DEFAULT 1,
    approval_status TEXT NOT NULL,
    approved_by TEXT,
    approved_at TIMESTAMP,
    FOREIGN KEY (education_ai_system_id) REFERENCES education_ai_system_registry(education_ai_system_id)
);

CREATE TABLE IF NOT EXISTS education_ai_governance_review (
    governance_review_id TEXT PRIMARY KEY,
    education_ai_system_id TEXT NOT NULL,
    review_type TEXT NOT NULL,
    reviewer TEXT NOT NULL,
    review_date DATE NOT NULL,
    decision TEXT NOT NULL,
    decision_rationale TEXT NOT NULL,
    required_actions TEXT,
    next_review_date DATE,
    FOREIGN KEY (education_ai_system_id) REFERENCES education_ai_system_registry(education_ai_system_id)
);

CREATE INDEX IF NOT EXISTS idx_education_ai_system_status
ON education_ai_system_registry(system_type, deployment_status);

CREATE INDEX IF NOT EXISTS idx_learning_event_system_time
ON learning_ai_event_log(education_ai_system_id, event_timestamp);

CREATE INDEX IF NOT EXISTS idx_learning_metric_system_status
ON learning_outcome_metric(education_ai_system_id, metric_name, metric_status);

CREATE INDEX IF NOT EXISTS idx_assessment_evidence_status
ON assessment_evidence_record(education_ai_system_id, assessment_validity_review_status);

CREATE INDEX IF NOT EXISTS idx_subgroup_review_system_status
ON education_ai_subgroup_review(education_ai_system_id, review_status);

CREATE INDEX IF NOT EXISTS idx_monitoring_signal_system_status
ON education_ai_monitoring_signal(education_ai_system_id, signal_status, signal_category);

CREATE VIEW IF NOT EXISTS v_learning_systems_requiring_review AS
SELECT
    s.education_ai_system_id,
    s.system_name,
    s.system_version,
    s.system_type,
    s.deployment_status,
    m.signal_name,
    m.signal_value,
    m.signal_status
FROM education_ai_system_registry s
LEFT JOIN education_ai_monitoring_signal m
    ON s.education_ai_system_id = m.education_ai_system_id
WHERE s.deployment_status IN ('review_required', 'suspended', 'restricted')
   OR m.signal_status IN ('warning', 'action', 'incident');

CREATE VIEW IF NOT EXISTS v_assessments_requiring_validity_review AS
SELECT
    s.system_name,
    a.assessment_name,
    a.intended_construct,
    a.ai_policy,
    a.process_evidence_required,
    a.oral_or_live_defense_required,
    a.assessment_validity_review_status
FROM assessment_evidence_record a
JOIN education_ai_system_registry s
    ON a.education_ai_system_id = s.education_ai_system_id
WHERE a.assessment_validity_review_status IN ('review_required', 'restricted', 'invalid');
