-- Retrieval-Augmented Generation and AI Knowledge Systems
-- SQL schema for source registries, document chunks, embeddings, retrieval logs,
-- reranking records, prompt versions, citations, access controls, evaluation results,
-- and governance review.

CREATE TABLE IF NOT EXISTS rag_source_registry (
    source_id TEXT PRIMARY KEY,
    source_name TEXT NOT NULL,
    source_type TEXT NOT NULL,
    authority_level TEXT NOT NULL,
    owner TEXT,
    access_group TEXT,
    freshness_policy TEXT,
    source_status TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS rag_document (
    document_id TEXT PRIMARY KEY,
    source_id TEXT NOT NULL,
    title TEXT NOT NULL,
    document_uri TEXT,
    document_version TEXT,
    publication_date DATE,
    last_updated_at TIMESTAMP,
    sensitivity_label TEXT,
    document_status TEXT NOT NULL,
    checksum TEXT,
    FOREIGN KEY (source_id) REFERENCES rag_source_registry(source_id)
);

CREATE TABLE IF NOT EXISTS rag_document_chunk (
    chunk_id TEXT PRIMARY KEY,
    document_id TEXT NOT NULL,
    chunk_index INTEGER NOT NULL,
    section_title TEXT,
    chunk_text_hash TEXT NOT NULL,
    token_count INTEGER,
    chunking_strategy TEXT NOT NULL,
    metadata_json TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (document_id) REFERENCES rag_document(document_id)
);

CREATE TABLE IF NOT EXISTS rag_embedding_record (
    embedding_id TEXT PRIMARY KEY,
    chunk_id TEXT NOT NULL,
    embedding_model TEXT NOT NULL,
    embedding_model_version TEXT NOT NULL,
    vector_index_name TEXT NOT NULL,
    vector_index_version TEXT NOT NULL,
    embedded_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (chunk_id) REFERENCES rag_document_chunk(chunk_id)
);

CREATE TABLE IF NOT EXISTS rag_prompt_version (
    prompt_version_id TEXT PRIMARY KEY,
    prompt_name TEXT NOT NULL,
    prompt_hash TEXT NOT NULL,
    retrieval_policy_summary TEXT,
    citation_policy_summary TEXT,
    abstention_policy_summary TEXT,
    approval_status TEXT NOT NULL,
    approved_by TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS rag_interaction (
    interaction_id TEXT PRIMARY KEY,
    user_or_process TEXT,
    query_hash TEXT NOT NULL,
    prompt_version_id TEXT,
    retrieval_mode TEXT NOT NULL,
    model_name TEXT,
    model_version TEXT,
    response_status TEXT NOT NULL,
    latency_ms INTEGER,
    total_tokens INTEGER,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (prompt_version_id) REFERENCES rag_prompt_version(prompt_version_id)
);

CREATE TABLE IF NOT EXISTS rag_retrieval_log (
    retrieval_log_id TEXT PRIMARY KEY,
    interaction_id TEXT NOT NULL,
    chunk_id TEXT NOT NULL,
    retrieval_rank INTEGER NOT NULL,
    retrieval_score REAL,
    retrieval_method TEXT NOT NULL,
    access_filter_passed INTEGER NOT NULL DEFAULT 1,
    freshness_filter_passed INTEGER NOT NULL DEFAULT 1,
    authority_filter_passed INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (interaction_id) REFERENCES rag_interaction(interaction_id),
    FOREIGN KEY (chunk_id) REFERENCES rag_document_chunk(chunk_id)
);

CREATE TABLE IF NOT EXISTS rag_reranking_record (
    reranking_record_id TEXT PRIMARY KEY,
    interaction_id TEXT NOT NULL,
    chunk_id TEXT NOT NULL,
    original_rank INTEGER,
    reranked_rank INTEGER,
    reranker_model TEXT,
    reranker_score REAL,
    reviewer_relevance_score REAL,
    FOREIGN KEY (interaction_id) REFERENCES rag_interaction(interaction_id),
    FOREIGN KEY (chunk_id) REFERENCES rag_document_chunk(chunk_id)
);

CREATE TABLE IF NOT EXISTS rag_generated_citation (
    citation_id TEXT PRIMARY KEY,
    interaction_id TEXT NOT NULL,
    chunk_id TEXT,
    cited_claim_hash TEXT NOT NULL,
    citation_position INTEGER,
    support_status TEXT NOT NULL,
    reviewer_notes TEXT,
    FOREIGN KEY (interaction_id) REFERENCES rag_interaction(interaction_id),
    FOREIGN KEY (chunk_id) REFERENCES rag_document_chunk(chunk_id)
);

CREATE TABLE IF NOT EXISTS rag_access_control_event (
    access_event_id TEXT PRIMARY KEY,
    interaction_id TEXT NOT NULL,
    document_id TEXT NOT NULL,
    user_or_process TEXT,
    required_access_group TEXT,
    access_decision TEXT NOT NULL,
    decision_reason TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (interaction_id) REFERENCES rag_interaction(interaction_id),
    FOREIGN KEY (document_id) REFERENCES rag_document(document_id)
);

CREATE TABLE IF NOT EXISTS rag_evaluation_result (
    evaluation_result_id TEXT PRIMARY KEY,
    interaction_id TEXT,
    evaluation_name TEXT NOT NULL,
    query_type TEXT,
    metric_name TEXT NOT NULL,
    metric_value REAL NOT NULL,
    reviewer TEXT,
    evaluated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (interaction_id) REFERENCES rag_interaction(interaction_id)
);

CREATE TABLE IF NOT EXISTS rag_security_review (
    security_review_id TEXT PRIMARY KEY,
    interaction_id TEXT,
    review_type TEXT NOT NULL,
    prompt_injection_detected INTEGER DEFAULT 0,
    access_control_issue_detected INTEGER DEFAULT 0,
    suspicious_source_content INTEGER DEFAULT 0,
    review_status TEXT NOT NULL,
    finding_summary TEXT,
    reviewed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (interaction_id) REFERENCES rag_interaction(interaction_id)
);

CREATE TABLE IF NOT EXISTS rag_governance_review (
    governance_review_id TEXT PRIMARY KEY,
    source_id TEXT,
    prompt_version_id TEXT,
    vector_index_name TEXT,
    review_type TEXT NOT NULL,
    reviewer TEXT NOT NULL,
    review_date DATE NOT NULL,
    decision TEXT NOT NULL,
    decision_rationale TEXT NOT NULL,
    required_actions TEXT,
    next_review_date DATE,
    FOREIGN KEY (source_id) REFERENCES rag_source_registry(source_id),
    FOREIGN KEY (prompt_version_id) REFERENCES rag_prompt_version(prompt_version_id)
);

CREATE TABLE IF NOT EXISTS rag_monitoring_signal (
    monitoring_signal_id TEXT PRIMARY KEY,
    signal_name TEXT NOT NULL,
    signal_value REAL NOT NULL,
    threshold_warning REAL,
    threshold_action REAL,
    signal_status TEXT NOT NULL,
    measured_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_rag_document_source
ON rag_document(source_id, document_status);

CREATE INDEX IF NOT EXISTS idx_rag_chunk_document
ON rag_document_chunk(document_id, chunk_index);

CREATE INDEX IF NOT EXISTS idx_rag_embedding_index
ON rag_embedding_record(vector_index_name, vector_index_version);

CREATE INDEX IF NOT EXISTS idx_rag_interaction_time
ON rag_interaction(created_at, response_status);

CREATE INDEX IF NOT EXISTS idx_rag_retrieval_interaction_rank
ON rag_retrieval_log(interaction_id, retrieval_rank);

CREATE INDEX IF NOT EXISTS idx_rag_citation_support
ON rag_generated_citation(interaction_id, support_status);

CREATE VIEW IF NOT EXISTS v_rag_unsupported_citations AS
SELECT
    c.citation_id,
    c.interaction_id,
    c.chunk_id,
    c.support_status,
    i.query_hash,
    i.model_name,
    i.model_version
FROM rag_generated_citation c
JOIN rag_interaction i
    ON c.interaction_id = i.interaction_id
WHERE c.support_status IN ('unsupported', 'uncertain', 'review_required');

CREATE VIEW IF NOT EXISTS v_rag_stale_or_low_authority_retrieval AS
SELECT
    rl.retrieval_log_id,
    rl.interaction_id,
    rl.chunk_id,
    rl.retrieval_rank,
    s.source_name,
    s.authority_level,
    d.last_updated_at,
    rl.freshness_filter_passed,
    rl.authority_filter_passed
FROM rag_retrieval_log rl
JOIN rag_document_chunk ch
    ON rl.chunk_id = ch.chunk_id
JOIN rag_document d
    ON ch.document_id = d.document_id
JOIN rag_source_registry s
    ON d.source_id = s.source_id
WHERE rl.freshness_filter_passed = 0
   OR rl.authority_filter_passed = 0
   OR s.authority_level IN ('low', 'unreviewed');
