-- AI Systems for Infrastructure and Smart Networks
-- SQL schema for smart infrastructure governance, telemetry, digital twins,
-- maintenance decisions, incidents, and cyber-physical assurance.

CREATE TABLE IF NOT EXISTS infrastructure_system (
    system_id TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    infrastructure_domain TEXT NOT NULL,
    jurisdiction TEXT,
    operator_name TEXT,
    public_purpose TEXT NOT NULL,
    risk_classification TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    retired_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS infrastructure_asset (
    asset_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    asset_name TEXT,
    asset_type TEXT NOT NULL,
    location_reference TEXT,
    service_population INTEGER,
    installation_year INTEGER,
    owner_team TEXT,
    criticality_class TEXT,
    equity_priority INTEGER NOT NULL DEFAULT 0,
    climate_exposure_score REAL,
    FOREIGN KEY (system_id) REFERENCES infrastructure_system(system_id)
);

CREATE TABLE IF NOT EXISTS infrastructure_edge (
    edge_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    source_asset_id TEXT NOT NULL,
    target_asset_id TEXT NOT NULL,
    edge_type TEXT NOT NULL,
    capacity REAL,
    dependency_description TEXT,
    FOREIGN KEY (system_id) REFERENCES infrastructure_system(system_id),
    FOREIGN KEY (source_asset_id) REFERENCES infrastructure_asset(asset_id),
    FOREIGN KEY (target_asset_id) REFERENCES infrastructure_asset(asset_id)
);

CREATE TABLE IF NOT EXISTS sensor_device (
    sensor_id TEXT PRIMARY KEY,
    asset_id TEXT NOT NULL,
    sensor_type TEXT NOT NULL,
    unit TEXT,
    calibration_status TEXT,
    installed_at TIMESTAMP,
    last_calibrated_at TIMESTAMP,
    sensor_health_score REAL,
    data_owner TEXT,
    FOREIGN KEY (asset_id) REFERENCES infrastructure_asset(asset_id)
);

CREATE TABLE IF NOT EXISTS sensor_telemetry (
    telemetry_id TEXT PRIMARY KEY,
    sensor_id TEXT NOT NULL,
    asset_id TEXT NOT NULL,
    observed_at TIMESTAMP NOT NULL,
    metric_name TEXT NOT NULL,
    metric_value REAL NOT NULL,
    unit TEXT,
    quality_flag TEXT,
    ingestion_latency_seconds REAL,
    FOREIGN KEY (sensor_id) REFERENCES sensor_device(sensor_id),
    FOREIGN KEY (asset_id) REFERENCES infrastructure_asset(asset_id)
);

CREATE TABLE IF NOT EXISTS digital_twin_model (
    twin_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    twin_name TEXT NOT NULL,
    model_version TEXT NOT NULL,
    scope_description TEXT NOT NULL,
    calibration_summary TEXT,
    uncertainty_summary TEXT,
    approved_use TEXT,
    prohibited_use TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (system_id) REFERENCES infrastructure_system(system_id)
);

CREATE TABLE IF NOT EXISTS infrastructure_ai_model (
    model_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    twin_id TEXT,
    model_name TEXT NOT NULL,
    model_version TEXT NOT NULL,
    model_purpose TEXT NOT NULL,
    training_data_summary TEXT,
    validation_summary TEXT,
    known_limitations TEXT,
    approval_status TEXT NOT NULL,
    approved_at TIMESTAMP,
    FOREIGN KEY (system_id) REFERENCES infrastructure_system(system_id),
    FOREIGN KEY (twin_id) REFERENCES digital_twin_model(twin_id)
);

CREATE TABLE IF NOT EXISTS asset_risk_score (
    risk_score_id TEXT PRIMARY KEY,
    asset_id TEXT NOT NULL,
    model_id TEXT NOT NULL,
    scored_at TIMESTAMP NOT NULL,
    failure_probability REAL,
    network_centrality_score REAL,
    data_quality_risk REAL,
    climate_exposure_score REAL,
    equity_priority INTEGER,
    criticality_score REAL,
    review_required INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (asset_id) REFERENCES infrastructure_asset(asset_id),
    FOREIGN KEY (model_id) REFERENCES infrastructure_ai_model(model_id)
);

CREATE TABLE IF NOT EXISTS maintenance_recommendation (
    recommendation_id TEXT PRIMARY KEY,
    risk_score_id TEXT NOT NULL,
    asset_id TEXT NOT NULL,
    recommended_action TEXT NOT NULL,
    recommendation_reason TEXT,
    urgency_class TEXT,
    estimated_cost REAL,
    human_review_status TEXT NOT NULL,
    final_decision TEXT,
    decision_rationale TEXT,
    decided_by TEXT,
    decided_at TIMESTAMP,
    FOREIGN KEY (risk_score_id) REFERENCES asset_risk_score(risk_score_id),
    FOREIGN KEY (asset_id) REFERENCES infrastructure_asset(asset_id)
);

CREATE TABLE IF NOT EXISTS infrastructure_alert (
    alert_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    asset_id TEXT,
    alert_type TEXT NOT NULL,
    severity TEXT NOT NULL,
    alert_status TEXT NOT NULL,
    detected_at TIMESTAMP NOT NULL,
    resolved_at TIMESTAMP,
    description TEXT NOT NULL,
    FOREIGN KEY (system_id) REFERENCES infrastructure_system(system_id),
    FOREIGN KEY (asset_id) REFERENCES infrastructure_asset(asset_id)
);

CREATE TABLE IF NOT EXISTS infrastructure_incident (
    incident_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    incident_type TEXT NOT NULL,
    severity TEXT NOT NULL,
    affected_assets TEXT,
    affected_population_estimate INTEGER,
    detected_at TIMESTAMP NOT NULL,
    contained_at TIMESTAMP,
    resolved_at TIMESTAMP,
    root_cause_summary TEXT,
    remediation_summary TEXT,
    public_reporting_required INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (system_id) REFERENCES infrastructure_system(system_id)
);

CREATE TABLE IF NOT EXISTS governance_review (
    review_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    review_type TEXT NOT NULL,
    reviewer TEXT NOT NULL,
    review_date DATE NOT NULL,
    decision TEXT NOT NULL,
    decision_rationale TEXT NOT NULL,
    required_actions TEXT,
    next_review_date DATE,
    FOREIGN KEY (system_id) REFERENCES infrastructure_system(system_id)
);

CREATE INDEX IF NOT EXISTS idx_telemetry_asset_time
ON sensor_telemetry(asset_id, observed_at);

CREATE INDEX IF NOT EXISTS idx_risk_asset_time
ON asset_risk_score(asset_id, scored_at);

CREATE INDEX IF NOT EXISTS idx_alert_system_status
ON infrastructure_alert(system_id, alert_status, severity);

CREATE VIEW IF NOT EXISTS v_high_priority_assets AS
SELECT
    a.asset_id,
    a.asset_name,
    a.asset_type,
    a.service_population,
    a.equity_priority,
    r.failure_probability,
    r.network_centrality_score,
    r.data_quality_risk,
    r.climate_exposure_score,
    r.criticality_score,
    r.review_required,
    r.scored_at
FROM infrastructure_asset a
JOIN asset_risk_score r
    ON a.asset_id = r.asset_id
WHERE r.criticality_score >= 0.60
   OR r.review_required = 1;

CREATE VIEW IF NOT EXISTS v_sensor_health_review AS
SELECT
    a.asset_id,
    a.asset_name,
    s.sensor_id,
    s.sensor_type,
    s.calibration_status,
    s.sensor_health_score,
    s.last_calibrated_at
FROM infrastructure_asset a
JOIN sensor_device s
    ON a.asset_id = s.asset_id
WHERE s.sensor_health_score < 0.75
   OR s.calibration_status NOT IN ('current', 'valid');

CREATE VIEW IF NOT EXISTS v_open_infrastructure_incidents AS
SELECT
    i.incident_id,
    sys.system_name,
    i.incident_type,
    i.severity,
    i.affected_population_estimate,
    i.detected_at,
    i.public_reporting_required
FROM infrastructure_incident i
JOIN infrastructure_system sys
    ON i.system_id = sys.system_id
WHERE i.resolved_at IS NULL;
