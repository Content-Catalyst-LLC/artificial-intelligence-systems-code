-- Systemic Risk, Feedback Loops, and Cascading Failures in AI Systems Metadata Schema

CREATE TABLE IF NOT EXISTS ai_systems (
    system_id TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    system_purpose TEXT NOT NULL,
    owner_team TEXT NOT NULL,
    sector TEXT,
    deployment_status TEXT CHECK(deployment_status IN ('proposed', 'development', 'pilot', 'production', 'paused', 'retired')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS system_components (
    component_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    component_name TEXT NOT NULL,
    component_type TEXT CHECK(component_type IN ('model', 'dataset', 'api', 'cloud_service', 'workflow', 'human_review', 'agent', 'tool', 'monitoring', 'governance', 'other')),
    provider_name TEXT,
    criticality_level TEXT CHECK(criticality_level IN ('low', 'medium', 'high', 'critical')),
    fallback_available BOOLEAN DEFAULT FALSE,
    FOREIGN KEY(system_id) REFERENCES ai_systems(system_id)
);

CREATE TABLE IF NOT EXISTS dependencies (
    dependency_id TEXT PRIMARY KEY,
    upstream_component_id TEXT NOT NULL,
    downstream_component_id TEXT NOT NULL,
    dependency_type TEXT CHECK(dependency_type IN ('data', 'model', 'api', 'cloud', 'workflow', 'decision', 'identity', 'security', 'human_review', 'other')),
    dependency_weight REAL,
    substitutability TEXT CHECK(substitutability IN ('low', 'medium', 'high', 'unknown')),
    notes TEXT,
    FOREIGN KEY(upstream_component_id) REFERENCES system_components(component_id),
    FOREIGN KEY(downstream_component_id) REFERENCES system_components(component_id)
);

CREATE TABLE IF NOT EXISTS feedback_loops (
    feedback_loop_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    loop_name TEXT NOT NULL,
    source_component_id TEXT,
    target_component_id TEXT,
    feedback_type TEXT CHECK(feedback_type IN ('stabilizing', 'destabilizing', 'self_reinforcing', 'self_correcting', 'unknown')),
    feedback_intensity REAL,
    monitoring_signal TEXT,
    governance_notes TEXT,
    FOREIGN KEY(system_id) REFERENCES ai_systems(system_id),
    FOREIGN KEY(source_component_id) REFERENCES system_components(component_id),
    FOREIGN KEY(target_component_id) REFERENCES system_components(component_id)
);

CREATE TABLE IF NOT EXISTS cascade_scenarios (
    scenario_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    scenario_name TEXT NOT NULL,
    initial_failure_component_id TEXT,
    scenario_description TEXT,
    coupling_level TEXT CHECK(coupling_level IN ('low', 'medium', 'high', 'critical')),
    estimated_cascade_probability REAL,
    estimated_cascade_size REAL,
    buffer_capacity REAL,
    reviewed BOOLEAN DEFAULT FALSE,
    FOREIGN KEY(system_id) REFERENCES ai_systems(system_id),
    FOREIGN KEY(initial_failure_component_id) REFERENCES system_components(component_id)
);

CREATE TABLE IF NOT EXISTS systemic_risk_scores (
    score_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    score_date DATE NOT NULL,
    dependency_intensity REAL,
    feedback_intensity REAL,
    coupling_level REAL,
    provider_concentration REAL,
    buffer_capacity REAL,
    systemic_risk_score REAL,
    risk_band TEXT CHECK(risk_band IN ('low', 'moderate', 'high', 'critical')),
    FOREIGN KEY(system_id) REFERENCES ai_systems(system_id)
);

CREATE TABLE IF NOT EXISTS incident_events (
    incident_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    incident_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    originating_component_id TEXT,
    incident_type TEXT CHECK(incident_type IN ('model_failure', 'data_pipeline_failure', 'provider_outage', 'workflow_cascade', 'agent_error', 'feedback_amplification', 'security_event', 'unknown')),
    severity TEXT CHECK(severity IN ('low', 'medium', 'high', 'critical')),
    propagation_observed BOOLEAN DEFAULT FALSE,
    containment_action TEXT,
    resolution_status TEXT CHECK(resolution_status IN ('open', 'contained', 'resolved', 'accepted_risk', 'escalated')),
    notes TEXT,
    FOREIGN KEY(system_id) REFERENCES ai_systems(system_id),
    FOREIGN KEY(originating_component_id) REFERENCES system_components(component_id)
);

CREATE TABLE IF NOT EXISTS governance_reviews (
    review_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    review_date DATE NOT NULL,
    reviewer TEXT NOT NULL,
    review_scope TEXT,
    dependency_map_reviewed BOOLEAN DEFAULT FALSE,
    feedback_loops_reviewed BOOLEAN DEFAULT FALSE,
    cascade_scenarios_reviewed BOOLEAN DEFAULT FALSE,
    concentration_risk_reviewed BOOLEAN DEFAULT FALSE,
    findings TEXT,
    required_actions TEXT,
    status TEXT CHECK(status IN ('draft', 'approved', 'requires_action', 'closed')),
    FOREIGN KEY(system_id) REFERENCES ai_systems(system_id)
);
