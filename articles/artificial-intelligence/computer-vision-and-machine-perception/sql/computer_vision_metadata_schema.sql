-- Computer Vision Metadata Schema
-- Supports the article "Computer Vision and Machine Perception"

CREATE TABLE IF NOT EXISTS vision_systems (
    system_id TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    system_purpose TEXT NOT NULL,
    owner_team TEXT NOT NULL,
    risk_tier TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS image_datasets (
    dataset_id TEXT PRIMARY KEY,
    dataset_name TEXT NOT NULL,
    data_source TEXT NOT NULL,
    image_domain TEXT,
    label_method TEXT,
    contains_sensitive_data BOOLEAN DEFAULT FALSE,
    consent_or_license_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS vision_model_versions (
    model_version_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    model_family TEXT NOT NULL,
    architecture_notes TEXT,
    training_dataset_id TEXT,
    model_card_url TEXT,
    git_commit_hash TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(system_id) REFERENCES vision_systems(system_id),
    FOREIGN KEY(training_dataset_id) REFERENCES image_datasets(dataset_id)
);

CREATE TABLE IF NOT EXISTS vision_evaluation_runs (
    evaluation_id TEXT PRIMARY KEY,
    model_version_id TEXT NOT NULL,
    evaluation_date DATE NOT NULL,
    evaluation_dataset_id TEXT,
    accuracy REAL,
    precision_score REAL,
    recall_score REAL,
    f1_score REAL,
    mean_iou REAL,
    mean_average_precision REAL,
    notes TEXT,
    FOREIGN KEY(model_version_id) REFERENCES vision_model_versions(model_version_id),
    FOREIGN KEY(evaluation_dataset_id) REFERENCES image_datasets(dataset_id)
);

CREATE TABLE IF NOT EXISTS vision_subgroup_diagnostics (
    diagnostic_id TEXT PRIMARY KEY,
    evaluation_id TEXT NOT NULL,
    subgroup_name TEXT NOT NULL,
    subgroup_value TEXT NOT NULL,
    condition_name TEXT,
    sample_size INTEGER NOT NULL,
    classification_error_rate REAL,
    false_positive_rate REAL,
    false_negative_rate REAL,
    mean_iou REAL,
    FOREIGN KEY(evaluation_id) REFERENCES vision_evaluation_runs(evaluation_id)
);
