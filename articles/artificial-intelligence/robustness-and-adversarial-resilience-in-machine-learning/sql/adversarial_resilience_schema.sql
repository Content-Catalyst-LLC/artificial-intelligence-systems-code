-- Robustness and Adversarial Resilience in Machine Learning
-- SQL schema for adversarial threat models, robustness tests,
-- attack scenarios, red-team findings, controls, incidents,
-- rollback records, and governance review.

CREATE TABLE IF NOT EXISTS ai_system_registry (
    ai_system_id TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    system_version TEXT NOT NULL,
    system_type TEXT NOT NULL,
    intended_use TEXT NOT NULL,
    risk_level TEXT NOT NULL,
    owner TEXT NOT NULL,
    deployment_status TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS adversarial_threat_model (
    threat_model_id TEXT PRIMARY KEY,
    ai_system_id TEXT NOT NULL,
    threat_model_name TEXT NOT NULL,
    attacker_goal TEXT NOT NULL,
    attacker_capability TEXT NOT NULL,
    attacker_knowledge TEXT NOT NULL,
    protected_assets TEXT NOT NULL,
    review_status TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ai_system_id) REFERENCES ai_system_registry(ai_system_id)
);

CREATE TABLE IF NOT EXISTS attack_scenario (
    attack_scenario_id TEXT PRIMARY KEY,
    threat_model_id TEXT NOT NULL,
    attack_type TEXT NOT NULL,
    lifecycle_stage TEXT NOT NULL,
    attack_surface TEXT NOT NULL,
    expected_impact TEXT NOT NULL,
    likelihood_score REAL,
    impact_score REAL,
    scenario_status TEXT NOT NULL,
    FOREIGN KEY (threat_model_id) REFERENCES adversarial_threat_model(threat_model_id)
);

CREATE TABLE IF NOT EXISTS robustness_test_run (
    robustness_test_run_id TEXT PRIMARY KEY,
    ai_system_id TEXT NOT NULL,
    test_name TEXT NOT NULL,
    test_type TEXT NOT NULL,
    reference_model_version TEXT NOT NULL,
    test_dataset_version TEXT,
    test_status TEXT NOT NULL,
    started_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    FOREIGN KEY (ai_system_id) REFERENCES ai_system_registry(ai_system_id)
);

CREATE TABLE IF NOT EXISTS robustness_metric (
    robustness_metric_id TEXT PRIMARY KEY,
    robustness_test_run_id TEXT NOT NULL,
    attack_scenario_id TEXT,
    metric_name TEXT NOT NULL,
    metric_value REAL NOT NULL,
    warning_threshold REAL,
    action_threshold REAL,
    metric_status TEXT NOT NULL,
    measured_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (robustness_test_run_id) REFERENCES robustness_test_run(robustness_test_run_id),
    FOREIGN KEY (attack_scenario_id) REFERENCES attack_scenario(attack_scenario_id)
);

CREATE TABLE IF NOT EXISTS red_team_finding (
    red_team_finding_id TEXT PRIMARY KEY,
    ai_system_id TEXT NOT NULL,
    attack_scenario_id TEXT,
    finding_title TEXT NOT NULL,
    finding_severity TEXT NOT NULL,
    finding_status TEXT NOT NULL,
    finding_summary TEXT NOT NULL,
    remediation_required TEXT,
    detected_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP,
    FOREIGN KEY (ai_system_id) REFERENCES ai_system_registry(ai_system_id),
    FOREIGN KEY (attack_scenario_id) REFERENCES attack_scenario(attack_scenario_id)
);

CREATE TABLE IF NOT EXISTS adversarial_control (
    adversarial_control_id TEXT PRIMARY KEY,
    ai_system_id TEXT NOT NULL,
    control_name TEXT NOT NULL,
    control_type TEXT NOT NULL,
    attack_type_addressed TEXT,
    implementation_status TEXT NOT NULL,
    owner TEXT,
    last_reviewed_at TIMESTAMP,
    FOREIGN KEY (ai_system_id) REFERENCES ai_system_registry(ai_system_id)
);

CREATE TABLE IF NOT EXISTS adversarial_incident (
    incident_id TEXT PRIMARY KEY,
    ai_system_id TEXT NOT NULL,
    attack_type TEXT NOT NULL,
    incident_severity TEXT NOT NULL,
    incident_status TEXT NOT NULL,
    description TEXT NOT NULL,
    containment_action TEXT,
    remediation_summary TEXT,
    detected_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP,
    FOREIGN KEY (ai_system_id) REFERENCES ai_system_registry(ai_system_id)
);

CREATE TABLE IF NOT EXISTS rollback_record (
    rollback_id TEXT PRIMARY KEY,
    ai_system_id TEXT NOT NULL,
    from_system_version TEXT NOT NULL,
    to_system_version TEXT NOT NULL,
    rollback_reason TEXT NOT NULL,
    rollback_status TEXT NOT NULL,
    executed_by TEXT,
    executed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ai_system_id) REFERENCES ai_system_registry(ai_system_id)
);

CREATE TABLE IF NOT EXISTS resilience_governance_review (
    governance_review_id TEXT PRIMARY KEY,
    ai_system_id TEXT NOT NULL,
    review_type TEXT NOT NULL,
    reviewer TEXT NOT NULL,
    review_date DATE NOT NULL,
    decision TEXT NOT NULL,
    decision_rationale TEXT NOT NULL,
    required_actions TEXT,
    next_review_date DATE,
    FOREIGN KEY (ai_system_id) REFERENCES ai_system_registry(ai_system_id)
);

CREATE TABLE IF NOT EXISTS adversarial_monitoring_signal (
    monitoring_signal_id TEXT PRIMARY KEY,
    ai_system_id TEXT NOT NULL,
    signal_name TEXT NOT NULL,
    signal_value REAL NOT NULL,
    signal_category TEXT NOT NULL,
    threshold_warning REAL,
    threshold_action REAL,
    signal_status TEXT NOT NULL,
    measured_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ai_system_id) REFERENCES ai_system_registry(ai_system_id)
);

CREATE INDEX IF NOT EXISTS idx_threat_model_system
ON adversarial_threat_model(ai_system_id, review_status);

CREATE INDEX IF NOT EXISTS idx_attack_scenario_type_stage
ON attack_scenario(attack_type, lifecycle_stage, scenario_status);

CREATE INDEX IF NOT EXISTS idx_robustness_metric_status
ON robustness_metric(robustness_test_run_id, metric_status);

CREATE INDEX IF NOT EXISTS idx_red_team_finding_status
ON red_team_finding(ai_system_id, finding_status, finding_severity);

CREATE INDEX IF NOT EXISTS idx_adversarial_incident_status
ON adversarial_incident(ai_system_id, incident_status, incident_severity);

CREATE VIEW IF NOT EXISTS v_open_adversarial_findings AS
SELECT
    f.red_team_finding_id,
    s.system_name,
    s.system_version,
    f.finding_title,
    f.finding_severity,
    f.finding_status,
    a.attack_type,
    a.lifecycle_stage
FROM red_team_finding f
JOIN ai_system_registry s
    ON f.ai_system_id = s.ai_system_id
LEFT JOIN attack_scenario a
    ON f.attack_scenario_id = a.attack_scenario_id
WHERE f.finding_status IN ('open', 'investigating', 'requires_action');

CREATE VIEW IF NOT EXISTS v_high_risk_attack_scenarios AS
SELECT
    s.system_name,
    t.threat_model_name,
    a.attack_type,
    a.lifecycle_stage,
    a.attack_surface,
    a.likelihood_score,
    a.impact_score,
    (a.likelihood_score * a.impact_score) AS scenario_risk_score
FROM attack_scenario a
JOIN adversarial_threat_model t
    ON a.threat_model_id = t.threat_model_id
JOIN ai_system_registry s
    ON t.ai_system_id = s.ai_system_id
WHERE (a.likelihood_score * a.impact_score) >= 0.35;
