-- AI labor and future-of-work governance schema.
-- This schema supports workplace AI impact assessment, task exposure,
-- job-quality monitoring, training access, worker consultation, and appeals.

CREATE TABLE workplace_ai_systems (
    system_id INTEGER PRIMARY KEY,
    system_name TEXT NOT NULL,
    purpose TEXT NOT NULL,
    owner_team TEXT NOT NULL,
    deployment_status TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE task_inventory (
    task_id INTEGER PRIMARY KEY,
    system_id INTEGER NOT NULL,
    role_group TEXT NOT NULL,
    task_name TEXT NOT NULL,
    task_weight REAL NOT NULL,
    ai_capability REAL NOT NULL,
    routineness REAL NOT NULL,
    human_judgment_requirement REAL NOT NULL,
    task_value REAL NOT NULL,
    automation_pressure REAL NOT NULL,
    augmentation_potential REAL NOT NULL,
    redesign_category TEXT NOT NULL,
    FOREIGN KEY (system_id) REFERENCES workplace_ai_systems(system_id)
);

CREATE TABLE job_quality_monitoring (
    record_id INTEGER PRIMARY KEY,
    system_id INTEGER NOT NULL,
    role_group TEXT NOT NULL,
    ai_exposure REAL NOT NULL,
    wage_security REAL NOT NULL,
    autonomy REAL NOT NULL,
    skill_development REAL NOT NULL,
    health_safety REAL NOT NULL,
    worker_voice REAL NOT NULL,
    monitoring_burden REAL NOT NULL,
    training_access REAL NOT NULL,
    job_quality_score REAL NOT NULL,
    measured_at TEXT NOT NULL,
    FOREIGN KEY (system_id) REFERENCES workplace_ai_systems(system_id)
);

CREATE TABLE worker_consultation_records (
    consultation_id INTEGER PRIMARY KEY,
    system_id INTEGER NOT NULL,
    consultation_date TEXT NOT NULL,
    worker_group TEXT NOT NULL,
    concerns_raised TEXT,
    changes_made TEXT,
    unresolved_issues TEXT,
    FOREIGN KEY (system_id) REFERENCES workplace_ai_systems(system_id)
);

CREATE TABLE workforce_transition_plans (
    plan_id INTEGER PRIMARY KEY,
    system_id INTEGER NOT NULL,
    role_group TEXT NOT NULL,
    training_plan TEXT NOT NULL,
    redeployment_pathway TEXT,
    wage_or_gain_sharing_plan TEXT,
    review_date TEXT NOT NULL,
    FOREIGN KEY (system_id) REFERENCES workplace_ai_systems(system_id)
);

CREATE TABLE workplace_ai_appeals (
    appeal_id INTEGER PRIMARY KEY,
    system_id INTEGER NOT NULL,
    worker_group TEXT NOT NULL,
    appeal_type TEXT NOT NULL,
    submitted_at TEXT NOT NULL,
    resolved_at TEXT,
    outcome TEXT,
    corrective_action TEXT,
    FOREIGN KEY (system_id) REFERENCES workplace_ai_systems(system_id)
);

-- Governance query: role groups with high exposure and low training access.
SELECT
    s.system_name,
    j.role_group,
    AVG(j.ai_exposure) AS mean_ai_exposure,
    AVG(j.training_access) AS mean_training_access,
    AVG(j.job_quality_score) AS mean_job_quality_score
FROM job_quality_monitoring j
JOIN workplace_ai_systems s ON j.system_id = s.system_id
GROUP BY s.system_name, j.role_group
HAVING AVG(j.ai_exposure) >= 0.60
   AND AVG(j.training_access) < 0.50;

-- Governance query: tasks where automation pressure is high.
SELECT
    s.system_name,
    t.role_group,
    t.task_name,
    t.automation_pressure,
    t.human_judgment_requirement,
    t.redesign_category
FROM task_inventory t
JOIN workplace_ai_systems s ON t.system_id = s.system_id
WHERE t.automation_pressure >= 0.35;
