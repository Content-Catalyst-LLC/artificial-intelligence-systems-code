-- AI Governance and Regulatory Systems Metadata Schema

CREATE TABLE IF NOT EXISTS ai_systems (
    system_id TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    system_purpose TEXT NOT NULL,
    owner_team TEXT NOT NULL,
    vendor_name TEXT,
    deployment_status TEXT CHECK(deployment_status IN ('proposed', 'development', 'pilot', 'production', 'paused', 'retired')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ai_use_cases (
    use_case_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    domain_name TEXT NOT NULL,
    intended_use TEXT NOT NULL,
    prohibited_use_screening TEXT,
    affected_population TEXT,
    public_sector BOOLEAN DEFAULT FALSE,
    high_impact BOOLEAN DEFAULT FALSE,
    FOREIGN KEY(system_id) REFERENCES ai_systems(system_id)
);

CREATE TABLE IF NOT EXISTS risk_assessments (
    assessment_id TEXT PRIMARY KEY,
    use_case_id TEXT NOT NULL,
    assessment_date DATE NOT NULL,
    risk_tier TEXT CHECK(risk_tier IN ('minimal', 'limited', 'high', 'prohibited', 'uncertain')),
    likelihood_score REAL,
    severity_score REAL,
    inherent_risk_score REAL,
    mitigation_maturity REAL,
    residual_risk_score REAL,
    assessor TEXT NOT NULL,
    review_status TEXT CHECK(review_status IN ('draft', 'approved', 'requires_revision', 'rejected')),
    FOREIGN KEY(use_case_id) REFERENCES ai_use_cases(use_case_id)
);

CREATE TABLE IF NOT EXISTS governance_controls (
    control_id TEXT PRIMARY KEY,
    control_name TEXT NOT NULL,
    control_category TEXT CHECK(control_category IN ('documentation', 'evaluation', 'human_oversight', 'security', 'privacy', 'bias_fairness', 'monitoring', 'incident_response', 'vendor_management', 'legal_review')),
    control_description TEXT NOT NULL,
    mapped_framework TEXT,
    required_for_risk_tier TEXT
);

CREATE TABLE IF NOT EXISTS control_evidence (
    evidence_id TEXT PRIMARY KEY,
    assessment_id TEXT NOT NULL,
    control_id TEXT NOT NULL,
    evidence_uri TEXT,
    evidence_summary TEXT,
    evidence_status TEXT CHECK(evidence_status IN ('missing', 'partial', 'complete', 'not_applicable')),
    evidence_owner TEXT,
    last_updated DATE,
    FOREIGN KEY(assessment_id) REFERENCES risk_assessments(assessment_id),
    FOREIGN KEY(control_id) REFERENCES governance_controls(control_id)
);

CREATE TABLE IF NOT EXISTS governance_reviews (
    review_id TEXT PRIMARY KEY,
    assessment_id TEXT NOT NULL,
    review_date DATE NOT NULL,
    reviewer TEXT NOT NULL,
    decision TEXT CHECK(decision IN ('approve', 'approve_with_conditions', 'pause', 'reject', 'retire')),
    conditions TEXT,
    next_review_date DATE,
    FOREIGN KEY(assessment_id) REFERENCES risk_assessments(assessment_id)
);

CREATE TABLE IF NOT EXISTS ai_incidents (
    incident_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    incident_date DATE NOT NULL,
    incident_type TEXT,
    severity_level TEXT CHECK(severity_level IN ('low', 'moderate', 'high', 'critical')),
    affected_population TEXT,
    incident_summary TEXT NOT NULL,
    remediation_status TEXT CHECK(remediation_status IN ('open', 'investigating', 'mitigated', 'closed')),
    reportable BOOLEAN DEFAULT FALSE,
    FOREIGN KEY(system_id) REFERENCES ai_systems(system_id)
);

CREATE TABLE IF NOT EXISTS monitoring_events (
    monitoring_event_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    event_date DATE NOT NULL,
    metric_name TEXT NOT NULL,
    metric_value REAL NOT NULL,
    threshold_value REAL,
    alert_level TEXT,
    review_required BOOLEAN DEFAULT FALSE,
    FOREIGN KEY(system_id) REFERENCES ai_systems(system_id)
);
