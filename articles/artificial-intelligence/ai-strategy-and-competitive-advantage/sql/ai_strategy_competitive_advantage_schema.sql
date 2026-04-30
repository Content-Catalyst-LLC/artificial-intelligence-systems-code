-- AI Strategy and Competitive Advantage Metadata Schema

CREATE TABLE IF NOT EXISTS ai_strategy_portfolios (
    portfolio_id TEXT PRIMARY KEY,
    portfolio_name TEXT NOT NULL,
    organization_unit TEXT,
    strategy_owner TEXT NOT NULL,
    review_cycle TEXT CHECK(review_cycle IN ('monthly', 'quarterly', 'semiannual', 'annual', 'ad_hoc')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ai_initiatives (
    initiative_id TEXT PRIMARY KEY,
    portfolio_id TEXT NOT NULL,
    initiative_name TEXT NOT NULL,
    business_function TEXT,
    initiative_type TEXT CHECK(initiative_type IN ('automation', 'decision_support', 'product_feature', 'platform_capability', 'data_product', 'agentic_workflow', 'governance', 'other')),
    deployment_stage TEXT CHECK(deployment_stage IN ('idea', 'pilot', 'scale_up', 'production', 'paused', 'retired')),
    strategic_objective TEXT,
    FOREIGN KEY(portfolio_id) REFERENCES ai_strategy_portfolios(portfolio_id)
);

CREATE TABLE IF NOT EXISTS strategic_scores (
    score_id TEXT PRIMARY KEY,
    initiative_id TEXT NOT NULL,
    score_date DATE NOT NULL,
    business_value REAL,
    defensibility REAL,
    data_readiness REAL,
    workflow_fit REAL,
    governance_maturity REAL,
    platform_dependence REAL,
    value_capture REAL,
    capability_score REAL,
    strategic_advantage_score REAL,
    priority_band TEXT CHECK(priority_band IN ('low', 'medium', 'high', 'critical')),
    FOREIGN KEY(initiative_id) REFERENCES ai_initiatives(initiative_id)
);

CREATE TABLE IF NOT EXISTS vrio_resources (
    resource_id TEXT PRIMARY KEY,
    initiative_id TEXT NOT NULL,
    resource_name TEXT NOT NULL,
    resource_type TEXT CHECK(resource_type IN ('data', 'workflow', 'model', 'distribution', 'brand_trust', 'talent', 'governance', 'customer_relationship', 'infrastructure', 'other')),
    valuable_score REAL,
    rare_score REAL,
    hard_to_imitate_score REAL,
    organizational_support_score REAL,
    vrio_score REAL,
    notes TEXT,
    FOREIGN KEY(initiative_id) REFERENCES ai_initiatives(initiative_id)
);

CREATE TABLE IF NOT EXISTS sourcing_decisions (
    sourcing_decision_id TEXT PRIMARY KEY,
    initiative_id TEXT NOT NULL,
    sourcing_option TEXT CHECK(sourcing_option IN ('make', 'buy', 'partner', 'hybrid')),
    control_score REAL,
    defensibility_score REAL,
    speed_score REAL,
    cost_score REAL,
    strategic_risk_score REAL,
    sourcing_fit_score REAL,
    rationale TEXT,
    FOREIGN KEY(initiative_id) REFERENCES ai_initiatives(initiative_id)
);

CREATE TABLE IF NOT EXISTS platform_dependencies (
    dependency_id TEXT PRIMARY KEY,
    initiative_id TEXT NOT NULL,
    provider_name TEXT,
    dependency_layer TEXT CHECK(dependency_layer IN ('cloud', 'model_api', 'data', 'identity', 'distribution', 'workflow_platform', 'security', 'other')),
    criticality REAL,
    substitutability REAL,
    switching_cost REAL,
    dependency_risk_score REAL,
    mitigation_plan TEXT,
    FOREIGN KEY(initiative_id) REFERENCES ai_initiatives(initiative_id)
);

CREATE TABLE IF NOT EXISTS governance_reviews (
    review_id TEXT PRIMARY KEY,
    initiative_id TEXT NOT NULL,
    review_date DATE NOT NULL,
    reviewer TEXT NOT NULL,
    review_scope TEXT,
    data_governance_reviewed BOOLEAN DEFAULT FALSE,
    model_risk_reviewed BOOLEAN DEFAULT FALSE,
    human_oversight_reviewed BOOLEAN DEFAULT FALSE,
    value_capture_reviewed BOOLEAN DEFAULT FALSE,
    sourcing_reviewed BOOLEAN DEFAULT FALSE,
    findings TEXT,
    required_actions TEXT,
    status TEXT CHECK(status IN ('draft', 'approved', 'requires_action', 'closed')),
    FOREIGN KEY(initiative_id) REFERENCES ai_initiatives(initiative_id)
);
