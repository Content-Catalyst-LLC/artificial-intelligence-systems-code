-- AI security governance schema.
-- This schema supports defensive documentation, incident tracking,
-- tool-permission review, security controls, and monitoring.
-- It does not implement attack techniques.

CREATE TABLE ai_security_systems (
    system_id INTEGER PRIMARY KEY,
    system_name TEXT NOT NULL,
    purpose TEXT NOT NULL,
    owner_team TEXT NOT NULL,
    deployment_status TEXT NOT NULL,
    risk_level TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE ai_security_assets (
    asset_id INTEGER PRIMARY KEY,
    system_id INTEGER NOT NULL,
    asset_name TEXT NOT NULL,
    asset_type TEXT NOT NULL,
    exposure_score REAL NOT NULL,
    impact_score REAL NOT NULL,
    control_strength REAL NOT NULL,
    FOREIGN KEY (system_id) REFERENCES ai_security_systems(system_id)
);

CREATE TABLE ai_security_controls (
    control_id INTEGER PRIMARY KEY,
    system_id INTEGER NOT NULL,
    control_name TEXT NOT NULL,
    control_type TEXT NOT NULL,
    control_owner TEXT NOT NULL,
    implementation_status TEXT NOT NULL,
    review_date TEXT,
    FOREIGN KEY (system_id) REFERENCES ai_security_systems(system_id)
);

CREATE TABLE ai_tool_permissions (
    permission_id INTEGER PRIMARY KEY,
    system_id INTEGER NOT NULL,
    tool_name TEXT NOT NULL,
    permission_scope TEXT NOT NULL,
    high_impact_action INTEGER NOT NULL,
    human_approval_required INTEGER NOT NULL,
    logging_enabled INTEGER NOT NULL,
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
    FOREIGN KEY (system_id) REFERENCES ai_security_systems(system_id)
);

CREATE TABLE ai_misuse_monitoring_events (
    event_id INTEGER PRIMARY KEY,
    system_id INTEGER NOT NULL,
    unusual_query_score REAL NOT NULL,
    tool_call_intensity REAL NOT NULL,
    sensitive_output_signal REAL NOT NULL,
    permission_risk REAL NOT NULL,
    residual_risk REAL NOT NULL,
    event_time TEXT NOT NULL,
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
    COUNT(m.event_id) AS monitored_events
FROM ai_misuse_monitoring_events m
JOIN ai_security_systems s ON m.system_id = s.system_id
GROUP BY s.system_name;
