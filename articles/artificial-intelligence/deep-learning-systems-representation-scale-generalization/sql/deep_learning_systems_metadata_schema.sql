-- Deep Learning Systems Metadata Schema
-- Supports the article "Deep Learning Systems: Representation, Scale, and Generalization"

CREATE TABLE IF NOT EXISTS deep_learning_systems (
    system_id TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    system_purpose TEXT NOT NULL,
    owner_team TEXT NOT NULL,
    risk_tier TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS architectures (
    architecture_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    architecture_family TEXT NOT NULL,
    layer_count INTEGER,
    parameter_count BIGINT,
    attention_based BOOLEAN DEFAULT FALSE,
    residual_connections BOOLEAN DEFAULT FALSE,
    notes TEXT,
    FOREIGN KEY(system_id) REFERENCES deep_learning_systems(system_id)
);

CREATE TABLE IF NOT EXISTS datasets (
    dataset_id TEXT PRIMARY KEY,
    dataset_name TEXT NOT NULL,
    data_source TEXT NOT NULL,
    modality TEXT,
    token_or_example_count BIGINT,
    data_license TEXT,
    contains_sensitive_data BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS training_runs (
    training_run_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    architecture_id TEXT NOT NULL,
    dataset_id TEXT NOT NULL,
    optimizer TEXT,
    learning_rate REAL,
    batch_size INTEGER,
    compute_budget_notes TEXT,
    hardware_notes TEXT,
    git_commit_hash TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(system_id) REFERENCES deep_learning_systems(system_id),
    FOREIGN KEY(architecture_id) REFERENCES architectures(architecture_id),
    FOREIGN KEY(dataset_id) REFERENCES datasets(dataset_id)
);

CREATE TABLE IF NOT EXISTS evaluation_runs (
    evaluation_id TEXT PRIMARY KEY,
    training_run_id TEXT NOT NULL,
    evaluation_date DATE NOT NULL,
    benchmark_name TEXT,
    train_loss REAL,
    validation_loss REAL,
    test_loss REAL,
    accuracy REAL,
    calibration_error REAL,
    robustness_notes TEXT,
    FOREIGN KEY(training_run_id) REFERENCES training_runs(training_run_id)
);

CREATE TABLE IF NOT EXISTS scaling_experiments (
    scaling_experiment_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    scale_axis TEXT CHECK(scale_axis IN ('parameters', 'data', 'compute', 'mixed')),
    scale_value REAL,
    observed_loss REAL,
    estimated_exponent REAL,
    notes TEXT,
    FOREIGN KEY(system_id) REFERENCES deep_learning_systems(system_id)
);

CREATE TABLE IF NOT EXISTS monitoring_events (
    monitoring_event_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    event_date DATE NOT NULL,
    metric_name TEXT NOT NULL,
    metric_value REAL,
    threshold_value REAL,
    alert_level TEXT,
    remediation_status TEXT,
    FOREIGN KEY(system_id) REFERENCES deep_learning_systems(system_id)
);
