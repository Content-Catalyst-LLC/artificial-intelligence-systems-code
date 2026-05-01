-- AI ethics, human rights, and public accountability schema.
-- This schema supports rights-impact assessment, remedy tracking,
-- public reporting, and audit documentation.

CREATE TABLE ai_public_systems (
    system_id INTEGER PRIMARY KEY,
    system_name TEXT NOT NULL,
    public_or_private_context TEXT NOT NULL,
    purpose TEXT NOT NULL,
    owner_team TEXT NOT NULL,
    deployment_status TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE rights_impact_assessments (
    assessment_id INTEGER PRIMARY KEY,
    system_id INTEGER NOT NULL,
    assessment_date TEXT NOT NULL,
    rights_affected TEXT NOT NULL,
    affected_groups TEXT NOT NULL,
    necessity_assessment TEXT NOT NULL,
    proportionality_assessment TEXT NOT NULL,
    inherent_rights_risk REAL NOT NULL,
    governance_control_strength REAL NOT NULL,
    residual_rights_risk REAL NOT NULL,
    approval_status TEXT NOT NULL,
    FOREIGN KEY (system_id) REFERENCES ai_public_systems(system_id)
);

CREATE TABLE ai_decision_records (
    decision_id INTEGER PRIMARY KEY,
    system_id INTEGER NOT NULL,
    group_label TEXT,
    ai_assisted INTEGER NOT NULL,
    adverse_outcome INTEGER NOT NULL,
    explanation_provided INTEGER NOT NULL,
    appeal_available INTEGER NOT NULL,
    decision_date TEXT NOT NULL,
    FOREIGN KEY (system_id) REFERENCES ai_public_systems(system_id)
);

CREATE TABLE remedies (
    remedy_id INTEGER PRIMARY KEY,
    decision_id INTEGER NOT NULL,
    appeal_submitted INTEGER NOT NULL,
    remedy_provided INTEGER NOT NULL,
    remedy_type TEXT,
    remedy_days INTEGER,
    corrective_action TEXT,
    FOREIGN KEY (decision_id) REFERENCES ai_decision_records(decision_id)
);

CREATE TABLE public_accountability_reports (
    report_id INTEGER PRIMARY KEY,
    system_id INTEGER NOT NULL,
    reporting_period TEXT NOT NULL,
    public_summary_url TEXT,
    adverse_outcome_rate REAL,
    appeal_rate REAL,
    remedy_rate REAL,
    mean_remedy_days REAL,
    audit_status TEXT NOT NULL,
    FOREIGN KEY (system_id) REFERENCES ai_public_systems(system_id)
);

-- Public-accountability query: outcome and remedy rates by system and group.
SELECT
    s.system_name,
    d.group_label,
    AVG(d.adverse_outcome) AS adverse_outcome_rate,
    AVG(r.appeal_submitted) AS appeal_rate,
    AVG(r.remedy_provided) AS remedy_rate,
    AVG(r.remedy_days) AS mean_remedy_days
FROM ai_decision_records d
JOIN ai_public_systems s ON d.system_id = s.system_id
LEFT JOIN remedies r ON d.decision_id = r.decision_id
GROUP BY s.system_name, d.group_label;

-- Governance query: systems with high residual rights risk.
SELECT
    s.system_name,
    r.assessment_date,
    r.residual_rights_risk,
    r.approval_status
FROM rights_impact_assessments r
JOIN ai_public_systems s ON r.system_id = s.system_id
WHERE r.residual_rights_risk >= 0.35;
