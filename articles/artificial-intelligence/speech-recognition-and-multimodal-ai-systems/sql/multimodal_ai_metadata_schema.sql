-- Multimodal AI Metadata Schema
-- Supports the article "Speech Recognition and Multimodal AI Systems"

CREATE TABLE IF NOT EXISTS multimodal_systems (
    system_id TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    system_purpose TEXT NOT NULL,
    owner_team TEXT NOT NULL,
    risk_tier TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS modalities (
    modality_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    modality_name TEXT NOT NULL,
    data_type TEXT NOT NULL,
    sampling_or_resolution TEXT,
    known_limitations TEXT,
    FOREIGN KEY(system_id) REFERENCES multimodal_systems(system_id)
);

CREATE TABLE IF NOT EXISTS datasets (
    dataset_id TEXT PRIMARY KEY,
    dataset_name TEXT NOT NULL,
    modality_id TEXT NOT NULL,
    data_source TEXT NOT NULL,
    consent_or_license_notes TEXT,
    contains_sensitive_data BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(modality_id) REFERENCES modalities(modality_id)
);

CREATE TABLE IF NOT EXISTS model_versions (
    model_version_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    model_family TEXT NOT NULL,
    architecture_notes TEXT,
    training_dataset_id TEXT,
    model_card_url TEXT,
    git_commit_hash TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(system_id) REFERENCES multimodal_systems(system_id),
    FOREIGN KEY(training_dataset_id) REFERENCES datasets(dataset_id)
);

CREATE TABLE IF NOT EXISTS evaluation_runs (
    evaluation_id TEXT PRIMARY KEY,
    model_version_id TEXT NOT NULL,
    evaluation_date DATE NOT NULL,
    evaluation_dataset_id TEXT,
    word_error_rate REAL,
    character_error_rate REAL,
    recall_at_k REAL,
    mean_reciprocal_rank REAL,
    notes TEXT,
    FOREIGN KEY(model_version_id) REFERENCES model_versions(model_version_id),
    FOREIGN KEY(evaluation_dataset_id) REFERENCES datasets(dataset_id)
);

CREATE TABLE IF NOT EXISTS subgroup_speech_diagnostics (
    diagnostic_id TEXT PRIMARY KEY,
    evaluation_id TEXT NOT NULL,
    subgroup_name TEXT NOT NULL,
    subgroup_value TEXT NOT NULL,
    noise_condition TEXT,
    sample_size INTEGER NOT NULL,
    word_error_rate REAL,
    deletion_rate REAL,
    insertion_rate REAL,
    substitution_rate REAL,
    FOREIGN KEY(evaluation_id) REFERENCES evaluation_runs(evaluation_id)
);
