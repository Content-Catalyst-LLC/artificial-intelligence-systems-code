-- Artificial Intelligence in Decision Support Systems
-- SQL schema for DSS governance, predictions, utilities, scenarios,
-- recommendations, human overrides, audits, and accountability.

CREATE TABLE IF NOT EXISTS decision_support_system (
    system_id TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    decision_domain TEXT NOT NULL,
    intended_use TEXT NOT NULL,
    prohibited_use TEXT,
    system_owner TEXT NOT NULL,
    risk_classification TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS decision_context (
    context_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    context_name TEXT NOT NULL,
    decision_question TEXT NOT NULL,
    decision_authority TEXT,
    review_required INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (system_id) REFERENCES decision_support_system(system_id)
);

CREATE TABLE IF NOT EXISTS decision_option (
    option_id TEXT PRIMARY KEY,
    context_id TEXT NOT NULL,
    option_name TEXT NOT NULL,
    option_description TEXT,
    feasibility_status TEXT,
    estimated_cost REAL,
    capacity_required REAL,
    equity_priority INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (context_id) REFERENCES decision_context(context_id)
);

CREATE TABLE IF NOT EXISTS prediction_record (
    prediction_id TEXT PRIMARY KEY,
    option_id TEXT NOT NULL,
    model_name TEXT NOT NULL,
    model_version TEXT,
    predicted_outcome TEXT,
    predicted_probability REAL,
    uncertainty_score REAL,
    calibration_status TEXT,
    prediction_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (option_id) REFERENCES decision_option(option_id)
);

CREATE TABLE IF NOT EXISTS utility_record (
    utility_id TEXT PRIMARY KEY,
    option_id TEXT NOT NULL,
    utility_model_name TEXT NOT NULL,
    expected_benefit REAL,
    expected_cost REAL,
    expected_utility REAL,
    robust_utility REAL,
    objective_summary TEXT,
    constraint_summary TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (option_id) REFERENCES decision_option(option_id)
);

CREATE TABLE IF NOT EXISTS scenario_record (
    scenario_id TEXT PRIMARY KEY,
    context_id TEXT NOT NULL,
    scenario_name TEXT NOT NULL,
    scenario_description TEXT,
    probability_weight REAL,
    stress_case INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (context_id) REFERENCES decision_context(context_id)
);

CREATE TABLE IF NOT EXISTS scenario_outcome (
    scenario_outcome_id TEXT PRIMARY KEY,
    scenario_id TEXT NOT NULL,
    option_id TEXT NOT NULL,
    outcome_value REAL,
    utility_value REAL,
    risk_value REAL,
    notes TEXT,
    FOREIGN KEY (scenario_id) REFERENCES scenario_record(scenario_id),
    FOREIGN KEY (option_id) REFERENCES decision_option(option_id)
);

CREATE TABLE IF NOT EXISTS recommendation_record (
    recommendation_id TEXT PRIMARY KEY,
    context_id TEXT NOT NULL,
    option_id TEXT NOT NULL,
    recommendation_rank INTEGER,
    recommendation_status TEXT NOT NULL,
    recommendation_reason TEXT,
    human_review_required INTEGER NOT NULL DEFAULT 1,
    generated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (context_id) REFERENCES decision_context(context_id),
    FOREIGN KEY (option_id) REFERENCES decision_option(option_id)
);

CREATE TABLE IF NOT EXISTS human_decision_review (
    review_id TEXT PRIMARY KEY,
    recommendation_id TEXT NOT NULL,
    reviewer TEXT NOT NULL,
    review_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    decision TEXT NOT NULL,
    override_applied INTEGER NOT NULL DEFAULT 0,
    override_reason TEXT,
    accountability_note TEXT,
    FOREIGN KEY (recommendation_id) REFERENCES recommendation_record(recommendation_id)
);

CREATE TABLE IF NOT EXISTS decision_audit_event (
    audit_event_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    context_id TEXT,
    event_type TEXT NOT NULL,
    event_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    event_summary TEXT NOT NULL,
    responsible_party TEXT,
    FOREIGN KEY (system_id) REFERENCES decision_support_system(system_id),
    FOREIGN KEY (context_id) REFERENCES decision_context(context_id)
);

CREATE TABLE IF NOT EXISTS governance_review (
    governance_review_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    review_type TEXT NOT NULL,
    reviewer TEXT NOT NULL,
    review_date DATE NOT NULL,
    decision TEXT NOT NULL,
    decision_rationale TEXT NOT NULL,
    required_actions TEXT,
    next_review_date DATE,
    FOREIGN KEY (system_id) REFERENCES decision_support_system(system_id)
);

CREATE INDEX IF NOT EXISTS idx_prediction_option_time
ON prediction_record(option_id, prediction_timestamp);

CREATE INDEX IF NOT EXISTS idx_recommendation_context_rank
ON recommendation_record(context_id, recommendation_rank);

CREATE INDEX IF NOT EXISTS idx_human_review_recommendation
ON human_decision_review(recommendation_id);

CREATE VIEW IF NOT EXISTS v_decision_recommendation_summary AS
SELECT
    dss.system_name,
    dc.context_name,
    do.option_name,
    pr.predicted_probability,
    pr.uncertainty_score,
    ur.expected_utility,
    ur.robust_utility,
    rr.recommendation_rank,
    rr.recommendation_status,
    rr.human_review_required
FROM recommendation_record rr
JOIN decision_context dc
    ON rr.context_id = dc.context_id
JOIN decision_support_system dss
    ON dc.system_id = dss.system_id
JOIN decision_option do
    ON rr.option_id = do.option_id
LEFT JOIN prediction_record pr
    ON do.option_id = pr.option_id
LEFT JOIN utility_record ur
    ON do.option_id = ur.option_id;

CREATE VIEW IF NOT EXISTS v_human_overrides AS
SELECT
    h.review_id,
    dss.system_name,
    dc.context_name,
    do.option_name,
    h.reviewer,
    h.decision,
    h.override_reason,
    h.review_timestamp
FROM human_decision_review h
JOIN recommendation_record rr
    ON h.recommendation_id = rr.recommendation_id
JOIN decision_context dc
    ON rr.context_id = dc.context_id
JOIN decision_support_system dss
    ON dc.system_id = dss.system_id
JOIN decision_option do
    ON rr.option_id = do.option_id
WHERE h.override_applied = 1;
