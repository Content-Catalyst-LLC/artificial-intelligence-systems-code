-- AI, expertise, and human judgment governance schema.
-- This SQL file is for documentation and prototyping.
-- Do not store sensitive, personal, regulated, clinical, legal, or confidential data in this schema without appropriate controls.

CREATE TABLE ai_expert_systems (
    system_id INTEGER PRIMARY KEY,
    system_name TEXT NOT NULL,
    domain TEXT NOT NULL,
    purpose TEXT NOT NULL,
    owner_team TEXT NOT NULL,
    deployment_status TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE expert_review_cases (
    case_id INTEGER PRIMARY KEY,
    system_id INTEGER NOT NULL,
    ai_output TEXT NOT NULL,
    ai_confidence REAL,
    expert_judgment TEXT,
    expert_role TEXT,
    context_complexity REAL,
    warranted_ai_reliance REAL,
    observed_ai_reliance REAL,
    automation_bias_flag INTEGER,
    ai_expert_disagreement REAL,
    review_required INTEGER,
    final_decision TEXT,
    rationale TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (system_id) REFERENCES ai_expert_systems(system_id)
);

CREATE TABLE expertise_monitoring_metrics (
    metric_id INTEGER PRIMARY KEY,
    system_id INTEGER NOT NULL,
    metric_name TEXT NOT NULL,
    metric_value REAL NOT NULL,
    measured_at TEXT NOT NULL,
    FOREIGN KEY (system_id) REFERENCES ai_expert_systems(system_id)
);

CREATE TABLE training_and_skill_reviews (
    review_id INTEGER PRIMARY KEY,
    system_id INTEGER NOT NULL,
    reviewer_group TEXT NOT NULL,
    skill_indicator TEXT NOT NULL,
    indicator_value REAL NOT NULL,
    review_date TEXT NOT NULL,
    corrective_action TEXT,
    FOREIGN KEY (system_id) REFERENCES ai_expert_systems(system_id)
);

CREATE TABLE disagreement_reviews (
    disagreement_id INTEGER PRIMARY KEY,
    case_id INTEGER NOT NULL,
    disagreement_type TEXT NOT NULL,
    possible_cause TEXT,
    severity TEXT,
    resolution TEXT,
    system_update_required INTEGER,
    reviewed_at TEXT NOT NULL,
    FOREIGN KEY (case_id) REFERENCES expert_review_cases(case_id)
);

-- Example monitoring query: AI-expert disagreement by system.
SELECT
    s.system_name,
    AVG(c.ai_expert_disagreement) AS mean_ai_expert_disagreement,
    AVG(c.observed_ai_reliance) AS mean_observed_ai_reliance,
    AVG(c.automation_bias_flag) AS automation_bias_rate,
    COUNT(c.case_id) AS reviewed_cases
FROM expert_review_cases c
JOIN ai_expert_systems s ON c.system_id = s.system_id
GROUP BY s.system_name;
