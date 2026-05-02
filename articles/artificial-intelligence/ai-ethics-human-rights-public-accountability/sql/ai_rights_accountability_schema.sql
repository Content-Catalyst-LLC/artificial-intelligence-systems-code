-- AI ethics, human rights, and public accountability schema.
-- This schema supports rights-impact assessment, remedy tracking,
-- public reporting, participation, procurement review, and audit documentation.
--
-- Do not store sensitive, personal, regulated, protected, confidential,
-- clinical, legal, employment, student, immigration, public-benefits, or
-- financial data without appropriate controls.

CREATE TABLE ai_public_systems (
    system_id INTEGER PRIMARY KEY,
    system_name TEXT NOT NULL,
    public_or_private_context TEXT NOT NULL,
    purpose TEXT NOT NULL,
    owner_team TEXT NOT NULL,
    deployment_status TEXT NOT NULL,
    vendor_name TEXT,
    model_or_service_name TEXT,
    model_version TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT
);

CREATE TABLE rights_impact_assessments (
    assessment_id INTEGER PRIMARY KEY,
    system_id INTEGER NOT NULL,
    assessment_date TEXT NOT NULL,
    rights_affected TEXT NOT NULL,
    affected_groups TEXT NOT NULL,
    necessity_assessment TEXT NOT NULL,
    proportionality_assessment TEXT NOT NULL,
    alternatives_considered TEXT,
    inherent_rights_risk REAL NOT NULL,
    governance_control_strength REAL NOT NULL,
    residual_rights_risk REAL NOT NULL,
    approval_status TEXT NOT NULL,
    next_review_date TEXT,
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
    decision_context TEXT,
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
    system_level_change_required INTEGER DEFAULT 0,
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
    burden_indicator REAL,
    audit_status TEXT NOT NULL,
    published_at TEXT,
    FOREIGN KEY (system_id) REFERENCES ai_public_systems(system_id)
);

CREATE TABLE community_participation_records (
    participation_id INTEGER PRIMARY KEY,
    system_id INTEGER NOT NULL,
    participation_date TEXT NOT NULL,
    stakeholder_group TEXT NOT NULL,
    participation_method TEXT NOT NULL,
    concerns_raised TEXT,
    changes_made TEXT,
    feedback_loop_completed INTEGER DEFAULT 0,
    FOREIGN KEY (system_id) REFERENCES ai_public_systems(system_id)
);

CREATE TABLE vendor_accountability_reviews (
    vendor_review_id INTEGER PRIMARY KEY,
    system_id INTEGER NOT NULL,
    vendor_name TEXT NOT NULL,
    review_date TEXT NOT NULL,
    documentation_received INTEGER NOT NULL,
    audit_rights_in_contract INTEGER NOT NULL,
    incident_notification_terms INTEGER NOT NULL,
    data_protection_terms INTEGER NOT NULL,
    public_reporting_support INTEGER DEFAULT 0,
    residual_vendor_risk TEXT,
    next_review_date TEXT,
    FOREIGN KEY (system_id) REFERENCES ai_public_systems(system_id)
);

CREATE TABLE ai_ethics_incidents (
    incident_id INTEGER PRIMARY KEY,
    system_id INTEGER NOT NULL,
    incident_type TEXT NOT NULL,
    severity TEXT NOT NULL,
    affected_groups TEXT,
    description TEXT NOT NULL,
    detected_at TEXT NOT NULL,
    resolved_at TEXT,
    remedy_summary TEXT,
    system_change_made INTEGER DEFAULT 0,
    FOREIGN KEY (system_id) REFERENCES ai_public_systems(system_id)
);

CREATE TABLE decommissioning_reviews (
    review_id INTEGER PRIMARY KEY,
    system_id INTEGER NOT NULL,
    review_date TEXT NOT NULL,
    trigger_reason TEXT NOT NULL,
    residual_rights_risk REAL,
    continued_use_justification TEXT,
    decision TEXT NOT NULL,
    next_action TEXT,
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
    r.approval_status,
    r.next_review_date
FROM rights_impact_assessments r
JOIN ai_public_systems s ON r.system_id = s.system_id
WHERE r.residual_rights_risk >= 0.35;

-- Governance query: vendor reviews missing accountability protections.
SELECT
    s.system_name,
    v.vendor_name,
    v.audit_rights_in_contract,
    v.incident_notification_terms,
    v.data_protection_terms,
    v.public_reporting_support
FROM vendor_accountability_reviews v
JOIN ai_public_systems s ON v.system_id = s.system_id
WHERE v.audit_rights_in_contract = 0
   OR v.incident_notification_terms = 0
   OR v.data_protection_terms = 0;

-- Governance query: participation records without completed feedback loop.
SELECT
    s.system_name,
    p.stakeholder_group,
    p.participation_method,
    p.concerns_raised,
    p.feedback_loop_completed
FROM community_participation_records p
JOIN ai_public_systems s ON p.system_id = s.system_id
WHERE p.feedback_loop_completed = 0;
