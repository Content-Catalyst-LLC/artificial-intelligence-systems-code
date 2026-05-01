-- Multimodal AI: Language, Vision, Audio, and Action
-- SQL schema for modality sources, encoders, fusion records, cross-modal retrieval,
-- evaluation results, action logs, privacy reviews, accessibility reviews,
-- and governance review.

CREATE TABLE IF NOT EXISTS multimodal_system (
    multimodal_system_id TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    system_version TEXT NOT NULL,
    intended_use TEXT NOT NULL,
    risk_level TEXT NOT NULL,
    owner TEXT NOT NULL,
    deployment_status TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS modality_source (
    modality_source_id TEXT PRIMARY KEY,
    multimodal_system_id TEXT NOT NULL,
    modality_type TEXT NOT NULL,
    source_name TEXT NOT NULL,
    source_uri TEXT,
    sensitivity_label TEXT,
    consent_status TEXT,
    retention_policy TEXT,
    source_status TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (multimodal_system_id) REFERENCES multimodal_system(multimodal_system_id)
);

CREATE TABLE IF NOT EXISTS modality_encoder (
    encoder_id TEXT PRIMARY KEY,
    multimodal_system_id TEXT NOT NULL,
    modality_type TEXT NOT NULL,
    encoder_name TEXT NOT NULL,
    encoder_version TEXT NOT NULL,
    embedding_dimension INTEGER,
    calibration_status TEXT,
    approved_status TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (multimodal_system_id) REFERENCES multimodal_system(multimodal_system_id)
);

CREATE TABLE IF NOT EXISTS multimodal_fusion_record (
    fusion_record_id TEXT PRIMARY KEY,
    multimodal_system_id TEXT NOT NULL,
    fusion_architecture TEXT NOT NULL,
    supported_modalities TEXT NOT NULL,
    weighting_policy TEXT,
    conflict_handling_policy TEXT,
    approved_status TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (multimodal_system_id) REFERENCES multimodal_system(multimodal_system_id)
);

CREATE TABLE IF NOT EXISTS multimodal_interaction (
    interaction_id TEXT PRIMARY KEY,
    multimodal_system_id TEXT NOT NULL,
    user_or_process TEXT,
    use_case TEXT NOT NULL,
    has_text INTEGER DEFAULT 0,
    has_vision INTEGER DEFAULT 0,
    has_audio INTEGER DEFAULT 0,
    has_video INTEGER DEFAULT 0,
    has_sensor INTEGER DEFAULT 0,
    has_action INTEGER DEFAULT 0,
    response_status TEXT NOT NULL,
    latency_ms INTEGER,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (multimodal_system_id) REFERENCES multimodal_system(multimodal_system_id)
);

CREATE TABLE IF NOT EXISTS cross_modal_retrieval_log (
    retrieval_log_id TEXT PRIMARY KEY,
    interaction_id TEXT NOT NULL,
    query_modality TEXT NOT NULL,
    retrieved_modality TEXT NOT NULL,
    retrieved_artifact_id TEXT,
    retrieval_rank INTEGER,
    similarity_score REAL,
    grounding_support_status TEXT,
    reviewer_relevance_score REAL,
    FOREIGN KEY (interaction_id) REFERENCES multimodal_interaction(interaction_id)
);

CREATE TABLE IF NOT EXISTS multimodal_evaluation_result (
    evaluation_result_id TEXT PRIMARY KEY,
    multimodal_system_id TEXT NOT NULL,
    evaluation_name TEXT NOT NULL,
    use_case TEXT NOT NULL,
    metric_name TEXT NOT NULL,
    metric_value REAL NOT NULL,
    modality_type TEXT,
    evaluated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    reviewer TEXT,
    FOREIGN KEY (multimodal_system_id) REFERENCES multimodal_system(multimodal_system_id)
);

CREATE TABLE IF NOT EXISTS multimodal_action_log (
    action_log_id TEXT PRIMARY KEY,
    interaction_id TEXT NOT NULL,
    action_type TEXT NOT NULL,
    action_target TEXT,
    action_status TEXT NOT NULL,
    required_confirmation INTEGER DEFAULT 0,
    user_confirmed INTEGER DEFAULT 0,
    rollback_available INTEGER DEFAULT 0,
    safety_review_status TEXT,
    executed_at TIMESTAMP,
    FOREIGN KEY (interaction_id) REFERENCES multimodal_interaction(interaction_id)
);

CREATE TABLE IF NOT EXISTS multimodal_privacy_review (
    privacy_review_id TEXT PRIMARY KEY,
    multimodal_system_id TEXT NOT NULL,
    modality_type TEXT NOT NULL,
    privacy_risk_category TEXT NOT NULL,
    finding_summary TEXT NOT NULL,
    mitigation_actions TEXT,
    review_status TEXT NOT NULL,
    reviewed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (multimodal_system_id) REFERENCES multimodal_system(multimodal_system_id)
);

CREATE TABLE IF NOT EXISTS multimodal_accessibility_review (
    accessibility_review_id TEXT PRIMARY KEY,
    multimodal_system_id TEXT NOT NULL,
    use_case TEXT NOT NULL,
    accessibility_dimension TEXT NOT NULL,
    evaluation_summary TEXT NOT NULL,
    affected_user_group TEXT,
    review_status TEXT NOT NULL,
    reviewed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (multimodal_system_id) REFERENCES multimodal_system(multimodal_system_id)
);

CREATE TABLE IF NOT EXISTS multimodal_governance_review (
    governance_review_id TEXT PRIMARY KEY,
    multimodal_system_id TEXT NOT NULL,
    review_type TEXT NOT NULL,
    reviewer TEXT NOT NULL,
    review_date DATE NOT NULL,
    decision TEXT NOT NULL,
    decision_rationale TEXT NOT NULL,
    required_actions TEXT,
    next_review_date DATE,
    FOREIGN KEY (multimodal_system_id) REFERENCES multimodal_system(multimodal_system_id)
);

CREATE TABLE IF NOT EXISTS multimodal_monitoring_signal (
    monitoring_signal_id TEXT PRIMARY KEY,
    multimodal_system_id TEXT NOT NULL,
    signal_name TEXT NOT NULL,
    signal_value REAL NOT NULL,
    threshold_warning REAL,
    threshold_action REAL,
    signal_status TEXT NOT NULL,
    measured_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (multimodal_system_id) REFERENCES multimodal_system(multimodal_system_id)
);

CREATE INDEX IF NOT EXISTS idx_multimodal_source_system_modality
ON modality_source(multimodal_system_id, modality_type, source_status);

CREATE INDEX IF NOT EXISTS idx_multimodal_encoder_system_modality
ON modality_encoder(multimodal_system_id, modality_type, approved_status);

CREATE INDEX IF NOT EXISTS idx_multimodal_interaction_system_time
ON multimodal_interaction(multimodal_system_id, created_at);

CREATE INDEX IF NOT EXISTS idx_cross_modal_retrieval_interaction
ON cross_modal_retrieval_log(interaction_id, query_modality, retrieved_modality);

CREATE INDEX IF NOT EXISTS idx_multimodal_eval_system_metric
ON multimodal_evaluation_result(multimodal_system_id, metric_name, use_case);

CREATE VIEW IF NOT EXISTS v_multimodal_systems_requiring_review AS
SELECT
    ms.multimodal_system_id,
    ms.system_name,
    ms.system_version,
    ms.risk_level,
    pr.modality_type,
    pr.privacy_risk_category,
    pr.review_status
FROM multimodal_system ms
LEFT JOIN multimodal_privacy_review pr
    ON ms.multimodal_system_id = pr.multimodal_system_id
WHERE ms.risk_level = 'high'
   OR pr.review_status IN ('open', 'requires_action');

CREATE VIEW IF NOT EXISTS v_multimodal_action_safety_review AS
SELECT
    mi.interaction_id,
    mi.multimodal_system_id,
    mi.use_case,
    al.action_type,
    al.action_status,
    al.required_confirmation,
    al.user_confirmed,
    al.rollback_available,
    al.safety_review_status
FROM multimodal_interaction mi
JOIN multimodal_action_log al
    ON mi.interaction_id = al.interaction_id
WHERE al.safety_review_status IN ('open', 'requires_action')
   OR (al.required_confirmation = 1 AND al.user_confirmed = 0)
   OR al.rollback_available = 0;
