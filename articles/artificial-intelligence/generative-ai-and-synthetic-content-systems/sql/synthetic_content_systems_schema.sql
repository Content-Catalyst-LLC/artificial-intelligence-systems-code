-- Generative AI and Synthetic Content Systems
-- SQL schema for generated artifacts, prompts, model runs, provenance,
-- human review, publication decisions, and governance audit events.

CREATE TABLE IF NOT EXISTS generative_system (
    system_id TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    provider_or_owner TEXT,
    modality_scope TEXT NOT NULL,
    intended_use TEXT NOT NULL,
    prohibited_use TEXT,
    risk_classification TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS generative_model_run (
    model_run_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    model_name TEXT NOT NULL,
    model_version TEXT,
    decoding_method TEXT,
    temperature REAL,
    top_p REAL,
    max_tokens INTEGER,
    safety_filter_version TEXT,
    run_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (system_id) REFERENCES generative_system(system_id)
);

CREATE TABLE IF NOT EXISTS prompt_record (
    prompt_id TEXT PRIMARY KEY,
    model_run_id TEXT NOT NULL,
    user_or_process TEXT,
    prompt_hash TEXT NOT NULL,
    prompt_uri TEXT,
    retrieval_context_uri TEXT,
    prompt_category TEXT,
    sensitive_domain INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (model_run_id) REFERENCES generative_model_run(model_run_id)
);

CREATE TABLE IF NOT EXISTS generated_artifact (
    artifact_id TEXT PRIMARY KEY,
    prompt_id TEXT NOT NULL,
    model_run_id TEXT NOT NULL,
    artifact_type TEXT NOT NULL,
    artifact_uri TEXT NOT NULL,
    content_hash TEXT NOT NULL,
    generation_status TEXT NOT NULL,
    quality_score REAL,
    grounding_score REAL,
    prompt_adherence_score REAL,
    policy_risk_score REAL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (prompt_id) REFERENCES prompt_record(prompt_id),
    FOREIGN KEY (model_run_id) REFERENCES generative_model_run(model_run_id)
);

CREATE TABLE IF NOT EXISTS provenance_record (
    provenance_id TEXT PRIMARY KEY,
    artifact_id TEXT NOT NULL,
    provenance_method TEXT NOT NULL,
    content_credentials_attached INTEGER NOT NULL DEFAULT 0,
    watermark_status TEXT,
    disclosure_label TEXT,
    source_material_summary TEXT,
    edit_history_uri TEXT,
    provenance_payload_uri TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (artifact_id) REFERENCES generated_artifact(artifact_id)
);

CREATE TABLE IF NOT EXISTS synthetic_content_review (
    review_id TEXT PRIMARY KEY,
    artifact_id TEXT NOT NULL,
    reviewer TEXT NOT NULL,
    review_type TEXT NOT NULL,
    review_decision TEXT NOT NULL,
    review_notes TEXT,
    factual_check_required INTEGER NOT NULL DEFAULT 0,
    legal_review_required INTEGER NOT NULL DEFAULT 0,
    publication_approved INTEGER NOT NULL DEFAULT 0,
    reviewed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (artifact_id) REFERENCES generated_artifact(artifact_id)
);

CREATE TABLE IF NOT EXISTS publication_decision (
    publication_id TEXT PRIMARY KEY,
    artifact_id TEXT NOT NULL,
    publication_channel TEXT NOT NULL,
    publication_status TEXT NOT NULL,
    disclosure_text TEXT,
    published_at TIMESTAMP,
    responsible_party TEXT,
    FOREIGN KEY (artifact_id) REFERENCES generated_artifact(artifact_id)
);

CREATE TABLE IF NOT EXISTS synthetic_content_incident (
    incident_id TEXT PRIMARY KEY,
    artifact_id TEXT,
    system_id TEXT NOT NULL,
    incident_type TEXT NOT NULL,
    severity TEXT NOT NULL,
    description TEXT NOT NULL,
    detected_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP,
    remediation_summary TEXT,
    FOREIGN KEY (artifact_id) REFERENCES generated_artifact(artifact_id),
    FOREIGN KEY (system_id) REFERENCES generative_system(system_id)
);

CREATE TABLE IF NOT EXISTS governance_audit_event (
    audit_event_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    artifact_id TEXT,
    event_type TEXT NOT NULL,
    event_summary TEXT NOT NULL,
    responsible_party TEXT,
    event_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (system_id) REFERENCES generative_system(system_id),
    FOREIGN KEY (artifact_id) REFERENCES generated_artifact(artifact_id)
);

CREATE INDEX IF NOT EXISTS idx_artifact_model_run
ON generated_artifact(model_run_id);

CREATE INDEX IF NOT EXISTS idx_artifact_policy_risk
ON generated_artifact(policy_risk_score);

CREATE INDEX IF NOT EXISTS idx_review_artifact
ON synthetic_content_review(artifact_id);

CREATE VIEW IF NOT EXISTS v_artifacts_requiring_review AS
SELECT
    a.artifact_id,
    a.artifact_type,
    a.quality_score,
    a.grounding_score,
    a.prompt_adherence_score,
    a.policy_risk_score,
    p.content_credentials_attached,
    p.watermark_status,
    r.review_decision
FROM generated_artifact a
LEFT JOIN provenance_record p
    ON a.artifact_id = p.artifact_id
LEFT JOIN synthetic_content_review r
    ON a.artifact_id = r.artifact_id
WHERE a.policy_risk_score >= 0.45
   OR a.grounding_score < 0.50
   OR p.content_credentials_attached = 0
   OR r.review_decision IS NULL;

CREATE VIEW IF NOT EXISTS v_open_synthetic_content_incidents AS
SELECT
    i.incident_id,
    s.system_name,
    i.artifact_id,
    i.incident_type,
    i.severity,
    i.description,
    i.detected_at
FROM synthetic_content_incident i
JOIN generative_system s
    ON i.system_id = s.system_id
WHERE i.resolved_at IS NULL;
