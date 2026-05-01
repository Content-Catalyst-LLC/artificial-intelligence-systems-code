-- Artificial Intelligence in Environmental Monitoring
-- SQL schema for environmental monitoring systems, sensors, observations,
-- Earth observation products, model outputs, alerts, validation, and governance.

CREATE TABLE IF NOT EXISTS environmental_monitoring_system (
    system_id TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    monitoring_domain TEXT NOT NULL,
    geographic_scope TEXT,
    public_purpose TEXT NOT NULL,
    system_owner TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS monitoring_zone (
    zone_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    zone_name TEXT,
    region_type TEXT,
    location_reference TEXT,
    population_exposure INTEGER,
    ecosystem_type TEXT,
    environmental_justice_priority INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (system_id) REFERENCES environmental_monitoring_system(system_id)
);

CREATE TABLE IF NOT EXISTS sensor_station (
    station_id TEXT PRIMARY KEY,
    zone_id TEXT NOT NULL,
    station_name TEXT,
    station_type TEXT NOT NULL,
    latitude REAL,
    longitude REAL,
    calibration_status TEXT,
    sensor_health_score REAL,
    installed_at TIMESTAMP,
    last_calibrated_at TIMESTAMP,
    FOREIGN KEY (zone_id) REFERENCES monitoring_zone(zone_id)
);

CREATE TABLE IF NOT EXISTS environmental_observation (
    observation_id TEXT PRIMARY KEY,
    station_id TEXT NOT NULL,
    zone_id TEXT NOT NULL,
    observed_at TIMESTAMP NOT NULL,
    variable_name TEXT NOT NULL,
    variable_value REAL NOT NULL,
    unit TEXT,
    quality_flag TEXT,
    uncertainty_value REAL,
    ingestion_latency_seconds REAL,
    FOREIGN KEY (station_id) REFERENCES sensor_station(station_id),
    FOREIGN KEY (zone_id) REFERENCES monitoring_zone(zone_id)
);

CREATE TABLE IF NOT EXISTS earth_observation_product (
    product_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    provider TEXT NOT NULL,
    product_name TEXT NOT NULL,
    spatial_resolution TEXT,
    temporal_resolution TEXT,
    bands_or_variables TEXT,
    processing_level TEXT,
    uncertainty_summary TEXT,
    access_uri TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (system_id) REFERENCES environmental_monitoring_system(system_id)
);

CREATE TABLE IF NOT EXISTS environmental_ai_model (
    model_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    model_name TEXT NOT NULL,
    model_version TEXT NOT NULL,
    model_purpose TEXT NOT NULL,
    training_data_summary TEXT,
    validation_summary TEXT,
    uncertainty_summary TEXT,
    known_limitations TEXT,
    approval_status TEXT NOT NULL,
    approved_at TIMESTAMP,
    FOREIGN KEY (system_id) REFERENCES environmental_monitoring_system(system_id)
);

CREATE TABLE IF NOT EXISTS environmental_model_output (
    output_id TEXT PRIMARY KEY,
    model_id TEXT NOT NULL,
    zone_id TEXT NOT NULL,
    output_timestamp TIMESTAMP NOT NULL,
    stress_probability REAL,
    anomaly_score REAL,
    data_quality_risk REAL,
    uncertainty_score REAL,
    priority_score REAL,
    human_review_required INTEGER NOT NULL DEFAULT 0,
    explanation_uri TEXT,
    FOREIGN KEY (model_id) REFERENCES environmental_ai_model(model_id),
    FOREIGN KEY (zone_id) REFERENCES monitoring_zone(zone_id)
);

CREATE TABLE IF NOT EXISTS environmental_alert (
    alert_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    zone_id TEXT NOT NULL,
    output_id TEXT,
    alert_type TEXT NOT NULL,
    severity TEXT NOT NULL,
    alert_status TEXT NOT NULL,
    detected_at TIMESTAMP NOT NULL,
    verified_at TIMESTAMP,
    resolved_at TIMESTAMP,
    description TEXT NOT NULL,
    public_notification_required INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (system_id) REFERENCES environmental_monitoring_system(system_id),
    FOREIGN KEY (zone_id) REFERENCES monitoring_zone(zone_id),
    FOREIGN KEY (output_id) REFERENCES environmental_model_output(output_id)
);

CREATE TABLE IF NOT EXISTS validation_event (
    validation_id TEXT PRIMARY KEY,
    model_id TEXT NOT NULL,
    zone_id TEXT,
    validation_type TEXT NOT NULL,
    validation_date DATE NOT NULL,
    reference_data_source TEXT,
    validation_metric TEXT,
    validation_value REAL,
    validation_summary TEXT,
    passed INTEGER NOT NULL,
    FOREIGN KEY (model_id) REFERENCES environmental_ai_model(model_id),
    FOREIGN KEY (zone_id) REFERENCES monitoring_zone(zone_id)
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
    FOREIGN KEY (system_id) REFERENCES environmental_monitoring_system(system_id)
);

CREATE INDEX IF NOT EXISTS idx_observation_zone_time
ON environmental_observation(zone_id, observed_at);

CREATE INDEX IF NOT EXISTS idx_output_zone_time
ON environmental_model_output(zone_id, output_timestamp);

CREATE INDEX IF NOT EXISTS idx_alert_status
ON environmental_alert(system_id, alert_status, severity);

CREATE VIEW IF NOT EXISTS v_high_priority_environmental_zones AS
SELECT
    z.zone_id,
    z.zone_name,
    z.region_type,
    z.population_exposure,
    z.environmental_justice_priority,
    o.stress_probability,
    o.anomaly_score,
    o.data_quality_risk,
    o.uncertainty_score,
    o.priority_score,
    o.human_review_required,
    o.output_timestamp
FROM monitoring_zone z
JOIN environmental_model_output o
    ON z.zone_id = o.zone_id
WHERE o.priority_score >= 0.60
   OR o.human_review_required = 1;

CREATE VIEW IF NOT EXISTS v_open_environmental_alerts AS
SELECT
    a.alert_id,
    s.system_name,
    z.zone_name,
    a.alert_type,
    a.severity,
    a.alert_status,
    a.detected_at,
    a.public_notification_required
FROM environmental_alert a
JOIN environmental_monitoring_system s
    ON a.system_id = s.system_id
JOIN monitoring_zone z
    ON a.zone_id = z.zone_id
WHERE a.alert_status NOT IN ('resolved', 'closed');
