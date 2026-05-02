-- AI documentation governance schema.
-- This schema supports risk registers, model cards, system cards, audit evidence,
-- lifecycle traceability, approvals, incidents, corrective actions, and documentation reviews.
--
-- Do not store sensitive, personal, regulated, protected, confidential,
-- proprietary, incident-confidential, credential, legal, clinical, employment,
-- public-benefits, financial, student, or security-sensitive data without
-- appropriate controls.

CREATE TABLE ai_systems (
    system_id INTEGER PRIMARY KEY,
    system_name TEXT NOT NULL,
    purpose TEXT NOT NULL,
    owner_team TEXT NOT NULL,
    deployment_status TEXT NOT NULL,
    risk_level TEXT NOT NULL,
    vendor_name TEXT,
    model_or_service_name TEXT,
    model_version TEXT,
    created_at TEXT NOT NULL,
    last_updated TEXT NOT NULL
);

CREATE TABLE model_cards (
    model_card_id INTEGER PRIMARY KEY,
    system_id INTEGER NOT NULL,
    model_name TEXT NOT NULL,
    model_version TEXT NOT NULL,
    intended_use TEXT NOT NULL,
    out_of_scope_use TEXT NOT NULL,
    training_data_summary TEXT,
    evaluation_data_summary TEXT,
    performance_summary TEXT,
    subgroup_performance_summary TEXT,
    limitations TEXT,
    ethical_considerations TEXT,
    security_and_misuse_considerations TEXT,
    human_oversight_requirements TEXT,
    monitoring_plan TEXT,
    last_reviewed TEXT,
    next_review_date TEXT,
    FOREIGN KEY (system_id) REFERENCES ai_systems(system_id)
);

CREATE TABLE system_cards (
    system_card_id INTEGER PRIMARY KEY,
    system_id INTEGER NOT NULL,
    system_scope TEXT NOT NULL,
    workflow_summary TEXT NOT NULL,
    connected_tools TEXT,
    connected_data_sources TEXT,
    user_roles TEXT,
    human_review_process TEXT,
    contestability_pathway TEXT,
    monitoring_summary TEXT,
    incident_response_summary TEXT,
    last_reviewed TEXT,
    next_review_date TEXT,
    FOREIGN KEY (system_id) REFERENCES ai_systems(system_id)
);

CREATE TABLE data_documentation (
    data_doc_id INTEGER PRIMARY KEY,
    system_id INTEGER NOT NULL,
    data_source_name TEXT NOT NULL,
    provenance_summary TEXT NOT NULL,
    collection_method TEXT,
    population_covered TEXT,
    known_exclusions TEXT,
    data_quality_summary TEXT,
    privacy_considerations TEXT,
    permitted_uses TEXT,
    prohibited_uses TEXT,
    version_label TEXT,
    last_reviewed TEXT,
    FOREIGN KEY (system_id) REFERENCES ai_systems(system_id)
);

CREATE TABLE risk_register (
    risk_id INTEGER PRIMARY KEY,
    system_id INTEGER NOT NULL,
    risk_code TEXT NOT NULL,
    risk_name TEXT NOT NULL,
    risk_category TEXT NOT NULL,
    affected_stakeholders TEXT,
    likelihood REAL NOT NULL,
    impact REAL NOT NULL,
    detectability REAL,
    mitigation_strength REAL NOT NULL,
    residual_risk REAL NOT NULL,
    documentation_completeness REAL,
    documentation_priority REAL,
    risk_owner TEXT NOT NULL,
    mitigation_plan TEXT,
    status TEXT NOT NULL,
    review_date TEXT,
    next_review_date TEXT,
    FOREIGN KEY (system_id) REFERENCES ai_systems(system_id)
);

CREATE TABLE audit_evidence (
    evidence_id INTEGER PRIMARY KEY,
    system_id INTEGER NOT NULL,
    evidence_type TEXT NOT NULL,
    evidence_name TEXT NOT NULL,
    artifact_uri TEXT,
    complete INTEGER NOT NULL,
    evidence_weight REAL NOT NULL,
    collected_at TEXT,
    last_reviewed TEXT,
    owner TEXT,
    access_level TEXT,
    retention_period TEXT,
    FOREIGN KEY (system_id) REFERENCES ai_systems(system_id)
);

CREATE TABLE lifecycle_versions (
    version_id INTEGER PRIMARY KEY,
    system_id INTEGER NOT NULL,
    artifact_type TEXT NOT NULL,
    artifact_name TEXT NOT NULL,
    version_label TEXT NOT NULL,
    change_summary TEXT,
    change_reason TEXT,
    approved_by TEXT,
    approved_at TEXT,
    rollback_available INTEGER DEFAULT 0,
    FOREIGN KEY (system_id) REFERENCES ai_systems(system_id)
);

CREATE TABLE monitoring_records (
    monitoring_id INTEGER PRIMARY KEY,
    system_id INTEGER NOT NULL,
    metric_name TEXT NOT NULL,
    metric_value REAL NOT NULL,
    threshold_value REAL,
    threshold_exceeded INTEGER DEFAULT 0,
    measured_at TEXT NOT NULL,
    reviewed_by TEXT,
    review_status TEXT,
    FOREIGN KEY (system_id) REFERENCES ai_systems(system_id)
);

CREATE TABLE incidents_and_corrective_actions (
    incident_id INTEGER PRIMARY KEY,
    system_id INTEGER NOT NULL,
    incident_type TEXT NOT NULL,
    severity TEXT NOT NULL,
    description TEXT NOT NULL,
    detected_at TEXT NOT NULL,
    owner TEXT NOT NULL,
    root_cause TEXT,
    corrective_action TEXT,
    resolved_at TEXT,
    verification_status TEXT,
    documentation_updated INTEGER NOT NULL,
    FOREIGN KEY (system_id) REFERENCES ai_systems(system_id)
);

CREATE TABLE documentation_reviews (
    review_id INTEGER PRIMARY KEY,
    system_id INTEGER NOT NULL,
    review_date TEXT NOT NULL,
    reviewer TEXT NOT NULL,
    documentation_completeness REAL NOT NULL,
    audit_gap REAL NOT NULL,
    stale_items INTEGER NOT NULL,
    decision TEXT NOT NULL,
    next_review_date TEXT,
    FOREIGN KEY (system_id) REFERENCES ai_systems(system_id)
);

-- Governance query: high residual risks with weak documentation.
SELECT
    s.system_name,
    r.risk_code,
    r.risk_name,
    r.residual_risk,
    r.documentation_completeness,
    r.documentation_priority,
    r.risk_owner,
    r.status
FROM risk_register r
JOIN ai_systems s ON r.system_id = s.system_id
WHERE r.residual_risk >= 0.20
  AND r.documentation_completeness < 0.70
  AND r.status <> 'closed';

-- Governance query: audit evidence completeness by system.
SELECT
    s.system_name,
    SUM(a.complete * a.evidence_weight) / SUM(a.evidence_weight) AS documentation_completeness,
    1 - (SUM(a.complete * a.evidence_weight) / SUM(a.evidence_weight)) AS audit_gap
FROM audit_evidence a
JOIN ai_systems s ON a.system_id = s.system_id
GROUP BY s.system_name;

-- Governance query: incidents where documentation was not updated.
SELECT
    s.system_name,
    i.incident_type,
    i.severity,
    i.detected_at,
    i.owner,
    i.documentation_updated
FROM incidents_and_corrective_actions i
JOIN ai_systems s ON i.system_id = s.system_id
WHERE i.documentation_updated = 0;

-- Governance query: overdue model cards and system cards.
SELECT
    s.system_name,
    'model_card' AS artifact_type,
    m.model_name AS artifact_name,
    m.next_review_date
FROM model_cards m
JOIN ai_systems s ON m.system_id = s.system_id
WHERE m.next_review_date IS NOT NULL
UNION ALL
SELECT
    s.system_name,
    'system_card' AS artifact_type,
    s.system_name AS artifact_name,
    c.next_review_date
FROM system_cards c
JOIN ai_systems s ON c.system_id = s.system_id
WHERE c.next_review_date IS NOT NULL;

-- Governance query: threshold breaches not reviewed.
SELECT
    s.system_name,
    m.metric_name,
    m.metric_value,
    m.threshold_value,
    m.measured_at,
    m.review_status
FROM monitoring_records m
JOIN ai_systems s ON m.system_id = s.system_id
WHERE m.threshold_exceeded = 1
  AND (m.review_status IS NULL OR m.review_status <> 'closed');
