-- Model Training, Optimization, and Evaluation Metadata Schema

CREATE TABLE IF NOT EXISTS ml_systems (
    system_id TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    system_purpose TEXT NOT NULL,
    owner_team TEXT NOT NULL,
    risk_tier TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS datasets (
    dataset_id TEXT PRIMARY KEY,
    dataset_name TEXT NOT NULL,
    data_source TEXT NOT NULL,
    split_role TEXT CHECK(split_role IN ('train', 'validation', 'test', 'monitoring')),
    data_version TEXT,
    contains_sensitive_data BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS training_runs (
    training_run_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    training_dataset_id TEXT NOT NULL,
    model_family TEXT NOT NULL,
    loss_function TEXT NOT NULL,
    optimizer TEXT NOT NULL,
    learning_rate REAL,
    batch_size INTEGER,
    max_epochs INTEGER,
    early_stopping BOOLEAN DEFAULT FALSE,
    git_commit_hash TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(system_id) REFERENCES ml_systems(system_id),
    FOREIGN KEY(training_dataset_id) REFERENCES datasets(dataset_id)
);

CREATE TABLE IF NOT EXISTS model_versions (
    model_version_id TEXT PRIMARY KEY,
    training_run_id TEXT NOT NULL,
    model_card_url TEXT,
    artifact_uri TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(training_run_id) REFERENCES training_runs(training_run_id)
);

CREATE TABLE IF NOT EXISTS evaluation_runs (
    evaluation_id TEXT PRIMARY KEY,
    model_version_id TEXT NOT NULL,
    evaluation_dataset_id TEXT NOT NULL,
    evaluation_date DATE NOT NULL,
    accuracy REAL,
    precision_score REAL,
    recall_score REAL,
    f1_score REAL,
    roc_auc REAL,
    expected_calibration_error REAL,
    notes TEXT,
    FOREIGN KEY(model_version_id) REFERENCES model_versions(model_version_id),
    FOREIGN KEY(evaluation_dataset_id) REFERENCES datasets(dataset_id)
);

CREATE TABLE IF NOT EXISTS subgroup_diagnostics (
    diagnostic_id TEXT PRIMARY KEY,
    evaluation_id TEXT NOT NULL,
    subgroup_name TEXT NOT NULL,
    subgroup_value TEXT NOT NULL,
    condition_name TEXT,
    sample_size INTEGER NOT NULL,
    classification_error_rate REAL,
    false_positive_rate REAL,
    false_negative_rate REAL,
    calibration_error REAL,
    FOREIGN KEY(evaluation_id) REFERENCES evaluation_runs(evaluation_id)
);

CREATE TABLE IF NOT EXISTS monitoring_events (
    monitoring_event_id TEXT PRIMARY KEY,
    model_version_id TEXT NOT NULL,
    event_date DATE NOT NULL,
    metric_name TEXT NOT NULL,
    metric_value REAL NOT NULL,
    threshold_value REAL,
    alert_level TEXT,
    remediation_status TEXT,
    FOREIGN KEY(model_version_id) REFERENCES model_versions(model_version_id)
);
