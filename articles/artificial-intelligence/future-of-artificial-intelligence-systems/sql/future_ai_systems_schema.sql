-- The Future of Artificial Intelligence Systems Metadata Schema

CREATE TABLE IF NOT EXISTS ai_future_scenarios (
    scenario_id TEXT PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    scenario_description TEXT NOT NULL,
    time_horizon TEXT,
    scenario_owner TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS scenario_dimensions (
    dimension_id TEXT PRIMARY KEY,
    scenario_id TEXT NOT NULL,
    dimension_name TEXT CHECK(dimension_name IN ('capability', 'infrastructure', 'governance', 'resilience', 'legitimacy', 'systemic_risk', 'cost', 'energy', 'data_quality', 'human_agency', 'other')),
    score REAL,
    confidence_level TEXT CHECK(confidence_level IN ('low', 'medium', 'high', 'unknown')),
    rationale TEXT,
    FOREIGN KEY(scenario_id) REFERENCES ai_future_scenarios(scenario_id)
);

CREATE TABLE IF NOT EXISTS ai_system_options (
    system_id TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    system_type TEXT CHECK(system_type IN ('centralized_frontier', 'specialized_model', 'distributed_edge', 'hybrid_platform', 'agentic_stack', 'public_infrastructure', 'other')),
    capability_score REAL,
    efficiency_score REAL,
    governance_capacity_score REAL,
    trust_score REAL,
    systemic_risk_score REAL,
    cost_score REAL,
    system_fitness_score REAL,
    governance_warning BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS scaling_assumptions (
    assumption_id TEXT PRIMARY KEY,
    system_id TEXT,
    scale_variable TEXT,
    loss_floor REAL,
    scaling_exponent REAL,
    compute_budget_description TEXT,
    data_budget_description TEXT,
    notes TEXT,
    FOREIGN KEY(system_id) REFERENCES ai_system_options(system_id)
);

CREATE TABLE IF NOT EXISTS future_constraints (
    constraint_id TEXT PRIMARY KEY,
    system_id TEXT,
    constraint_type TEXT CHECK(constraint_type IN ('compute', 'energy', 'data', 'governance', 'trust', 'regulatory', 'security', 'economic', 'institutional', 'other')),
    constraint_description TEXT NOT NULL,
    severity TEXT CHECK(severity IN ('low', 'medium', 'high', 'critical', 'unknown')),
    mitigation_strategy TEXT,
    FOREIGN KEY(system_id) REFERENCES ai_system_options(system_id)
);

CREATE TABLE IF NOT EXISTS systemic_risk_indicators (
    risk_id TEXT PRIMARY KEY,
    scenario_id TEXT,
    risk_name TEXT NOT NULL,
    risk_type TEXT CHECK(risk_type IN ('dependency_concentration', 'feedback_loop', 'model_monoculture', 'governance_lag', 'automation_bias', 'adversarial_failure', 'infrastructure_failure', 'other')),
    likelihood REAL,
    impact REAL,
    mitigation_readiness REAL,
    notes TEXT,
    FOREIGN KEY(scenario_id) REFERENCES ai_future_scenarios(scenario_id)
);

CREATE TABLE IF NOT EXISTS governance_readiness_reviews (
    review_id TEXT PRIMARY KEY,
    system_id TEXT,
    review_date DATE NOT NULL,
    reviewer TEXT NOT NULL,
    capability_reviewed BOOLEAN DEFAULT FALSE,
    infrastructure_reviewed BOOLEAN DEFAULT FALSE,
    risk_reviewed BOOLEAN DEFAULT FALSE,
    responsible_scaling_reviewed BOOLEAN DEFAULT FALSE,
    human_oversight_reviewed BOOLEAN DEFAULT FALSE,
    deployment_constraints_reviewed BOOLEAN DEFAULT FALSE,
    findings TEXT,
    required_actions TEXT,
    status TEXT CHECK(status IN ('draft', 'approved', 'requires_action', 'closed')),
    FOREIGN KEY(system_id) REFERENCES ai_system_options(system_id)
);
