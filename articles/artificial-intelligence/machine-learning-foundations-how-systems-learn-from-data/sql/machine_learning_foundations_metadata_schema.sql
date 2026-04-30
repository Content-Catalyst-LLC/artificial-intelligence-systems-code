-- Machine Learning Foundations Metadata Schema

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
    system_id TEXT NOT NULL,
    dataset_name TEXT NOT NULL,
    data_source TEXT NOT NULL,
    dataset_role TEXT CHECK(dataset_role IN ('train', 'validation', 'test', 'monitoring', 'reference')),
    data_version TEXT,
    contains_sensitive_data BOOLEAN DEFAULT FALSE,
    provenance_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(system_id) REFERENCES ml_systems(system_id)
);

CREATE TABLE IF NOT EXISTS feature_sets (
    feature_set_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    feature_set_name TEXT NOT NULL,
    representation_type TEXT CHECK(representation_type IN ('engineered_features', 'embeddings', 'raw_inputs', 'hybrid')),
    preprocessing_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(system_id) REFERENCES ml_systems(system_id)
);

CREATE TABLE IF NOT EXISTS model_versions (
    model_version_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    model_family TEXT NOT NULL,
    feature_set_id TEXT,
    objective_name TEXT NOT NULL,
    model_card_url TEXT,
    git_commit_hash TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(system_id) REFERENCES ml_systems(system_id),
    FOREIGN KEY(feature_set_id) REFERENCES feature_sets(feature_set_id)
);

CREATE TABLE IF NOT EXISTS training_runs (
    training_run_id TEXT PRIMARY KEY,
    model_version_id TEXT NOT NULL,
    training_dataset_id TEXT NOT NULL,
    optimizer TEXT,
    loss_function TEXT,
    learning_rate REAL,
    batch_size INTEGER,
    random_seed INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(model_version_id) REFERENCES model_versions(model_version_id),
    FOREIGN KEY(training_dataset_id) REFERENCES datasets(dataset_id)
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
    calibration_error REAL,
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
    metric_value REAL,
    threshold_value REAL,
    alert_level TEXT,
    remediation_status TEXT,
    FOREIGN KEY(model_version_id) REFERENCES model_versions(model_version_id)
);
