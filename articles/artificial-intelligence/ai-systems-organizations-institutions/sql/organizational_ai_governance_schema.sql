-- AI Systems in Organizations and Institutions Metadata Schema

CREATE TABLE IF NOT EXISTS organizational_ai_programs (
    program_id TEXT PRIMARY KEY,
    organization_name TEXT NOT NULL,
    program_name TEXT NOT NULL,
    program_owner TEXT NOT NULL,
    institutional_context TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ai_use_cases (
    use_case_id TEXT PRIMARY KEY,
    program_id TEXT NOT NULL,
    use_case_name TEXT NOT NULL,
    department TEXT,
    workflow_owner TEXT,
    intended_use TEXT NOT NULL,
    affected_population TEXT,
    decision_type TEXT CHECK(decision_type IN ('operational', 'employment', 'public_service', 'healthcare', 'finance', 'education', 'infrastructure', 'legal', 'other')),
    decision_frequency TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(program_id) REFERENCES organizational_ai_programs(program_id)
);

CREATE TABLE IF NOT EXISTS decision_allocation_reviews (
    review_id TEXT PRIMARY KEY,
    use_case_id TEXT NOT NULL,
    review_date DATE NOT NULL,
    decision_risk_score REAL,
    ai_readiness_score REAL,
    recommended_decision_mode TEXT CHECK(recommended_decision_mode IN ('human_only', 'ai_decision_support_only', 'human_in_the_loop', 'human_on_the_loop', 'monitored_automation', 'full_delegation', 'human_led_with_ai_support_and_strong_review')),
    rationale TEXT,
    reviewer TEXT,
    FOREIGN KEY(use_case_id) REFERENCES ai_use_cases(use_case_id)
);

CREATE TABLE IF NOT EXISTS organizational_risk_factors (
    risk_factor_id TEXT PRIMARY KEY,
    use_case_id TEXT NOT NULL,
    risk_type TEXT CHECK(risk_type IN ('model_error', 'workflow_coupling', 'opacity', 'overreliance', 'governance_gap', 'rights_impact', 'safety_impact', 'labor_impact', 'privacy', 'vendor_dependency', 'other')),
    risk_score REAL,
    mitigation_plan TEXT,
    residual_risk TEXT CHECK(residual_risk IN ('low', 'medium', 'high', 'critical', 'unknown')),
    FOREIGN KEY(use_case_id) REFERENCES ai_use_cases(use_case_id)
);

CREATE TABLE IF NOT EXISTS oversight_controls (
    control_id TEXT PRIMARY KEY,
    use_case_id TEXT NOT NULL,
    control_name TEXT NOT NULL,
    control_type TEXT CHECK(control_type IN ('human_review', 'override', 'appeal', 'audit', 'monitoring', 'documentation', 'access_control', 'incident_response', 'vendor_review', 'other')),
    control_owner TEXT,
    control_frequency TEXT,
    control_status TEXT CHECK(control_status IN ('planned', 'active', 'needs_update', 'retired', 'missing')),
    notes TEXT,
    FOREIGN KEY(use_case_id) REFERENCES ai_use_cases(use_case_id)
);

CREATE TABLE IF NOT EXISTS institutional_legitimacy_reviews (
    legitimacy_review_id TEXT PRIMARY KEY,
    use_case_id TEXT NOT NULL,
    legal_alignment_reviewed BOOLEAN DEFAULT FALSE,
    professional_norms_reviewed BOOLEAN DEFAULT FALSE,
    stakeholder_impact_reviewed BOOLEAN DEFAULT FALSE,
    public_accountability_reviewed BOOLEAN DEFAULT FALSE,
    accessibility_reviewed BOOLEAN DEFAULT FALSE,
    contestability_reviewed BOOLEAN DEFAULT FALSE,
    findings TEXT,
    required_actions TEXT,
    status TEXT CHECK(status IN ('draft', 'approved', 'requires_action', 'closed')),
    FOREIGN KEY(use_case_id) REFERENCES ai_use_cases(use_case_id)
);

CREATE TABLE IF NOT EXISTS ai_incidents_and_lessons (
    incident_id TEXT PRIMARY KEY,
    use_case_id TEXT NOT NULL,
    incident_date DATE NOT NULL,
    incident_type TEXT CHECK(incident_type IN ('model_error', 'data_failure', 'workflow_failure', 'overreliance', 'bias_or_fairness', 'privacy', 'security', 'public_complaint', 'other')),
    incident_description TEXT NOT NULL,
    affected_population TEXT,
    severity TEXT CHECK(severity IN ('low', 'medium', 'high', 'critical', 'unknown')),
    corrective_action TEXT,
    lesson_learned TEXT,
    status TEXT CHECK(status IN ('open', 'investigating', 'mitigated', 'closed')),
    FOREIGN KEY(use_case_id) REFERENCES ai_use_cases(use_case_id)
);

CREATE TABLE IF NOT EXISTS governance_reviews (
    governance_review_id TEXT PRIMARY KEY,
    program_id TEXT NOT NULL,
    review_date DATE NOT NULL,
    reviewer TEXT NOT NULL,
    use_case_inventory_reviewed BOOLEAN DEFAULT FALSE,
    risk_classification_reviewed BOOLEAN DEFAULT FALSE,
    decision_allocation_reviewed BOOLEAN DEFAULT FALSE,
    oversight_controls_reviewed BOOLEAN DEFAULT FALSE,
    documentation_reviewed BOOLEAN DEFAULT FALSE,
    incident_reviewed BOOLEAN DEFAULT FALSE,
    findings TEXT,
    required_actions TEXT,
    status TEXT CHECK(status IN ('draft', 'approved', 'requires_action', 'closed')),
    FOREIGN KEY(program_id) REFERENCES organizational_ai_programs(program_id)
);
