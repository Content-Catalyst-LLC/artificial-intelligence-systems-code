-- Data Quality, Bias, and Measurement in Machine Learning Metadata Schema

CREATE TABLE IF NOT EXISTS data_quality_projects (
    project_id TEXT PRIMARY KEY,
    project_name TEXT NOT NULL,
    intended_model_use TEXT NOT NULL,
    data_owner TEXT NOT NULL,
    governance_owner TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS datasets (
    dataset_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    dataset_name TEXT NOT NULL,
    dataset_version TEXT NOT NULL,
    source_system TEXT,
    collection_period TEXT,
    target_population TEXT,
    known_limitations TEXT,
    appropriate_uses TEXT,
    inappropriate_uses TEXT,
    FOREIGN KEY(project_id) REFERENCES data_quality_projects(project_id)
);

CREATE TABLE IF NOT EXISTS measurement_constructs (
    construct_id TEXT PRIMARY KEY,
    dataset_id TEXT NOT NULL,
    construct_name TEXT NOT NULL,
    latent_construct_description TEXT NOT NULL,
    observed_proxy_variable TEXT NOT NULL,
    construct_validity_notes TEXT,
    measurement_risk_level TEXT CHECK(measurement_risk_level IN ('low', 'medium', 'high', 'unknown')),
    FOREIGN KEY(dataset_id) REFERENCES datasets(dataset_id)
);

CREATE TABLE IF NOT EXISTS data_quality_metrics (
    metric_id TEXT PRIMARY KEY,
    dataset_id TEXT NOT NULL,
    metric_date DATE NOT NULL,
    metric_name TEXT NOT NULL,
    metric_value REAL,
    subgroup TEXT,
    threshold_value REAL,
    status TEXT CHECK(status IN ('pass', 'warning', 'fail', 'not_reviewed')),
    notes TEXT,
    FOREIGN KEY(dataset_id) REFERENCES datasets(dataset_id)
);

CREATE TABLE IF NOT EXISTS bias_audit_findings (
    finding_id TEXT PRIMARY KEY,
    dataset_id TEXT NOT NULL,
    bias_type TEXT CHECK(bias_type IN ('historical_bias', 'representation_bias', 'measurement_bias', 'aggregation_bias', 'learning_bias', 'evaluation_bias', 'deployment_bias', 'other')),
    affected_group TEXT,
    description TEXT NOT NULL,
    severity TEXT CHECK(severity IN ('low', 'medium', 'high', 'critical', 'unknown')),
    mitigation_plan TEXT,
    residual_risk TEXT,
    FOREIGN KEY(dataset_id) REFERENCES datasets(dataset_id)
);

CREATE TABLE IF NOT EXISTS missingness_audits (
    audit_id TEXT PRIMARY KEY,
    dataset_id TEXT NOT NULL,
    variable_name TEXT NOT NULL,
    missing_rate REAL,
    subgroup TEXT,
    missingness_mechanism TEXT CHECK(missingness_mechanism IN ('MCAR', 'MAR', 'MNAR', 'unknown')),
    interpretation TEXT,
    FOREIGN KEY(dataset_id) REFERENCES datasets(dataset_id)
);

CREATE TABLE IF NOT EXISTS fairness_metrics (
    fairness_metric_id TEXT PRIMARY KEY,
    dataset_id TEXT NOT NULL,
    model_version TEXT,
    protected_attribute TEXT NOT NULL,
    subgroup_a TEXT,
    subgroup_b TEXT,
    metric_name TEXT NOT NULL,
    metric_value REAL,
    acceptable_threshold REAL,
    review_notes TEXT,
    FOREIGN KEY(dataset_id) REFERENCES datasets(dataset_id)
);

CREATE TABLE IF NOT EXISTS governance_reviews (
    review_id TEXT PRIMARY KEY,
    dataset_id TEXT NOT NULL,
    review_date DATE NOT NULL,
    reviewer TEXT NOT NULL,
    construct_validity_reviewed BOOLEAN DEFAULT FALSE,
    data_quality_reviewed BOOLEAN DEFAULT FALSE,
    missingness_reviewed BOOLEAN DEFAULT FALSE,
    representation_reviewed BOOLEAN DEFAULT FALSE,
    label_quality_reviewed BOOLEAN DEFAULT FALSE,
    fairness_reviewed BOOLEAN DEFAULT FALSE,
    documentation_reviewed BOOLEAN DEFAULT FALSE,
    findings TEXT,
    required_actions TEXT,
    status TEXT CHECK(status IN ('draft', 'approved', 'requires_action', 'closed')),
    FOREIGN KEY(dataset_id) REFERENCES datasets(dataset_id)
);
