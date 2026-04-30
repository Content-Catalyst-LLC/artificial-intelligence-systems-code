-- Trust, Interpretability, and User-Centered AI Systems Metadata Schema

CREATE TABLE IF NOT EXISTS ai_systems (
    system_id TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    system_purpose TEXT NOT NULL,
    owner_team TEXT NOT NULL,
    deployment_status TEXT CHECK(deployment_status IN ('proposed', 'development', 'pilot', 'production', 'paused', 'retired')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS user_groups (
    user_group_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    group_name TEXT NOT NULL,
    role_description TEXT,
    expertise_level TEXT CHECK(expertise_level IN ('novice', 'intermediate', 'expert', 'mixed', 'unknown')),
    accessibility_needs TEXT,
    workflow_context TEXT,
    FOREIGN KEY(system_id) REFERENCES ai_systems(system_id)
);

CREATE TABLE IF NOT EXISTS ai_outputs (
    output_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    model_version TEXT,
    output_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    input_reference TEXT,
    output_type TEXT CHECK(output_type IN ('prediction', 'recommendation', 'classification', 'summary', 'generation', 'ranking', 'alert')),
    model_confidence REAL,
    uncertainty_summary TEXT,
    within_validated_scope BOOLEAN,
    FOREIGN KEY(system_id) REFERENCES ai_systems(system_id)
);

CREATE TABLE IF NOT EXISTS explanations (
    explanation_id TEXT PRIMARY KEY,
    output_id TEXT NOT NULL,
    explanation_type TEXT CHECK(explanation_type IN ('feature_attribution', 'counterfactual', 'example_based', 'rule_based', 'evidence_based', 'process_trace', 'uncertainty', 'other')),
    explanation_text TEXT,
    evidence_reference TEXT,
    fidelity_score REAL,
    usefulness_score REAL,
    actionability_score REAL,
    stability_score REAL,
    FOREIGN KEY(output_id) REFERENCES ai_outputs(output_id)
);

CREATE TABLE IF NOT EXISTS user_interactions (
    interaction_id TEXT PRIMARY KEY,
    output_id TEXT NOT NULL,
    user_group_id TEXT,
    interaction_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_action TEXT CHECK(user_action IN ('accepted', 'overrode', 'escalated', 'ignored', 'requested_explanation', 'contested', 'corrected')),
    decision_time_seconds REAL,
    user_feedback TEXT,
    FOREIGN KEY(output_id) REFERENCES ai_outputs(output_id),
    FOREIGN KEY(user_group_id) REFERENCES user_groups(user_group_id)
);

CREATE TABLE IF NOT EXISTS reliance_diagnostics (
    diagnostic_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    diagnostic_date DATE NOT NULL,
    user_group_id TEXT,
    risk_level TEXT CHECK(risk_level IN ('low', 'medium', 'high', 'critical', 'unknown')),
    model_accuracy REAL,
    user_reliance_rate REAL,
    overreliance_rate REAL,
    underreliance_rate REAL,
    mean_reliance_gap REAL,
    review_required BOOLEAN DEFAULT FALSE,
    FOREIGN KEY(system_id) REFERENCES ai_systems(system_id),
    FOREIGN KEY(user_group_id) REFERENCES user_groups(user_group_id)
);

CREATE TABLE IF NOT EXISTS contestation_events (
    contestation_id TEXT PRIMARY KEY,
    output_id TEXT NOT NULL,
    contestation_date DATE NOT NULL,
    contestation_type TEXT,
    issue_summary TEXT NOT NULL,
    review_owner TEXT,
    resolution_status TEXT CHECK(resolution_status IN ('open', 'under_review', 'resolved', 'rejected', 'escalated')),
    remedy_summary TEXT,
    FOREIGN KEY(output_id) REFERENCES ai_outputs(output_id)
);

CREATE TABLE IF NOT EXISTS design_reviews (
    design_review_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    review_date DATE NOT NULL,
    reviewer TEXT NOT NULL,
    review_scope TEXT,
    human_centered_design_status TEXT CHECK(human_centered_design_status IN ('draft', 'partial', 'complete', 'requires_revision')),
    accessibility_review_status TEXT,
    explanation_review_status TEXT,
    findings TEXT,
    required_actions TEXT,
    FOREIGN KEY(system_id) REFERENCES ai_systems(system_id)
);
