-- AI documentation governance schema.
-- This schema supports risk registers, model cards, audit evidence,
-- lifecycle traceability, approvals, incidents, and corrective actions.

CREATE TABLE ai_systems (
    system_id INTEGER PRIMARY KEY,
    system_name TEXT NOT NULL,
    purpose TEXT NOT NULL,
    owner_team TEXT NOT NULL,
    deployment_status TEXT NOT NULL,
    risk_level TEXT NOT NULL,
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
    limitations TEXT,
    ethical_considerations TEXT,
    monitoring_plan TEXT,
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
    mitigation_strength REAL NOT NULL,
    residual_risk REAL NOT NULL,
    risk_owner TEXT NOT NULL,
    mitigation_plan TEXT,
    status TEXT NOT NULL,
    review_date TEXT,
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
    owner TEXT,
    FOREIGN KEY (system_id) REFERENCES ai_systems(system_id)
);

CREATE TABLE lifecycle_versions (
    version_id INTEGER PRIMARY KEY,
    system_id INTEGER NOT NULL,
    artifact_type TEXT NOT NULL,
    artifact_name TEXT NOT NULL,
    version_label TEXT NOT NULL,
    change_summary TEXT,
    approved_by TEXT,
    approved_at TEXT,
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
    corrective_action TEXT,
    resolved_at TEXT,
    documentation_updated INTEGER NOT NULL,
    FOREIGN KEY (system_id) REFERENCES ai_systems(system_id)
);

-- Governance query: high residual risks with weak documentation.
SELECT
    s.system_name,
    r.risk_code,
    r.risk_name,
    r.residual_risk,
    r.risk_owner,
    r.status
FROM risk_register r
JOIN ai_systems s ON r.system_id = s.system_id
WHERE r.residual_risk >= 0.20
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
