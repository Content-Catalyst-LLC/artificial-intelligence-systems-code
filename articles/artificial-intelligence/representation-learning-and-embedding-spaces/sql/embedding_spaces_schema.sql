-- Representation Learning and Embedding Spaces
-- SQL schema for embedding models, vector indexes, retrieval logs,
-- evaluation sets, drift monitoring, bias review, and governance artifacts.

CREATE TABLE IF NOT EXISTS embedding_model (
    embedding_model_id TEXT PRIMARY KEY,
    model_name TEXT NOT NULL,
    model_version TEXT NOT NULL,
    modality TEXT NOT NULL,
    embedding_dimension INTEGER NOT NULL,
    training_data_summary TEXT,
    intended_use TEXT NOT NULL,
    prohibited_use TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS vector_index (
    vector_index_id TEXT PRIMARY KEY,
    embedding_model_id TEXT NOT NULL,
    index_name TEXT NOT NULL,
    index_type TEXT NOT NULL,
    similarity_metric TEXT NOT NULL,
    object_count INTEGER,
    refresh_cadence TEXT,
    last_refreshed_at TIMESTAMP,
    index_owner TEXT,
    FOREIGN KEY (embedding_model_id) REFERENCES embedding_model(embedding_model_id)
);

CREATE TABLE IF NOT EXISTS embedded_object (
    object_id TEXT PRIMARY KEY,
    vector_index_id TEXT NOT NULL,
    source_uri TEXT,
    object_type TEXT NOT NULL,
    object_title TEXT,
    metadata_payload_uri TEXT,
    embedding_hash TEXT,
    embedding_norm REAL,
    embedded_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vector_index_id) REFERENCES vector_index(vector_index_id)
);

CREATE TABLE IF NOT EXISTS retrieval_query (
    query_id TEXT PRIMARY KEY,
    vector_index_id TEXT NOT NULL,
    query_text_hash TEXT NOT NULL,
    query_modality TEXT,
    query_embedding_hash TEXT,
    user_or_process TEXT,
    query_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vector_index_id) REFERENCES vector_index(vector_index_id)
);

CREATE TABLE IF NOT EXISTS retrieval_result (
    retrieval_result_id TEXT PRIMARY KEY,
    query_id TEXT NOT NULL,
    object_id TEXT NOT NULL,
    rank INTEGER NOT NULL,
    similarity_score REAL NOT NULL,
    retrieval_score REAL,
    clicked INTEGER DEFAULT 0,
    accepted INTEGER DEFAULT 0,
    reviewer_feedback TEXT,
    FOREIGN KEY (query_id) REFERENCES retrieval_query(query_id),
    FOREIGN KEY (object_id) REFERENCES embedded_object(object_id)
);

CREATE TABLE IF NOT EXISTS embedding_evaluation_set (
    evaluation_set_id TEXT PRIMARY KEY,
    vector_index_id TEXT NOT NULL,
    evaluation_name TEXT NOT NULL,
    evaluation_type TEXT NOT NULL,
    query_count INTEGER,
    ground_truth_uri TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vector_index_id) REFERENCES vector_index(vector_index_id)
);

CREATE TABLE IF NOT EXISTS embedding_evaluation_result (
    evaluation_result_id TEXT PRIMARY KEY,
    evaluation_set_id TEXT NOT NULL,
    metric_name TEXT NOT NULL,
    metric_value REAL NOT NULL,
    evaluated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    FOREIGN KEY (evaluation_set_id) REFERENCES embedding_evaluation_set(evaluation_set_id)
);

CREATE TABLE IF NOT EXISTS embedding_bias_review (
    bias_review_id TEXT PRIMARY KEY,
    embedding_model_id TEXT NOT NULL,
    review_type TEXT NOT NULL,
    reviewed_by TEXT,
    review_date DATE NOT NULL,
    finding_summary TEXT NOT NULL,
    mitigation_actions TEXT,
    review_status TEXT NOT NULL,
    FOREIGN KEY (embedding_model_id) REFERENCES embedding_model(embedding_model_id)
);

CREATE TABLE IF NOT EXISTS embedding_drift_record (
    drift_record_id TEXT PRIMARY KEY,
    vector_index_id TEXT NOT NULL,
    drift_metric TEXT NOT NULL,
    drift_value REAL NOT NULL,
    threshold_warning REAL,
    threshold_action REAL,
    drift_status TEXT NOT NULL,
    measured_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vector_index_id) REFERENCES vector_index(vector_index_id)
);

CREATE TABLE IF NOT EXISTS representation_governance_review (
    governance_review_id TEXT PRIMARY KEY,
    embedding_model_id TEXT NOT NULL,
    review_type TEXT NOT NULL,
    reviewer TEXT NOT NULL,
    review_date DATE NOT NULL,
    decision TEXT NOT NULL,
    decision_rationale TEXT NOT NULL,
    required_actions TEXT,
    next_review_date DATE,
    FOREIGN KEY (embedding_model_id) REFERENCES embedding_model(embedding_model_id)
);

CREATE INDEX IF NOT EXISTS idx_retrieval_query_index_time
ON retrieval_query(vector_index_id, query_timestamp);

CREATE INDEX IF NOT EXISTS idx_retrieval_result_query_rank
ON retrieval_result(query_id, rank);

CREATE INDEX IF NOT EXISTS idx_embedding_eval_set
ON embedding_evaluation_result(evaluation_set_id, metric_name);

CREATE INDEX IF NOT EXISTS idx_embedding_drift_status
ON embedding_drift_record(vector_index_id, drift_status);

CREATE VIEW IF NOT EXISTS v_low_quality_retrieval AS
SELECT
    q.query_id,
    q.vector_index_id,
    r.object_id,
    r.rank,
    r.similarity_score,
    r.retrieval_score,
    r.accepted
FROM retrieval_query q
JOIN retrieval_result r
    ON q.query_id = r.query_id
WHERE r.rank <= 5
  AND r.similarity_score < 0.25;

CREATE VIEW IF NOT EXISTS v_embedding_models_requiring_review AS
SELECT
    m.embedding_model_id,
    m.model_name,
    m.model_version,
    m.modality,
    b.review_status,
    d.drift_status
FROM embedding_model m
LEFT JOIN embedding_bias_review b
    ON m.embedding_model_id = b.embedding_model_id
LEFT JOIN vector_index vi
    ON m.embedding_model_id = vi.embedding_model_id
LEFT JOIN embedding_drift_record d
    ON vi.vector_index_id = d.vector_index_id
WHERE b.review_status IN ('open', 'requires_action')
   OR d.drift_status IN ('warning', 'action');
