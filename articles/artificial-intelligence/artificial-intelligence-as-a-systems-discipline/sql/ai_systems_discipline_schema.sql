-- Artificial Intelligence as a Systems Discipline
-- SQL schema for AI system inventories, lifecycle stages, governance evidence,
-- monitoring records, incidents, assurance artifacts, and retirement decisions.

CREATE TABLE IF NOT EXISTS ai_system (
    system_id TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    domain TEXT NOT NULL,
    intended_use TEXT NOT NULL,
    prohibited_use TEXT,
    risk_tier TEXT NOT NULL,
    system_owner TEXT NOT NULL,
    lifecycle_status TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    retired_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ai_system_component (
    component_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    component_type TEXT NOT NULL,
    component_name TEXT NOT NULL,
    version TEXT,
    owner TEXT,
    description TEXT,
    FOREIGN KEY (system_id) REFERENCES ai_system(system_id)
);

CREATE TABLE IF NOT EXISTS ai_lifecycle_stage (
    lifecycle_stage_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    stage_name TEXT NOT NULL,
    stage_status TEXT NOT NULL,
    responsible_party TEXT NOT NULL,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    evidence_uri TEXT,
    FOREIGN KEY (system_id) REFERENCES ai_system(system_id)
);

CREATE TABLE IF NOT EXISTS ai_system_metric (
    metric_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    metric_name TEXT NOT NULL,
    metric_category TEXT NOT NULL,
    metric_value REAL NOT NULL,
    threshold_warning REAL,
    threshold_action REAL,
    measured_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (system_id) REFERENCES ai_system(system_id)
);

CREATE TABLE IF NOT EXISTS ai_risk_record (
    risk_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    risk_category TEXT NOT NULL,
    risk_description TEXT NOT NULL,
    likelihood_score REAL,
    impact_score REAL,
    mitigation_summary TEXT,
    residual_risk_score REAL,
    review_status TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (system_id) REFERENCES ai_system(system_id)
);

CREATE TABLE IF NOT EXISTS ai_governance_review (
    review_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    review_type TEXT NOT NULL,
    reviewer TEXT NOT NULL,
    review_date DATE NOT NULL,
    decision TEXT NOT NULL,
    decision_rationale TEXT NOT NULL,
    required_actions TEXT,
    next_review_date DATE,
    FOREIGN KEY (system_id) REFERENCES ai_system(system_id)
);

CREATE TABLE IF NOT EXISTS ai_monitoring_record (
    monitoring_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    monitoring_type TEXT NOT NULL,
    signal_name TEXT NOT NULL,
    signal_value REAL,
    alert_status TEXT,
    observed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    FOREIGN KEY (system_id) REFERENCES ai_system(system_id)
);

CREATE TABLE IF NOT EXISTS ai_incident (
    incident_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    incident_type TEXT NOT NULL,
    severity TEXT NOT NULL,
    incident_status TEXT NOT NULL,
    description TEXT NOT NULL,
    detected_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP,
    remediation_summary TEXT,
    FOREIGN KEY (system_id) REFERENCES ai_system(system_id)
);

CREATE TABLE IF NOT EXISTS ai_assurance_artifact (
    artifact_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    artifact_type TEXT NOT NULL,
    artifact_name TEXT NOT NULL,
    artifact_uri TEXT,
    artifact_status TEXT NOT NULL,
    created_by TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (system_id) REFERENCES ai_system(system_id)
);

CREATE TABLE IF NOT EXISTS ai_retirement_decision (
    retirement_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    decision_date DATE NOT NULL,
    decision_maker TEXT NOT NULL,
    retirement_reason TEXT NOT NULL,
    data_retention_plan TEXT,
    replacement_system_id TEXT,
    final_status TEXT NOT NULL,
    FOREIGN KEY (system_id) REFERENCES ai_system(system_id)
);

CREATE INDEX IF NOT EXISTS idx_ai_system_domain_status
ON ai_system(domain, lifecycle_status);

CREATE INDEX IF NOT EXISTS idx_ai_metric_system_time
ON ai_system_metric(system_id, measured_at);

CREATE INDEX IF NOT EXISTS idx_ai_risk_system_status
ON ai_risk_record(system_id, review_status);

CREATE INDEX IF NOT EXISTS idx_ai_incident_status
ON ai_incident(system_id, incident_status, severity);

CREATE VIEW IF NOT EXISTS v_ai_system_governance_dashboard AS
SELECT
    s.system_id,
    s.system_name,
    s.domain,
    s.risk_tier,
    s.lifecycle_status,
    COUNT(DISTINCT r.risk_id) AS open_risk_records,
    COUNT(DISTINCT i.incident_id) AS open_incidents,
    COUNT(DISTINCT a.artifact_id) AS assurance_artifacts
FROM ai_system s
LEFT JOIN ai_risk_record r
    ON s.system_id = r.system_id
    AND r.review_status NOT IN ('closed', 'accepted')
LEFT JOIN ai_incident i
    ON s.system_id = i.system_id
    AND i.incident_status NOT IN ('resolved', 'closed')
LEFT JOIN ai_assurance_artifact a
    ON s.system_id = a.system_id
GROUP BY
    s.system_id,
    s.system_name,
    s.domain,
    s.risk_tier,
    s.lifecycle_status;

CREATE VIEW IF NOT EXISTS v_ai_systems_requiring_review AS
SELECT
    s.system_id,
    s.system_name,
    s.domain,
    s.risk_tier,
    s.lifecycle_status,
    r.risk_category,
    r.residual_risk_score,
    r.review_status
FROM ai_system s
JOIN ai_risk_record r
    ON s.system_id = r.system_id
WHERE r.residual_risk_score >= 0.45
   OR r.review_status IN ('open', 'requires_action');
