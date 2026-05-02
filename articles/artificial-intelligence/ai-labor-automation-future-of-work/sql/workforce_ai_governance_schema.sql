-- AI labor and future-of-work governance schema.
-- This schema supports workplace AI impact assessment, task exposure,
-- job-quality monitoring, training access, worker consultation, worker appeals,
-- transition planning, productivity distribution, and governance review.
--
-- Do not store sensitive, personal, employee-identifiable, regulated,
-- protected, confidential, compensation, disciplinary, union, health,
-- immigration, labor-relations, or workplace-surveillance data without
-- appropriate controls.

CREATE TABLE workplace_ai_systems (
    system_id INTEGER PRIMARY KEY,
    system_name TEXT NOT NULL,
    purpose TEXT NOT NULL,
    owner_team TEXT NOT NULL,
    deployment_status TEXT NOT NULL,
    vendor_name TEXT,
    model_or_service_name TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT
);

CREATE TABLE workforce_impact_assessments (
    assessment_id INTEGER PRIMARY KEY,
    system_id INTEGER NOT NULL,
    assessment_date TEXT NOT NULL,
    affected_roles TEXT NOT NULL,
    automation_scope TEXT,
    augmentation_scope TEXT,
    monitoring_scope TEXT,
    discipline_or_termination_impact INTEGER NOT NULL,
    worker_consultation_completed INTEGER NOT NULL,
    training_plan_available INTEGER NOT NULL,
    appeal_pathway_available INTEGER NOT NULL,
    residual_labor_risk TEXT,
    approval_status TEXT NOT NULL,
    next_review_date TEXT,
    FOREIGN KEY (system_id) REFERENCES workplace_ai_systems(system_id)
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
    training_function REAL,
    worker_autonomy_importance REAL,
    automation_pressure REAL NOT NULL,
    augmentation_potential REAL NOT NULL,
    deskilling_risk REAL,
    worker_autonomy_risk REAL,
    redesign_category TEXT NOT NULL,
    governance_review_required INTEGER DEFAULT 0,
    FOREIGN KEY (system_id) REFERENCES workplace_ai_systems(system_id)
);

CREATE TABLE job_quality_monitoring (
    record_id INTEGER PRIMARY KEY,
    system_id INTEGER NOT NULL,
    role_group TEXT NOT NULL,
    employment_status TEXT,
    ai_exposure REAL NOT NULL,
    wage_security REAL NOT NULL,
    autonomy REAL NOT NULL,
    skill_development REAL NOT NULL,
    health_safety REAL NOT NULL,
    worker_voice REAL NOT NULL,
    monitoring_burden REAL NOT NULL,
    workload_intensity REAL,
    schedule_predictability REAL,
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
    consultation_method TEXT NOT NULL,
    concerns_raised TEXT,
    changes_made TEXT,
    unresolved_issues TEXT,
    feedback_loop_completed INTEGER DEFAULT 0,
    FOREIGN KEY (system_id) REFERENCES workplace_ai_systems(system_id)
);

CREATE TABLE workforce_transition_plans (
    plan_id INTEGER PRIMARY KEY,
    system_id INTEGER NOT NULL,
    role_group TEXT NOT NULL,
    exposure_level TEXT NOT NULL,
    training_plan TEXT NOT NULL,
    paid_training_time INTEGER NOT NULL,
    redeployment_pathway TEXT,
    mobility_support TEXT,
    wage_or_gain_sharing_plan TEXT,
    review_date TEXT NOT NULL,
    FOREIGN KEY (system_id) REFERENCES workplace_ai_systems(system_id)
);

CREATE TABLE productivity_distribution_records (
    distribution_id INTEGER PRIMARY KEY,
    system_id INTEGER NOT NULL,
    role_group TEXT NOT NULL,
    reporting_period TEXT NOT NULL,
    estimated_productivity_gain REAL,
    worker_gain_share REAL,
    workload_change REAL,
    wage_change REAL,
    working_time_change REAL,
    job_quality_change REAL,
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
    system_change_required INTEGER DEFAULT 0,
    FOREIGN KEY (system_id) REFERENCES workplace_ai_systems(system_id)
);

CREATE TABLE workplace_ai_incidents (
    incident_id INTEGER PRIMARY KEY,
    system_id INTEGER NOT NULL,
    incident_type TEXT NOT NULL,
    severity TEXT NOT NULL,
    affected_worker_group TEXT,
    description TEXT NOT NULL,
    detected_at TEXT NOT NULL,
    resolved_at TEXT,
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

-- Governance query: high monitoring burden and low worker voice.
SELECT
    s.system_name,
    j.role_group,
    AVG(j.monitoring_burden) AS mean_monitoring_burden,
    AVG(j.worker_voice) AS mean_worker_voice,
    AVG(j.job_quality_score) AS mean_job_quality_score
FROM job_quality_monitoring j
JOIN workplace_ai_systems s ON j.system_id = s.system_id
GROUP BY s.system_name, j.role_group
HAVING AVG(j.monitoring_burden) >= 0.60
   AND AVG(j.worker_voice) < 0.50;

-- Governance query: consultation records without completed feedback loops.
SELECT
    s.system_name,
    c.worker_group,
    c.consultation_method,
    c.concerns_raised,
    c.unresolved_issues,
    c.feedback_loop_completed
FROM worker_consultation_records c
JOIN workplace_ai_systems s ON c.system_id = s.system_id
WHERE c.feedback_loop_completed = 0;

-- Governance query: productivity gains not shared with workers.
SELECT
    s.system_name,
    p.role_group,
    p.reporting_period,
    p.estimated_productivity_gain,
    p.worker_gain_share,
    p.workload_change,
    p.wage_change,
    p.working_time_change
FROM productivity_distribution_records p
JOIN workplace_ai_systems s ON p.system_id = s.system_id
WHERE p.estimated_productivity_gain > 0
  AND (p.worker_gain_share IS NULL OR p.worker_gain_share < 0.30);
