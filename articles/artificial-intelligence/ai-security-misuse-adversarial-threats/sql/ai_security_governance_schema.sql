-- AI security governance schema.
-- This schema supports defensive documentation, incident tracking,
-- tool-permission review, security controls, vendor review, red-team tracking,
-- and monitoring.
--
-- It does not implement attack techniques.

CREATE TABLE ai_security_systems (
    system_id INTEGER PRIMARY KEY,
    system_name TEXT NOT NULL,
    purpose TEXT NOT NULL,
    owner_team TEXT NOT NULL,
    deployment_status TEXT NOT NULL,
    risk_level TEXT NOT NULL,
    model_or_service_name TEXT,
    model_version TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT
);

CREATE TABLE ai_security_assets (
    asset_id INTEGER PRIMARY KEY,
    system_id INTEGER NOT NULL,
    asset_name TEXT NOT NULL,
    asset_type TEXT NOT NULL,
    exposure_score REAL NOT NULL,
    impact_score REAL NOT NULL,
    threat_likelihood REAL NOT NULL,
    control_strength REAL NOT NULL,
    residual_risk REAL,
    review_required INTEGER DEFAULT 0,
    FOREIGN KEY (system_id) REFERENCES ai_security_systems(system_id)
);

CREATE TABLE ai_security_controls (
    control_id INTEGER PRIMARY KEY,
    system_id INTEGER NOT NULL,
    control_name TEXT NOT NULL,
    control_type TEXT NOT NULL,
    control_owner TEXT NOT NULL,
    implementation_status TEXT NOT NULL,
    control_strength REAL,
    review_date TEXT,
    next_review_date TEXT,
    FOREIGN KEY (system_id) REFERENCES ai_security_systems(system_id)
);

CREATE TABLE ai_tool_permissions (
    permission_id INTEGER PRIMARY KEY,
    system_id INTEGER NOT NULL,
    tool_name TEXT NOT NULL,
    permission_scope TEXT NOT NULL,
    can_read_sensitive_data INTEGER NOT NULL,
    can_write_records INTEGER NOT NULL,
    can_trigger_external_action INTEGER NOT NULL,
    high_impact_action INTEGER NOT NULL,
    human_approval_required INTEGER NOT NULL,
    logging_enabled INTEGER NOT NULL,
    rollback_available INTEGER DEFAULT 0,
    FOREIGN KEY (system_id) REFERENCES ai_security_systems(system_id)
);

CREATE TABLE ai_retrieval_sources (
    source_id INTEGER PRIMARY KEY,
    system_id INTEGER NOT NULL,
    source_name TEXT NOT NULL,
    source_type TEXT NOT NULL,
    access_controlled INTEGER NOT NULL,
    provenance_documented INTEGER NOT NULL,
    trust_score REAL,
    last_reviewed_at TEXT,
    FOREIGN KEY (system_id) REFERENCES ai_security_systems(system_id)
);

CREATE TABLE ai_security_incidents (
    incident_id INTEGER PRIMARY KEY,
    system_id INTEGER NOT NULL,
    incident_type TEXT NOT NULL,
    severity TEXT NOT NULL,
    detection_source TEXT NOT NULL,
    description TEXT NOT NULL,
    detected_at TEXT NOT NULL,
    contained_at TEXT,
    resolved_at TEXT,
    corrective_action TEXT,
    recurrence_flag INTEGER DEFAULT 0,
    FOREIGN KEY (system_id) REFERENCES ai_security_systems(system_id)
);

CREATE TABLE ai_misuse_monitoring_events (
    event_id INTEGER PRIMARY KEY,
    system_id INTEGER NOT NULL,
    unusual_query_score REAL NOT NULL,
    tool_call_intensity REAL NOT NULL,
    sensitive_output_signal REAL NOT NULL,
    permission_risk REAL NOT NULL,
    retrieval_anomaly_score REAL,
    residual_risk REAL NOT NULL,
    review_flag INTEGER DEFAULT 0,
    event_time TEXT NOT NULL,
    FOREIGN KEY (system_id) REFERENCES ai_security_systems(system_id)
);

CREATE TABLE ai_vendor_security_reviews (
    vendor_review_id INTEGER PRIMARY KEY,
    system_id INTEGER NOT NULL,
    vendor_name TEXT NOT NULL,
    review_date TEXT NOT NULL,
    model_artifact_controls TEXT,
    data_handling_controls TEXT,
    incident_notification_terms TEXT,
    audit_rights TEXT,
    residual_vendor_risk TEXT,
    next_review_date TEXT,
    FOREIGN KEY (system_id) REFERENCES ai_security_systems(system_id)
);

CREATE TABLE ai_red_team_findings (
    finding_id INTEGER PRIMARY KEY,
    system_id INTEGER NOT NULL,
    finding_category TEXT NOT NULL,
    severity TEXT NOT NULL,
    affected_component TEXT NOT NULL,
    description TEXT NOT NULL,
    remediation_owner TEXT NOT NULL,
    remediation_status TEXT NOT NULL,
    residual_risk TEXT,
    found_at TEXT NOT NULL,
    retest_at TEXT,
    FOREIGN KEY (system_id) REFERENCES ai_security_systems(system_id)
);

-- Defensive governance query: tools that require approval but lack it.
SELECT
    s.system_name,
    p.tool_name,
    p.permission_scope,
    p.high_impact_action,
    p.human_approval_required
FROM ai_tool_permissions p
JOIN ai_security_systems s ON p.system_id = s.system_id
WHERE p.high_impact_action = 1
  AND p.human_approval_required = 0;

-- Defensive governance query: average residual risk by system.
SELECT
    s.system_name,
    AVG(m.residual_risk) AS mean_residual_risk,
    AVG(m.review_flag) AS review_flag_rate,
    COUNT(m.event_id) AS monitored_events
FROM ai_misuse_monitoring_events m
JOIN ai_security_systems s ON m.system_id = s.system_id
GROUP BY s.system_name;

-- Defensive governance query: retrieval sources lacking provenance.
SELECT
    s.system_name,
    r.source_name,
    r.source_type,
    r.access_controlled,
    r.provenance_documented,
    r.trust_score
FROM ai_retrieval_sources r
JOIN ai_security_systems s ON r.system_id = s.system_id
WHERE r.provenance_documented = 0
   OR r.trust_score < 0.60;

-- Defensive governance query: unresolved high-severity findings.
SELECT
    s.system_name,
    f.finding_category,
    f.severity,
    f.affected_component,
    f.remediation_status,
    f.residual_risk
FROM ai_red_team_findings f
JOIN ai_security_systems s ON f.system_id = s.system_id
WHERE f.severity IN ('high', 'critical')
  AND f.remediation_status NOT IN ('closed', 'accepted');
