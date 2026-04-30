-- Economics of AI Systems and Platform Power Metadata Schema

CREATE TABLE IF NOT EXISTS ai_economic_ecosystems (
    ecosystem_id TEXT PRIMARY KEY,
    ecosystem_name TEXT NOT NULL,
    analysis_scope TEXT,
    analyst TEXT NOT NULL,
    review_cycle TEXT CHECK(review_cycle IN ('monthly', 'quarterly', 'semiannual', 'annual', 'ad_hoc')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ai_value_chain_actors (
    actor_id TEXT PRIMARY KEY,
    ecosystem_id TEXT NOT NULL,
    actor_name TEXT NOT NULL,
    value_chain_layer TEXT CHECK(value_chain_layer IN ('data', 'compute', 'cloud', 'model', 'application', 'distribution', 'user', 'governance', 'other')),
    market_share REAL,
    captured_surplus REAL,
    notes TEXT,
    FOREIGN KEY(ecosystem_id) REFERENCES ai_economic_ecosystems(ecosystem_id)
);

CREATE TABLE IF NOT EXISTS platform_power_scores (
    score_id TEXT PRIMARY KEY,
    actor_id TEXT NOT NULL,
    score_date DATE NOT NULL,
    data_control REAL,
    compute_control REAL,
    distribution_control REAL,
    switching_costs REAL,
    gatekeeping_power REAL,
    interoperability_score REAL,
    platform_power_score REAL,
    FOREIGN KEY(actor_id) REFERENCES ai_value_chain_actors(actor_id)
);

CREATE TABLE IF NOT EXISTS dependency_scores (
    dependency_id TEXT PRIMARY KEY,
    ecosystem_id TEXT NOT NULL,
    downstream_actor_id TEXT NOT NULL,
    upstream_actor_id TEXT NOT NULL,
    dependency_layer TEXT CHECK(dependency_layer IN ('compute', 'cloud', 'model_api', 'data', 'identity', 'distribution', 'security', 'payments', 'other')),
    criticality REAL,
    substitutability REAL,
    switching_cost REAL,
    dependency_risk_score REAL,
    mitigation_plan TEXT,
    FOREIGN KEY(ecosystem_id) REFERENCES ai_economic_ecosystems(ecosystem_id),
    FOREIGN KEY(downstream_actor_id) REFERENCES ai_value_chain_actors(actor_id),
    FOREIGN KEY(upstream_actor_id) REFERENCES ai_value_chain_actors(actor_id)
);

CREATE TABLE IF NOT EXISTS value_capture_estimates (
    estimate_id TEXT PRIMARY KEY,
    ecosystem_id TEXT NOT NULL,
    actor_id TEXT NOT NULL,
    estimate_date DATE NOT NULL,
    created_surplus REAL,
    captured_surplus REAL,
    value_capture_share REAL,
    surplus_shift_notes TEXT,
    FOREIGN KEY(ecosystem_id) REFERENCES ai_economic_ecosystems(ecosystem_id),
    FOREIGN KEY(actor_id) REFERENCES ai_value_chain_actors(actor_id)
);

CREATE TABLE IF NOT EXISTS concentration_metrics (
    metric_id TEXT PRIMARY KEY,
    ecosystem_id TEXT NOT NULL,
    metric_date DATE NOT NULL,
    concentration_type TEXT CHECK(concentration_type IN ('market_share', 'compute_dependency', 'cloud_dependency', 'model_api_dependency', 'distribution_dependency', 'data_dependency')),
    concentration_score REAL,
    top_actor_share REAL,
    top_three_actor_share REAL,
    interpretation TEXT,
    FOREIGN KEY(ecosystem_id) REFERENCES ai_economic_ecosystems(ecosystem_id)
);

CREATE TABLE IF NOT EXISTS governance_reviews (
    review_id TEXT PRIMARY KEY,
    ecosystem_id TEXT NOT NULL,
    review_date DATE NOT NULL,
    reviewer TEXT NOT NULL,
    review_scope TEXT,
    value_chain_reviewed BOOLEAN DEFAULT FALSE,
    concentration_reviewed BOOLEAN DEFAULT FALSE,
    interoperability_reviewed BOOLEAN DEFAULT FALSE,
    compute_dependency_reviewed BOOLEAN DEFAULT FALSE,
    value_capture_reviewed BOOLEAN DEFAULT FALSE,
    findings TEXT,
    required_actions TEXT,
    status TEXT CHECK(status IN ('draft', 'approved', 'requires_action', 'closed')),
    FOREIGN KEY(ecosystem_id) REFERENCES ai_economic_ecosystems(ecosystem_id)
);
