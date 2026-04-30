-- Human-AI Interaction and Interface Design Metadata Schema

CREATE TABLE IF NOT EXISTS ai_interaction_systems (
    system_id TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    system_purpose TEXT NOT NULL,
    owner_team TEXT NOT NULL,
    interaction_mode TEXT CHECK(interaction_mode IN ('decision_support', 'collaboration', 'supervision', 'delegation', 'generative_prompting', 'mixed')),
    deployment_status TEXT CHECK(deployment_status IN ('proposed', 'development', 'pilot', 'production', 'paused', 'retired')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS user_groups (
    user_group_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    group_name TEXT NOT NULL,
    expertise_level TEXT CHECK(expertise_level IN ('novice', 'intermediate', 'expert', 'mixed', 'unknown')),
    workflow_context TEXT,
    accessibility_needs TEXT,
    affected_stakeholder BOOLEAN DEFAULT FALSE,
    FOREIGN KEY(system_id) REFERENCES ai_interaction_systems(system_id)
);

CREATE TABLE IF NOT EXISTS interface_presentations (
    presentation_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    model_version TEXT,
    presentation_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    input_reference TEXT,
    output_type TEXT CHECK(output_type IN ('prediction', 'recommendation', 'alert', 'summary', 'generation', 'ranking', 'plan')),
    model_confidence REAL,
    uncertainty_displayed BOOLEAN,
    explanation_displayed BOOLEAN,
    override_available BOOLEAN,
    escalation_available BOOLEAN,
    contestation_available BOOLEAN,
    FOREIGN KEY(system_id) REFERENCES ai_interaction_systems(system_id)
);

CREATE TABLE IF NOT EXISTS user_decisions (
    decision_id TEXT PRIMARY KEY,
    presentation_id TEXT NOT NULL,
    user_group_id TEXT,
    decision_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_action TEXT CHECK(user_action IN ('accepted', 'overrode', 'escalated', 'ignored', 'revised', 'contested', 'requested_explanation')),
    decision_time_seconds REAL,
    user_feedback TEXT,
    FOREIGN KEY(presentation_id) REFERENCES interface_presentations(presentation_id),
    FOREIGN KEY(user_group_id) REFERENCES user_groups(user_group_id)
);

CREATE TABLE IF NOT EXISTS interaction_diagnostics (
    diagnostic_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    diagnostic_date DATE NOT NULL,
    user_group_id TEXT,
    risk_level TEXT CHECK(risk_level IN ('low', 'medium', 'high', 'critical', 'unknown')),
    model_accuracy REAL,
    acceptance_rate REAL,
    escalation_rate REAL,
    overreliance_rate REAL,
    underreliance_rate REAL,
    mean_reliance_gap REAL,
    mean_decision_time_seconds REAL,
    review_required BOOLEAN DEFAULT FALSE,
    FOREIGN KEY(system_id) REFERENCES ai_interaction_systems(system_id),
    FOREIGN KEY(user_group_id) REFERENCES user_groups(user_group_id)
);

CREATE TABLE IF NOT EXISTS contestation_events (
    contestation_id TEXT PRIMARY KEY,
    presentation_id TEXT NOT NULL,
    contestation_date DATE NOT NULL,
    issue_summary TEXT NOT NULL,
    review_owner TEXT,
    resolution_status TEXT CHECK(resolution_status IN ('open', 'under_review', 'resolved', 'rejected', 'escalated')),
    remedy_summary TEXT,
    FOREIGN KEY(presentation_id) REFERENCES interface_presentations(presentation_id)
);

CREATE TABLE IF NOT EXISTS design_reviews (
    design_review_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    review_date DATE NOT NULL,
    reviewer TEXT NOT NULL,
    review_scope TEXT,
    mental_model_review_status TEXT,
    accessibility_review_status TEXT,
    explanation_review_status TEXT,
    reliance_risk_review_status TEXT,
    findings TEXT,
    required_actions TEXT,
    FOREIGN KEY(system_id) REFERENCES ai_interaction_systems(system_id)
);
