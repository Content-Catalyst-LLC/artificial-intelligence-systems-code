-- NLP System Metadata Schema
-- Supports the article "Natural Language Processing and Computational Language Systems"

CREATE TABLE IF NOT EXISTS nlp_systems (
    system_id TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    system_purpose TEXT NOT NULL,
    owner_team TEXT NOT NULL,
    risk_tier TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS text_datasets (
    dataset_id TEXT PRIMARY KEY,
    dataset_name TEXT NOT NULL,
    data_source TEXT NOT NULL,
    language_or_domain TEXT,
    license_or_consent_notes TEXT,
    contains_sensitive_data BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS nlp_model_versions (
    model_version_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    model_family TEXT NOT NULL,
    tokenizer_name TEXT,
    context_window INTEGER,
    training_dataset_id TEXT,
    model_card_url TEXT,
    git_commit_hash TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(system_id) REFERENCES nlp_systems(system_id),
    FOREIGN KEY(training_dataset_id) REFERENCES text_datasets(dataset_id)
);

CREATE TABLE IF NOT EXISTS nlp_evaluation_runs (
    evaluation_id TEXT PRIMARY KEY,
    model_version_id TEXT NOT NULL,
    evaluation_date DATE NOT NULL,
    evaluation_dataset_id TEXT,
    accuracy REAL,
    precision_score REAL,
    recall_score REAL,
    f1_score REAL,
    perplexity REAL,
    hallucination_rate REAL,
    citation_accuracy REAL,
    notes TEXT,
    FOREIGN KEY(model_version_id) REFERENCES nlp_model_versions(model_version_id),
    FOREIGN KEY(evaluation_dataset_id) REFERENCES text_datasets(dataset_id)
);

CREATE TABLE IF NOT EXISTS retrieval_events (
    retrieval_event_id TEXT PRIMARY KEY,
    evaluation_id TEXT NOT NULL,
    query_text TEXT NOT NULL,
    retrieved_document_id TEXT,
    rank_position INTEGER,
    similarity_score REAL,
    judged_relevant BOOLEAN,
    FOREIGN KEY(evaluation_id) REFERENCES nlp_evaluation_runs(evaluation_id)
);

CREATE TABLE IF NOT EXISTS nlp_subgroup_diagnostics (
    diagnostic_id TEXT PRIMARY KEY,
    evaluation_id TEXT NOT NULL,
    subgroup_name TEXT NOT NULL,
    subgroup_value TEXT NOT NULL,
    document_domain TEXT,
    sample_size INTEGER NOT NULL,
    classification_error_rate REAL,
    false_positive_rate REAL,
    false_negative_rate REAL,
    hallucination_rate REAL,
    FOREIGN KEY(evaluation_id) REFERENCES nlp_evaluation_runs(evaluation_id)
);
