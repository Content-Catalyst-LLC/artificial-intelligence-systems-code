-- Model Validation, Benchmarking, and Generalization Theory Metadata Schema

CREATE TABLE IF NOT EXISTS validation_projects (
    project_id TEXT PRIMARY KEY,
    project_name TEXT NOT NULL,
    model_family TEXT,
    intended_use TEXT NOT NULL,
    validation_owner TEXT NOT NULL,
    deployment_context TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS model_versions (
    model_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    model_name TEXT NOT NULL,
    model_version TEXT NOT NULL,
    training_date DATE,
    algorithm_type TEXT,
    feature_set_version TEXT,
    hyperparameter_summary TEXT,
    FOREIGN KEY(project_id) REFERENCES validation_projects(project_id)
);

CREATE TABLE IF NOT EXISTS dataset_splits (
    split_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    dataset_name TEXT NOT NULL,
    split_name TEXT CHECK(split_name IN ('train', 'validation', 'test', 'external_validation', 'shifted_deployment', 'benchmark', 'shadow_deployment')),
    split_method TEXT,
    sample_size INTEGER,
    time_period TEXT,
    population_description TEXT,
    leakage_risk_notes TEXT,
    FOREIGN KEY(project_id) REFERENCES validation_projects(project_id)
);

CREATE TABLE IF NOT EXISTS validation_runs (
    run_id TEXT PRIMARY KEY,
    model_id TEXT NOT NULL,
    split_id TEXT NOT NULL,
    run_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metric_name TEXT NOT NULL,
    metric_value REAL NOT NULL,
    confidence_interval_lower REAL,
    confidence_interval_upper REAL,
    subgroup TEXT,
    notes TEXT,
    FOREIGN KEY(model_id) REFERENCES model_versions(model_id),
    FOREIGN KEY(split_id) REFERENCES dataset_splits(split_id)
);

CREATE TABLE IF NOT EXISTS calibration_metrics (
    calibration_id TEXT PRIMARY KEY,
    model_id TEXT NOT NULL,
    split_id TEXT NOT NULL,
    bin_count INTEGER,
    expected_calibration_error REAL,
    maximum_calibration_error REAL,
    brier_score REAL,
    calibration_notes TEXT,
    FOREIGN KEY(model_id) REFERENCES model_versions(model_id),
    FOREIGN KEY(split_id) REFERENCES dataset_splits(split_id)
);

CREATE TABLE IF NOT EXISTS benchmark_runs (
    benchmark_run_id TEXT PRIMARY KEY,
    model_id TEXT NOT NULL,
    benchmark_name TEXT NOT NULL,
    benchmark_version TEXT,
    benchmark_task TEXT,
    benchmark_score REAL,
    benchmark_ceiling_estimate REAL,
    saturation_indicator REAL,
    contamination_risk_notes TEXT,
    FOREIGN KEY(model_id) REFERENCES model_versions(model_id)
);

CREATE TABLE IF NOT EXISTS shift_tests (
    shift_test_id TEXT PRIMARY KEY,
    model_id TEXT NOT NULL,
    source_split_id TEXT NOT NULL,
    target_split_id TEXT NOT NULL,
    shift_type TEXT CHECK(shift_type IN ('covariate_shift', 'label_shift', 'concept_drift', 'domain_shift', 'selection_shift', 'unknown')),
    source_metric_value REAL,
    target_metric_value REAL,
    degradation_value REAL,
    monitoring_recommendation TEXT,
    FOREIGN KEY(model_id) REFERENCES model_versions(model_id),
    FOREIGN KEY(source_split_id) REFERENCES dataset_splits(split_id),
    FOREIGN KEY(target_split_id) REFERENCES dataset_splits(split_id)
);

CREATE TABLE IF NOT EXISTS governance_reviews (
    review_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    review_date DATE NOT NULL,
    reviewer TEXT NOT NULL,
    intended_use_reviewed BOOLEAN DEFAULT FALSE,
    split_design_reviewed BOOLEAN DEFAULT FALSE,
    metric_alignment_reviewed BOOLEAN DEFAULT FALSE,
    external_validation_reviewed BOOLEAN DEFAULT FALSE,
    calibration_reviewed BOOLEAN DEFAULT FALSE,
    shift_reviewed BOOLEAN DEFAULT FALSE,
    benchmark_limitations_reviewed BOOLEAN DEFAULT FALSE,
    findings TEXT,
    required_actions TEXT,
    status TEXT CHECK(status IN ('draft', 'approved', 'requires_action', 'closed')),
    FOREIGN KEY(project_id) REFERENCES validation_projects(project_id)
);
