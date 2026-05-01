-- Synthetic Data, Simulation, and AI Evaluation Environments
-- SQL schema for synthetic datasets, simulation environments, benchmark registries,
-- privacy reviews, utility metrics, scenario coverage, sim-to-real validation,
-- and governance records.

CREATE TABLE IF NOT EXISTS synthetic_artifact_registry (
    artifact_id TEXT PRIMARY KEY,
    artifact_name TEXT NOT NULL,
    artifact_type TEXT NOT NULL,
    artifact_version TEXT NOT NULL,
    intended_use TEXT NOT NULL,
    owner TEXT NOT NULL,
    approval_status TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS source_data_record (
    source_data_id TEXT PRIMARY KEY,
    artifact_id TEXT NOT NULL,
    source_name TEXT NOT NULL,
    source_version TEXT,
    data_classification TEXT NOT NULL,
    access_restrictions TEXT,
    provenance_summary TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (artifact_id) REFERENCES synthetic_artifact_registry(artifact_id)
);

CREATE TABLE IF NOT EXISTS synthetic_generation_method (
    generation_method_id TEXT PRIMARY KEY,
    artifact_id TEXT NOT NULL,
    method_name TEXT NOT NULL,
    method_type TEXT NOT NULL,
    generator_version TEXT NOT NULL,
    privacy_method TEXT,
    configuration_hash TEXT,
    generated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (artifact_id) REFERENCES synthetic_artifact_registry(artifact_id)
);

CREATE TABLE IF NOT EXISTS synthetic_fidelity_metric (
    fidelity_metric_id TEXT PRIMARY KEY,
    artifact_id TEXT NOT NULL,
    metric_name TEXT NOT NULL,
    metric_value REAL NOT NULL,
    feature_or_slice TEXT,
    warning_threshold REAL,
    action_threshold REAL,
    metric_status TEXT NOT NULL,
    measured_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (artifact_id) REFERENCES synthetic_artifact_registry(artifact_id)
);

CREATE TABLE IF NOT EXISTS synthetic_utility_metric (
    utility_metric_id TEXT PRIMARY KEY,
    artifact_id TEXT NOT NULL,
    task_name TEXT NOT NULL,
    metric_name TEXT NOT NULL,
    synthetic_metric_value REAL NOT NULL,
    real_holdout_metric_value REAL,
    utility_gap REAL,
    metric_status TEXT NOT NULL,
    measured_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (artifact_id) REFERENCES synthetic_artifact_registry(artifact_id)
);

CREATE TABLE IF NOT EXISTS synthetic_privacy_review (
    privacy_review_id TEXT PRIMARY KEY,
    artifact_id TEXT NOT NULL,
    privacy_method TEXT,
    privacy_risk_metric TEXT NOT NULL,
    privacy_risk_value REAL NOT NULL,
    attacker_model TEXT,
    review_decision TEXT NOT NULL,
    reviewer TEXT NOT NULL,
    reviewed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (artifact_id) REFERENCES synthetic_artifact_registry(artifact_id)
);

CREATE TABLE IF NOT EXISTS simulation_environment (
    simulation_environment_id TEXT PRIMARY KEY,
    environment_name TEXT NOT NULL,
    environment_version TEXT NOT NULL,
    environment_type TEXT NOT NULL,
    simulated_system TEXT NOT NULL,
    assumptions_summary TEXT,
    owner TEXT NOT NULL,
    approval_status TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS simulation_scenario (
    scenario_id TEXT PRIMARY KEY,
    simulation_environment_id TEXT NOT NULL,
    scenario_name TEXT NOT NULL,
    scenario_family TEXT NOT NULL,
    scenario_description TEXT NOT NULL,
    rare_case_flag INTEGER DEFAULT 0,
    safety_case_flag INTEGER DEFAULT 0,
    scenario_status TEXT NOT NULL,
    FOREIGN KEY (simulation_environment_id) REFERENCES simulation_environment(simulation_environment_id)
);

CREATE TABLE IF NOT EXISTS sim_to_real_validation (
    sim_to_real_validation_id TEXT PRIMARY KEY,
    simulation_environment_id TEXT NOT NULL,
    validation_name TEXT NOT NULL,
    sim_metric_value REAL NOT NULL,
    real_metric_value REAL,
    sim_to_real_gap REAL,
    validation_status TEXT NOT NULL,
    reviewer TEXT,
    validated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (simulation_environment_id) REFERENCES simulation_environment(simulation_environment_id)
);

CREATE TABLE IF NOT EXISTS benchmark_environment (
    benchmark_id TEXT PRIMARY KEY,
    benchmark_name TEXT NOT NULL,
    benchmark_version TEXT NOT NULL,
    benchmark_purpose TEXT NOT NULL,
    task_scope TEXT NOT NULL,
    metric_suite TEXT NOT NULL,
    contamination_risk_level TEXT,
    owner TEXT NOT NULL,
    approval_status TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS benchmark_evaluation_result (
    benchmark_evaluation_result_id TEXT PRIMARY KEY,
    benchmark_id TEXT NOT NULL,
    model_or_system_id TEXT NOT NULL,
    metric_name TEXT NOT NULL,
    metric_value REAL NOT NULL,
    scenario_or_slice TEXT,
    evaluation_status TEXT NOT NULL,
    evaluated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (benchmark_id) REFERENCES benchmark_environment(benchmark_id)
);

CREATE TABLE IF NOT EXISTS synthetic_governance_review (
    governance_review_id TEXT PRIMARY KEY,
    artifact_or_environment_id TEXT NOT NULL,
    review_type TEXT NOT NULL,
    reviewer TEXT NOT NULL,
    review_date DATE NOT NULL,
    decision TEXT NOT NULL,
    decision_rationale TEXT NOT NULL,
    required_actions TEXT,
    next_review_date DATE
);

CREATE INDEX IF NOT EXISTS idx_synthetic_artifact_type_status
ON synthetic_artifact_registry(artifact_type, approval_status);

CREATE INDEX IF NOT EXISTS idx_fidelity_metric_artifact_status
ON synthetic_fidelity_metric(artifact_id, metric_status);

CREATE INDEX IF NOT EXISTS idx_utility_metric_artifact_task
ON synthetic_utility_metric(artifact_id, task_name, metric_status);

CREATE INDEX IF NOT EXISTS idx_privacy_review_artifact_decision
ON synthetic_privacy_review(artifact_id, review_decision);

CREATE INDEX IF NOT EXISTS idx_sim_scenario_environment_family
ON simulation_scenario(simulation_environment_id, scenario_family, scenario_status);

CREATE VIEW IF NOT EXISTS v_synthetic_artifacts_requiring_review AS
SELECT
    a.artifact_id,
    a.artifact_name,
    a.artifact_type,
    a.artifact_version,
    f.metric_name AS fidelity_metric,
    f.metric_value AS fidelity_value,
    u.utility_gap,
    p.privacy_risk_value
FROM synthetic_artifact_registry a
LEFT JOIN synthetic_fidelity_metric f
    ON a.artifact_id = f.artifact_id
LEFT JOIN synthetic_utility_metric u
    ON a.artifact_id = u.artifact_id
LEFT JOIN synthetic_privacy_review p
    ON a.artifact_id = p.artifact_id
WHERE a.approval_status IN ('review_required', 'restricted')
   OR f.metric_status IN ('warning', 'action')
   OR u.metric_status IN ('warning', 'action')
   OR p.review_decision IN ('restricted', 'rejected', 'requires_remediation');

CREATE VIEW IF NOT EXISTS v_simulation_environments_requiring_validation AS
SELECT
    e.simulation_environment_id,
    e.environment_name,
    e.environment_version,
    e.environment_type,
    v.validation_name,
    v.sim_to_real_gap,
    v.validation_status
FROM simulation_environment e
LEFT JOIN sim_to_real_validation v
    ON e.simulation_environment_id = v.simulation_environment_id
WHERE e.approval_status IN ('review_required', 'restricted')
   OR v.validation_status IN ('warning', 'action', 'failed');
