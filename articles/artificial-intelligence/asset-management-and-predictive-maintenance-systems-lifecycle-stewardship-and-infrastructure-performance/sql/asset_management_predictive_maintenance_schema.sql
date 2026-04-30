-- Asset Management and Predictive Maintenance Systems Metadata Schema

CREATE TABLE IF NOT EXISTS asset_portfolios (
    portfolio_id TEXT PRIMARY KEY,
    portfolio_name TEXT NOT NULL,
    owner_organization TEXT NOT NULL,
    service_domain TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS assets (
    asset_id TEXT PRIMARY KEY,
    portfolio_id TEXT NOT NULL,
    asset_name TEXT NOT NULL,
    asset_class TEXT NOT NULL,
    parent_asset_id TEXT,
    location_description TEXT,
    install_date DATE,
    expected_service_life_years INTEGER,
    criticality_score REAL,
    replacement_cost REAL,
    active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY(portfolio_id) REFERENCES asset_portfolios(portfolio_id),
    FOREIGN KEY(parent_asset_id) REFERENCES assets(asset_id)
);

CREATE TABLE IF NOT EXISTS inspections (
    inspection_id TEXT PRIMARY KEY,
    asset_id TEXT NOT NULL,
    inspection_date DATE NOT NULL,
    inspection_method TEXT,
    condition_score REAL,
    defect_summary TEXT,
    inspector TEXT,
    data_quality_score REAL,
    FOREIGN KEY(asset_id) REFERENCES assets(asset_id)
);

CREATE TABLE IF NOT EXISTS sensor_observations (
    observation_id TEXT PRIMARY KEY,
    asset_id TEXT NOT NULL,
    sensor_type TEXT NOT NULL,
    observation_time TIMESTAMP NOT NULL,
    metric_name TEXT NOT NULL,
    metric_value REAL NOT NULL,
    unit TEXT,
    quality_flag TEXT,
    FOREIGN KEY(asset_id) REFERENCES assets(asset_id)
);

CREATE TABLE IF NOT EXISTS work_orders (
    work_order_id TEXT PRIMARY KEY,
    asset_id TEXT NOT NULL,
    work_order_type TEXT CHECK(work_order_type IN ('inspection', 'preventive', 'condition_based', 'predictive', 'corrective', 'renewal')),
    priority_level TEXT CHECK(priority_level IN ('low', 'medium', 'high', 'critical')),
    requested_date DATE,
    scheduled_date DATE,
    completed_date DATE,
    status TEXT CHECK(status IN ('requested', 'scheduled', 'in_progress', 'complete', 'deferred', 'cancelled')),
    estimated_cost REAL,
    actual_cost REAL,
    notes TEXT,
    FOREIGN KEY(asset_id) REFERENCES assets(asset_id)
);

CREATE TABLE IF NOT EXISTS failure_events (
    failure_id TEXT PRIMARY KEY,
    asset_id TEXT NOT NULL,
    failure_date DATE NOT NULL,
    failure_mode TEXT,
    service_impact TEXT,
    downtime_hours REAL,
    consequence_cost REAL,
    root_cause TEXT,
    FOREIGN KEY(asset_id) REFERENCES assets(asset_id)
);

CREATE TABLE IF NOT EXISTS predictive_scores (
    score_id TEXT PRIMARY KEY,
    asset_id TEXT NOT NULL,
    model_version TEXT NOT NULL,
    score_date DATE NOT NULL,
    failure_probability REAL,
    remaining_useful_life_estimate REAL,
    risk_score REAL,
    priority_score REAL,
    recommended_strategy TEXT,
    confidence_level TEXT,
    FOREIGN KEY(asset_id) REFERENCES assets(asset_id)
);

CREATE TABLE IF NOT EXISTS lifecycle_cost_scenarios (
    scenario_id TEXT PRIMARY KEY,
    asset_id TEXT NOT NULL,
    scenario_name TEXT NOT NULL,
    analysis_start_date DATE,
    analysis_horizon_years INTEGER,
    discount_rate REAL,
    maintenance_cost_present_value REAL,
    renewal_cost_present_value REAL,
    expected_failure_cost_present_value REAL,
    total_lifecycle_cost_present_value REAL,
    FOREIGN KEY(asset_id) REFERENCES assets(asset_id)
);

CREATE TABLE IF NOT EXISTS governance_reviews (
    review_id TEXT PRIMARY KEY,
    portfolio_id TEXT NOT NULL,
    review_date DATE NOT NULL,
    reviewer TEXT NOT NULL,
    review_scope TEXT,
    findings TEXT,
    required_actions TEXT,
    status TEXT CHECK(status IN ('draft', 'approved', 'requires_action', 'closed')),
    FOREIGN KEY(portfolio_id) REFERENCES asset_portfolios(portfolio_id)
);
