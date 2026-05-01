-- Large Language Models and Foundation Model Systems
-- SQL schema for base models, prompt versions, retrieval logs, tool-call logs,
-- evaluation results, safety reviews, incident records, and governance review.

CREATE TABLE IF NOT EXISTS llm_base_model (
    llm_model_id TEXT PRIMARY KEY,
    model_name TEXT NOT NULL,
    model_version TEXT NOT NULL,
    provider_or_owner TEXT,
    context_window_tokens INTEGER,
    modality_scope TEXT,
    intended_base_use TEXT,
    prohibited_use TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS llm_application (
    llm_application_id TEXT PRIMARY KEY,
    llm_model_id TEXT NOT NULL,
    application_name TEXT NOT NULL,
    application_version TEXT NOT NULL,
    intended_use TEXT NOT NULL,
    risk_level TEXT NOT NULL,
    owner TEXT NOT NULL,
    deployment_status TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (llm_model_id) REFERENCES llm_base_model(llm_model_id)
);

CREATE TABLE IF NOT EXISTS prompt_version (
    prompt_version_id TEXT PRIMARY KEY,
    llm_application_id TEXT NOT NULL,
    prompt_name TEXT NOT NULL,
    prompt_type TEXT NOT NULL,
    prompt_hash TEXT NOT NULL,
    policy_summary TEXT,
    approved_by TEXT,
    approval_status TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (llm_application_id) REFERENCES llm_application(llm_application_id)
);

CREATE TABLE IF NOT EXISTS retrieval_source (
    retrieval_source_id TEXT PRIMARY KEY,
    llm_application_id TEXT NOT NULL,
    source_name TEXT NOT NULL,
    source_type TEXT NOT NULL,
    authority_level TEXT,
    freshness_policy TEXT,
    access_policy TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (llm_application_id) REFERENCES llm_application(llm_application_id)
);

CREATE TABLE IF NOT EXISTS llm_interaction_log (
    interaction_id TEXT PRIMARY KEY,
    llm_application_id TEXT NOT NULL,
    prompt_version_id TEXT,
    user_or_process TEXT,
    input_token_count INTEGER,
    output_token_count INTEGER,
    latency_ms INTEGER,
    model_response_status TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (llm_application_id) REFERENCES llm_application(llm_application_id),
    FOREIGN KEY (prompt_version_id) REFERENCES prompt_version(prompt_version_id)
);

CREATE TABLE IF NOT EXISTS retrieval_log (
    retrieval_log_id TEXT PRIMARY KEY,
    interaction_id TEXT NOT NULL,
    retrieval_source_id TEXT,
    query_hash TEXT,
    retrieved_document_id TEXT,
    retrieved_chunk_id TEXT,
    retrieval_rank INTEGER,
    retrieval_score REAL,
    citation_used INTEGER DEFAULT 0,
    reviewer_relevance_score REAL,
    FOREIGN KEY (interaction_id) REFERENCES llm_interaction_log(interaction_id),
    FOREIGN KEY (retrieval_source_id) REFERENCES retrieval_source(retrieval_source_id)
);

CREATE TABLE IF NOT EXISTS tool_call_log (
    tool_call_id TEXT PRIMARY KEY,
    interaction_id TEXT NOT NULL,
    tool_name TEXT NOT NULL,
    tool_permission_level TEXT NOT NULL,
    tool_call_status TEXT NOT NULL,
    required_user_confirmation INTEGER DEFAULT 0,
    user_confirmed INTEGER DEFAULT 0,
    execution_latency_ms INTEGER,
    error_summary TEXT,
    FOREIGN KEY (interaction_id) REFERENCES llm_interaction_log(interaction_id)
);

CREATE TABLE IF NOT EXISTS llm_evaluation_result (
    evaluation_result_id TEXT PRIMARY KEY,
    llm_application_id TEXT NOT NULL,
    evaluation_name TEXT NOT NULL,
    use_case TEXT NOT NULL,
    metric_name TEXT NOT NULL,
    metric_value REAL NOT NULL,
    evaluation_dataset_uri TEXT,
    evaluated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (llm_application_id) REFERENCES llm_application(llm_application_id)
);

CREATE TABLE IF NOT EXISTS llm_safety_review (
    safety_review_id TEXT PRIMARY KEY,
    llm_application_id TEXT NOT NULL,
    review_type TEXT NOT NULL,
    reviewer TEXT,
    safety_score REAL,
    prompt_injection_score REAL,
    privacy_control_score REAL,
    finding_summary TEXT,
    mitigation_actions TEXT,
    review_status TEXT NOT NULL,
    reviewed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (llm_application_id) REFERENCES llm_application(llm_application_id)
);

CREATE TABLE IF NOT EXISTS llm_incident_record (
    incident_id TEXT PRIMARY KEY,
    llm_application_id TEXT NOT NULL,
    incident_type TEXT NOT NULL,
    severity TEXT NOT NULL,
    incident_status TEXT NOT NULL,
    description TEXT NOT NULL,
    detected_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP,
    remediation_summary TEXT,
    FOREIGN KEY (llm_application_id) REFERENCES llm_application(llm_application_id)
);

CREATE TABLE IF NOT EXISTS llm_governance_review (
    governance_review_id TEXT PRIMARY KEY,
    llm_application_id TEXT NOT NULL,
    review_type TEXT NOT NULL,
    reviewer TEXT NOT NULL,
    review_date DATE NOT NULL,
    decision TEXT NOT NULL,
    decision_rationale TEXT NOT NULL,
    required_actions TEXT,
    next_review_date DATE,
    FOREIGN KEY (llm_application_id) REFERENCES llm_application(llm_application_id)
);

CREATE TABLE IF NOT EXISTS llm_monitoring_signal (
    monitoring_signal_id TEXT PRIMARY KEY,
    llm_application_id TEXT NOT NULL,
    signal_name TEXT NOT NULL,
    signal_value REAL NOT NULL,
    threshold_warning REAL,
    threshold_action REAL,
    signal_status TEXT NOT NULL,
    measured_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (llm_application_id) REFERENCES llm_application(llm_application_id)
);

CREATE INDEX IF NOT EXISTS idx_llm_application_model
ON llm_application(llm_model_id, deployment_status);

CREATE INDEX IF NOT EXISTS idx_llm_interaction_app_time
ON llm_interaction_log(llm_application_id, created_at);

CREATE INDEX IF NOT EXISTS idx_retrieval_interaction_rank
ON retrieval_log(interaction_id, retrieval_rank);

CREATE INDEX IF NOT EXISTS idx_tool_call_interaction
ON tool_call_log(interaction_id, tool_call_status);

CREATE INDEX IF NOT EXISTS idx_llm_eval_metric
ON llm_evaluation_result(llm_application_id, metric_name, use_case);

CREATE VIEW IF NOT EXISTS v_llm_applications_requiring_review AS
SELECT
    app.llm_application_id,
    app.application_name,
    app.application_version,
    app.risk_level,
    sr.safety_score,
    sr.prompt_injection_score,
    sr.privacy_control_score,
    sr.review_status
FROM llm_application app
LEFT JOIN llm_safety_review sr
    ON app.llm_application_id = sr.llm_application_id
WHERE app.risk_level = 'high'
   OR sr.review_status IN ('open', 'requires_action')
   OR sr.safety_score < 0.75
   OR sr.prompt_injection_score < 0.70
   OR sr.privacy_control_score < 0.80;

CREATE VIEW IF NOT EXISTS v_llm_cost_latency_monitoring AS
SELECT
    llm_application_id,
    COUNT(*) AS interactions,
    AVG(input_token_count + output_token_count) AS mean_total_tokens,
    AVG(latency_ms) AS mean_latency_ms,
    SUM(CASE WHEN model_response_status != 'success' THEN 1 ELSE 0 END) AS failed_interactions
FROM llm_interaction_log
GROUP BY llm_application_id;
