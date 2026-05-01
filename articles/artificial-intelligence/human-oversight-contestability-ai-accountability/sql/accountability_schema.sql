-- AI accountability and contestability schema
-- This SQL file is for documentation and prototyping.
-- It avoids vendor-specific features where possible.

CREATE TABLE ai_systems (
    system_id INTEGER PRIMARY KEY,
    system_name TEXT NOT NULL,
    purpose TEXT NOT NULL,
    owner_team TEXT NOT NULL,
    risk_level TEXT NOT NULL,
    deployment_status TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE oversight_cases (
    case_id INTEGER PRIMARY KEY,
    system_id INTEGER NOT NULL,
    model_output TEXT NOT NULL,
    uncertainty_score REAL NOT NULL,
    expected_risk REAL NOT NULL,
    rights_sensitive INTEGER NOT NULL,
    vulnerable_context INTEGER NOT NULL,
    route TEXT NOT NULL,
    final_decision TEXT,
    human_reviewer TEXT,
    decision_reason TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (system_id) REFERENCES ai_systems(system_id)
);

CREATE TABLE appeals (
    appeal_id INTEGER PRIMARY KEY,
    case_id INTEGER NOT NULL,
    appeal_reason TEXT NOT NULL,
    submitted_at TEXT NOT NULL,
    resolved_at TEXT,
    appeal_status TEXT NOT NULL,
    correction_made INTEGER NOT NULL,
    remedy_description TEXT,
    FOREIGN KEY (case_id) REFERENCES oversight_cases(case_id)
);

CREATE TABLE incidents (
    incident_id INTEGER PRIMARY KEY,
    system_id INTEGER NOT NULL,
    incident_type TEXT NOT NULL,
    severity TEXT NOT NULL,
    description TEXT NOT NULL,
    detected_at TEXT NOT NULL,
    resolved_at TEXT,
    corrective_action TEXT,
    FOREIGN KEY (system_id) REFERENCES ai_systems(system_id)
);

-- Example monitoring query: appeal success rate by system.
SELECT
    s.system_name,
    COUNT(a.appeal_id) AS total_appeals,
    AVG(a.correction_made) AS correction_rate
FROM appeals a
JOIN oversight_cases c ON a.case_id = c.case_id
JOIN ai_systems s ON c.system_id = s.system_id
GROUP BY s.system_name;
