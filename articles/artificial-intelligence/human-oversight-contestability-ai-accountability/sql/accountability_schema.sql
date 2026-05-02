-- AI accountability and contestability schema.
-- This file is intended for educational governance prototyping.
-- Do not store sensitive, personal, regulated, clinical, legal, government-benefits,
-- employment, immigration, financial, or confidential data without appropriate controls.

CREATE TABLE ai_systems (
    system_id INTEGER PRIMARY KEY,
    system_name TEXT NOT NULL,
    purpose TEXT NOT NULL,
    owner_team TEXT NOT NULL,
    risk_level TEXT NOT NULL,
    deployment_status TEXT NOT NULL,
    vendor_name TEXT,
    model_version TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT
);

CREATE TABLE oversight_cases (
    case_id INTEGER PRIMARY KEY,
    system_id INTEGER NOT NULL,
    model_output TEXT NOT NULL,
    uncertainty_score REAL NOT NULL,
    expected_risk REAL NOT NULL,
    rights_sensitive INTEGER NOT NULL,
    vulnerable_context INTEGER NOT NULL,
    affected_group TEXT,
    route TEXT NOT NULL,
    review_reason TEXT,
    final_decision TEXT,
    human_reviewer TEXT,
    decision_reason TEXT,
    affected_person_notified INTEGER DEFAULT 0,
    appeal_pathway_provided INTEGER DEFAULT 0,
    created_at TEXT NOT NULL,
    FOREIGN KEY (system_id) REFERENCES ai_systems(system_id)
);

CREATE TABLE decision_records (
    record_id INTEGER PRIMARY KEY,
    case_id INTEGER NOT NULL,
    input_summary TEXT NOT NULL,
    evidence_summary TEXT,
    model_output TEXT NOT NULL,
    uncertainty_score REAL,
    expected_risk REAL,
    reviewer_rationale TEXT,
    final_action TEXT,
    timestamp_utc TEXT NOT NULL,
    FOREIGN KEY (case_id) REFERENCES oversight_cases(case_id)
);

CREATE TABLE appeals (
    appeal_id INTEGER PRIMARY KEY,
    case_id INTEGER NOT NULL,
    appeal_reason TEXT NOT NULL,
    submitted_at TEXT NOT NULL,
    acknowledged_at TEXT,
    resolved_at TEXT,
    appeal_status TEXT NOT NULL,
    correction_made INTEGER NOT NULL,
    remedy_description TEXT,
    system_issue_detected INTEGER DEFAULT 0,
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
    recurrence_flag INTEGER DEFAULT 0,
    FOREIGN KEY (system_id) REFERENCES ai_systems(system_id)
);

CREATE TABLE reviewer_workload (
    workload_id INTEGER PRIMARY KEY,
    system_id INTEGER NOT NULL,
    reviewer_group TEXT NOT NULL,
    review_period_start TEXT NOT NULL,
    review_period_end TEXT NOT NULL,
    review_count INTEGER NOT NULL,
    available_review_hours REAL NOT NULL,
    mean_minutes_per_review REAL NOT NULL,
    capacity_status TEXT NOT NULL,
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

-- Example monitoring query: human-review rate by system and affected group.
SELECT
    s.system_name,
    c.affected_group,
    AVG(CASE WHEN c.route = 'human_review' THEN 1.0 ELSE 0.0 END) AS human_review_rate,
    AVG(c.expected_risk) AS mean_expected_risk,
    AVG(c.uncertainty_score) AS mean_uncertainty
FROM oversight_cases c
JOIN ai_systems s ON c.system_id = s.system_id
GROUP BY s.system_name, c.affected_group;

-- Example monitoring query: reviewer capacity pressure.
SELECT
    s.system_name,
    w.reviewer_group,
    w.review_count,
    w.available_review_hours,
    w.mean_minutes_per_review,
    w.capacity_status
FROM reviewer_workload w
JOIN ai_systems s ON w.system_id = s.system_id;
