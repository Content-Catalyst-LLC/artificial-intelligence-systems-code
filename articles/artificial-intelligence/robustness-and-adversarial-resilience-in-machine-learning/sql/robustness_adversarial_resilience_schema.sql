-- Robustness and Adversarial Resilience in Machine Learning Metadata Schema

CREATE TABLE IF NOT EXISTS robustness_evaluation_systems (
    system_id TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    system_purpose TEXT NOT NULL,
    owner_team TEXT NOT NULL,
    model_family TEXT,
    deployment_status TEXT CHECK(deployment_status IN ('proposed', 'development', 'pilot', 'production', 'paused', 'retired')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS threat_models (
    threat_model_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    threat_model_name TEXT NOT NULL,
    attacker_goal TEXT,
    attacker_knowledge TEXT CHECK(attacker_knowledge IN ('white_box', 'gray_box', 'black_box', 'unknown')),
    attacker_capability TEXT,
    lifecycle_stage TEXT CHECK(lifecycle_stage IN ('data_collection', 'training', 'evaluation', 'deployment', 'inference', 'monitoring', 'retirement', 'multiple')),
    perturbation_constraint TEXT,
    notes TEXT,
    FOREIGN KEY(system_id) REFERENCES robustness_evaluation_systems(system_id)
);

CREATE TABLE IF NOT EXISTS robustness_test_runs (
    test_run_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    threat_model_id TEXT,
    run_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    dataset_reference TEXT,
    model_version TEXT,
    attack_method TEXT,
    perturbation_budget REAL,
    perturbation_norm TEXT,
    clean_accuracy REAL,
    robust_accuracy REAL,
    robustness_gap REAL,
    evaluation_status TEXT CHECK(evaluation_status IN ('planned', 'running', 'complete', 'failed', 'requires_review')),
    FOREIGN KEY(system_id) REFERENCES robustness_evaluation_systems(system_id),
    FOREIGN KEY(threat_model_id) REFERENCES threat_models(threat_model_id)
);

CREATE TABLE IF NOT EXISTS stress_test_scenarios (
    scenario_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    scenario_name TEXT NOT NULL,
    stress_type TEXT CHECK(stress_type IN ('adversarial', 'corruption', 'distribution_shift', 'physical_world', 'poisoning', 'extraction', 'privacy', 'backdoor', 'runtime')),
    severity_level TEXT CHECK(severity_level IN ('low', 'medium', 'high', 'critical')),
    scenario_description TEXT,
    expected_failure_mode TEXT,
    FOREIGN KEY(system_id) REFERENCES robustness_evaluation_systems(system_id)
);

CREATE TABLE IF NOT EXISTS runtime_incidents (
    incident_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    incident_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    incident_type TEXT CHECK(incident_type IN ('suspected_attack', 'distribution_shift', 'data_corruption', 'model_drift', 'unexpected_output', 'availability_degradation', 'privacy_event')),
    severity TEXT CHECK(severity IN ('low', 'medium', 'high', 'critical')),
    detection_method TEXT,
    containment_action TEXT,
    resolution_status TEXT CHECK(resolution_status IN ('open', 'contained', 'resolved', 'accepted_risk', 'escalated')),
    notes TEXT,
    FOREIGN KEY(system_id) REFERENCES robustness_evaluation_systems(system_id)
);

CREATE TABLE IF NOT EXISTS mitigation_controls (
    control_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    control_name TEXT NOT NULL,
    control_type TEXT CHECK(control_type IN ('adversarial_training', 'input_filtering', 'certification', 'monitoring', 'access_control', 'rate_limit', 'human_review', 'fallback', 'rollback', 'data_provenance', 'red_team')),
    control_owner TEXT,
    implementation_status TEXT CHECK(implementation_status IN ('planned', 'implemented', 'tested', 'retired', 'requires_review')),
    effectiveness_notes TEXT,
    FOREIGN KEY(system_id) REFERENCES robustness_evaluation_systems(system_id)
);

CREATE TABLE IF NOT EXISTS governance_reviews (
    review_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    review_date DATE NOT NULL,
    reviewer TEXT NOT NULL,
    review_scope TEXT,
    findings TEXT,
    required_actions TEXT,
    status TEXT CHECK(status IN ('draft', 'approved', 'requires_action', 'closed')),
    FOREIGN KEY(system_id) REFERENCES robustness_evaluation_systems(system_id)
);
