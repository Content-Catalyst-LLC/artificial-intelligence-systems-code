-- AI Article Governance Schema
-- Supports the article "What Is Artificial Intelligence?"

CREATE TABLE IF NOT EXISTS ai_systems (
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
    contains_sensitive_attributes BOOLEAN DEFAULT FALSE,
    data_license TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS model_versions (
    model_version_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    model_family TEXT NOT NULL,
    training_dataset_id TEXT NOT NULL,
    training_date DATE NOT NULL,
    git_commit_hash TEXT,
    model_card_url TEXT,
    FOREIGN KEY(system_id) REFERENCES ai_systems(system_id),
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
    notes TEXT,
    FOREIGN KEY(model_version_id) REFERENCES model_versions(model_version_id),
    FOREIGN KEY(evaluation_dataset_id) REFERENCES datasets(dataset_id)
);

CREATE TABLE IF NOT EXISTS subgroup_diagnostics (
    diagnostic_id TEXT PRIMARY KEY,
    evaluation_id TEXT NOT NULL,
    subgroup_name TEXT NOT NULL,
    subgroup_value TEXT NOT NULL,
    sample_size INTEGER NOT NULL,
    selection_rate REAL,
    false_positive_rate REAL,
    false_negative_rate REAL,
    FOREIGN KEY(evaluation_id) REFERENCES evaluation_runs(evaluation_id)
);
