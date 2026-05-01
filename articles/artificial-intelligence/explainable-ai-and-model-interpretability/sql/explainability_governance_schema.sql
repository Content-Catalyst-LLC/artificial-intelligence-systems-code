-- Explainable AI and Model Interpretability
-- SQL schema for explanation governance, auditability, and contestability.

CREATE TABLE IF NOT EXISTS ai_explainability_system (
    system_id TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    domain TEXT NOT NULL,
    intended_use TEXT NOT NULL,
    explanation_purpose TEXT NOT NULL,
    risk_classification TEXT NOT NULL,
    system_owner TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ai_model_card (
    model_card_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    model_name TEXT NOT NULL,
    model_version TEXT NOT NULL,
    model_type TEXT NOT NULL,
    intended_users TEXT,
    intended_uses TEXT,
    prohibited_uses TEXT,
    performance_summary TEXT,
    interpretability_summary TEXT,
    known_limitations TEXT,
    ethical_considerations TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (system_id) REFERENCES ai_explainability_system(system_id)
);

CREATE TABLE IF NOT EXISTS ai_explanation_method (
    explanation_method_id TEXT PRIMARY KEY,
    method_name TEXT NOT NULL,
    method_family TEXT NOT NULL,
    explanation_scope TEXT NOT NULL,
    model_relation TEXT NOT NULL,
    strengths TEXT,
    limitations TEXT,
    required_inputs TEXT,
    governance_notes TEXT
);

CREATE TABLE IF NOT EXISTS ai_prediction_explanation (
    explanation_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    model_card_id TEXT NOT NULL,
    explanation_method_id TEXT NOT NULL,
    prediction_id TEXT NOT NULL,
    subject_reference TEXT,
    prediction_score REAL,
    predicted_label TEXT,
    explanation_payload_uri TEXT NOT NULL,
    explanation_summary TEXT,
    explanation_stability_score REAL,
    explanation_fidelity_score REAL,
    generated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (system_id) REFERENCES ai_explainability_system(system_id),
    FOREIGN KEY (model_card_id) REFERENCES ai_model_card(model_card_id),
    FOREIGN KEY (explanation_method_id) REFERENCES ai_explanation_method(explanation_method_id)
);

CREATE TABLE IF NOT EXISTS ai_feature_attribution (
    attribution_id TEXT PRIMARY KEY,
    explanation_id TEXT NOT NULL,
    feature_name TEXT NOT NULL,
    feature_value TEXT,
    attribution_value REAL NOT NULL,
    attribution_rank INTEGER,
    direction TEXT,
    interpretation_note TEXT,
    FOREIGN KEY (explanation_id) REFERENCES ai_prediction_explanation(explanation_id)
);

CREATE TABLE IF NOT EXISTS ai_counterfactual_explanation (
    counterfactual_id TEXT PRIMARY KEY,
    explanation_id TEXT NOT NULL,
    original_prediction TEXT NOT NULL,
    counterfactual_prediction TEXT NOT NULL,
    distance_score REAL,
    plausibility_score REAL,
    actionability_score REAL,
    counterfactual_payload_uri TEXT NOT NULL,
    generated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (explanation_id) REFERENCES ai_prediction_explanation(explanation_id)
);

CREATE TABLE IF NOT EXISTS ai_counterfactual_feature_change (
    change_id TEXT PRIMARY KEY,
    counterfactual_id TEXT NOT NULL,
    feature_name TEXT NOT NULL,
    original_value TEXT,
    counterfactual_value TEXT,
    change_description TEXT,
    actionable INTEGER NOT NULL DEFAULT 1,
    sensitive_or_protected INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (counterfactual_id) REFERENCES ai_counterfactual_explanation(counterfactual_id)
);

CREATE TABLE IF NOT EXISTS ai_explanation_audit (
    audit_id TEXT PRIMARY KEY,
    explanation_id TEXT NOT NULL,
    reviewer TEXT NOT NULL,
    review_date DATE NOT NULL,
    fidelity_pass INTEGER NOT NULL,
    stability_pass INTEGER NOT NULL,
    usability_pass INTEGER NOT NULL,
    causal_review_required INTEGER NOT NULL,
    contestability_supported INTEGER NOT NULL,
    audit_decision TEXT NOT NULL,
    audit_notes TEXT,
    FOREIGN KEY (explanation_id) REFERENCES ai_prediction_explanation(explanation_id)
);

CREATE TABLE IF NOT EXISTS ai_explanation_contestation (
    contestation_id TEXT PRIMARY KEY,
    explanation_id TEXT NOT NULL,
    submitted_by TEXT,
    submitted_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    contestation_reason TEXT NOT NULL,
    status TEXT NOT NULL,
    resolution_summary TEXT,
    resolved_at TIMESTAMP,
    FOREIGN KEY (explanation_id) REFERENCES ai_prediction_explanation(explanation_id)
);

CREATE VIEW IF NOT EXISTS v_explanation_audit_status AS
SELECT
    e.explanation_id,
    s.system_name,
    m.model_name,
    m.model_version,
    method.method_name,
    e.prediction_score,
    e.predicted_label,
    e.explanation_stability_score,
    e.explanation_fidelity_score,
    a.audit_decision,
    a.causal_review_required,
    a.contestability_supported
FROM ai_prediction_explanation e
JOIN ai_explainability_system s
    ON e.system_id = s.system_id
JOIN ai_model_card m
    ON e.model_card_id = m.model_card_id
JOIN ai_explanation_method method
    ON e.explanation_method_id = method.explanation_method_id
LEFT JOIN ai_explanation_audit a
    ON e.explanation_id = a.explanation_id;

CREATE VIEW IF NOT EXISTS v_counterfactual_actionability AS
SELECT
    c.counterfactual_id,
    c.explanation_id,
    c.distance_score,
    c.plausibility_score,
    c.actionability_score,
    SUM(CASE WHEN f.actionable = 1 THEN 1 ELSE 0 END) AS actionable_changes,
    SUM(CASE WHEN f.sensitive_or_protected = 1 THEN 1 ELSE 0 END) AS sensitive_changes
FROM ai_counterfactual_explanation c
LEFT JOIN ai_counterfactual_feature_change f
    ON c.counterfactual_id = f.counterfactual_id
GROUP BY
    c.counterfactual_id,
    c.explanation_id,
    c.distance_score,
    c.plausibility_score,
    c.actionability_score;
