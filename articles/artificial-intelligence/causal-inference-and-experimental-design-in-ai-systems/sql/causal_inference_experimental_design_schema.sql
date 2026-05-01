-- Causal Inference and Experimental Design in AI Systems Metadata Schema

CREATE TABLE IF NOT EXISTS causal_studies (
    study_id TEXT PRIMARY KEY,
    study_name TEXT NOT NULL,
    causal_question TEXT NOT NULL,
    study_owner TEXT NOT NULL,
    study_context TEXT,
    design_type TEXT CHECK(design_type IN ('randomized_experiment', 'ab_test', 'observational', 'quasi_experimental', 'simulation', 'mixed_design')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS causal_estimands (
    estimand_id TEXT PRIMARY KEY,
    study_id TEXT NOT NULL,
    estimand_name TEXT NOT NULL,
    unit_of_analysis TEXT NOT NULL,
    treatment_definition TEXT NOT NULL,
    comparison_condition TEXT NOT NULL,
    outcome_definition TEXT NOT NULL,
    target_population TEXT,
    time_horizon TEXT,
    estimand_type TEXT CHECK(estimand_type IN ('ATE', 'ATT', 'ATC', 'CATE', 'policy_effect', 'mediation_effect', 'spillover_effect', 'other')),
    FOREIGN KEY(study_id) REFERENCES causal_studies(study_id)
);

CREATE TABLE IF NOT EXISTS identification_assumptions (
    assumption_id TEXT PRIMARY KEY,
    estimand_id TEXT NOT NULL,
    assumption_type TEXT CHECK(assumption_type IN ('consistency', 'exchangeability', 'positivity', 'no_interference', 'transportability', 'exclusion_restriction', 'monotonicity', 'other')),
    assumption_statement TEXT NOT NULL,
    evidence_or_rationale TEXT,
    risk_level TEXT CHECK(risk_level IN ('low', 'medium', 'high', 'unknown')),
    FOREIGN KEY(estimand_id) REFERENCES causal_estimands(estimand_id)
);

CREATE TABLE IF NOT EXISTS experiment_assignments (
    assignment_id TEXT PRIMARY KEY,
    study_id TEXT NOT NULL,
    unit_id TEXT NOT NULL,
    treatment_group TEXT NOT NULL,
    assignment_probability REAL,
    assignment_timestamp TIMESTAMP,
    randomization_unit TEXT,
    stratification_variables TEXT,
    FOREIGN KEY(study_id) REFERENCES causal_studies(study_id)
);

CREATE TABLE IF NOT EXISTS causal_observations (
    observation_id TEXT PRIMARY KEY,
    study_id TEXT NOT NULL,
    unit_id TEXT NOT NULL,
    treatment_received TEXT,
    outcome_value REAL,
    outcome_timestamp TIMESTAMP,
    covariate_snapshot TEXT,
    exposure_notes TEXT,
    FOREIGN KEY(study_id) REFERENCES causal_studies(study_id)
);

CREATE TABLE IF NOT EXISTS causal_effect_estimates (
    estimate_id TEXT PRIMARY KEY,
    estimand_id TEXT NOT NULL,
    method_name TEXT NOT NULL,
    estimate_value REAL,
    standard_error REAL,
    confidence_interval_lower REAL,
    confidence_interval_upper REAL,
    p_value REAL,
    sensitivity_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(estimand_id) REFERENCES causal_estimands(estimand_id)
);

CREATE TABLE IF NOT EXISTS validity_threats (
    threat_id TEXT PRIMARY KEY,
    study_id TEXT NOT NULL,
    threat_type TEXT CHECK(threat_type IN ('confounding', 'selection_bias', 'measurement_error', 'attrition', 'interference', 'spillover', 'noncompliance', 'external_validity', 'transportability', 'feedback_loop', 'other')),
    description TEXT NOT NULL,
    mitigation_plan TEXT,
    residual_risk TEXT CHECK(residual_risk IN ('low', 'medium', 'high', 'unknown')),
    FOREIGN KEY(study_id) REFERENCES causal_studies(study_id)
);

CREATE TABLE IF NOT EXISTS governance_reviews (
    review_id TEXT PRIMARY KEY,
    study_id TEXT NOT NULL,
    review_date DATE NOT NULL,
    reviewer TEXT NOT NULL,
    causal_question_reviewed BOOLEAN DEFAULT FALSE,
    estimand_reviewed BOOLEAN DEFAULT FALSE,
    assumptions_reviewed BOOLEAN DEFAULT FALSE,
    interference_reviewed BOOLEAN DEFAULT FALSE,
    external_validity_reviewed BOOLEAN DEFAULT FALSE,
    findings TEXT,
    required_actions TEXT,
    status TEXT CHECK(status IN ('draft', 'approved', 'requires_action', 'closed')),
    FOREIGN KEY(study_id) REFERENCES causal_studies(study_id)
);
