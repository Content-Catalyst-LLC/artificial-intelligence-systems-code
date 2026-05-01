-- AI Infrastructure: Data Pipelines, Compute, and Deployment Systems Metadata Schema

CREATE TABLE IF NOT EXISTS ai_infrastructure_projects (
    project_id TEXT PRIMARY KEY,
    project_name TEXT NOT NULL,
    project_owner TEXT NOT NULL,
    intended_ai_use TEXT NOT NULL,
    governance_owner TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS pipeline_tasks (
    task_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    task_name TEXT NOT NULL,
    task_type TEXT CHECK(task_type IN ('ingestion', 'validation', 'transformation', 'feature_engineering', 'training', 'evaluation', 'registration', 'deployment', 'monitoring', 'other')),
    upstream_dependencies TEXT,
    expected_duration_minutes REAL,
    failure_probability REAL,
    governance_gate BOOLEAN DEFAULT FALSE,
    code_reference TEXT,
    data_reference TEXT,
    FOREIGN KEY(project_id) REFERENCES ai_infrastructure_projects(project_id)
);

CREATE TABLE IF NOT EXISTS compute_resources (
    resource_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    resource_name TEXT NOT NULL,
    resource_type TEXT CHECK(resource_type IN ('cpu_pool', 'gpu_pool', 'tpu_pool', 'accelerator_cluster', 'edge_device', 'serving_pool', 'other')),
    available_units INTEGER,
    allocated_units INTEGER,
    utilization_target REAL,
    cost_per_hour REAL,
    energy_profile TEXT,
    FOREIGN KEY(project_id) REFERENCES ai_infrastructure_projects(project_id)
);

CREATE TABLE IF NOT EXISTS model_artifacts (
    model_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    model_name TEXT NOT NULL,
    model_version TEXT NOT NULL,
    training_dataset_version TEXT,
    feature_set_version TEXT,
    training_code_reference TEXT,
    environment_reference TEXT,
    evaluation_report_reference TEXT,
    registry_status TEXT CHECK(registry_status IN ('draft', 'validated', 'approved', 'deployed', 'retired')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(project_id) REFERENCES ai_infrastructure_projects(project_id)
);

CREATE TABLE IF NOT EXISTS deployments (
    deployment_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    model_id TEXT NOT NULL,
    service_name TEXT NOT NULL,
    deployment_environment TEXT CHECK(deployment_environment IN ('dev', 'staging', 'production', 'edge', 'hybrid', 'other')),
    replicas INTEGER,
    throughput_per_replica REAL,
    latency_budget_ms REAL,
    observed_p95_latency_ms REAL,
    rollback_available BOOLEAN DEFAULT FALSE,
    deployment_status TEXT CHECK(deployment_status IN ('planned', 'testing', 'active', 'paused', 'retired')),
    deployed_at TIMESTAMP,
    FOREIGN KEY(project_id) REFERENCES ai_infrastructure_projects(project_id),
    FOREIGN KEY(model_id) REFERENCES model_artifacts(model_id)
);

CREATE TABLE IF NOT EXISTS observability_signals (
    signal_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    deployment_id TEXT,
    signal_name TEXT NOT NULL,
    signal_type TEXT CHECK(signal_type IN ('metric', 'log', 'trace', 'model_signal', 'data_signal', 'security_signal', 'other')),
    collection_frequency TEXT,
    alert_threshold REAL,
    owner TEXT,
    status TEXT CHECK(status IN ('planned', 'active', 'needs_update', 'retired')),
    FOREIGN KEY(project_id) REFERENCES ai_infrastructure_projects(project_id),
    FOREIGN KEY(deployment_id) REFERENCES deployments(deployment_id)
);

CREATE TABLE IF NOT EXISTS infrastructure_risk_reviews (
    review_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    review_date DATE NOT NULL,
    reviewer TEXT NOT NULL,
    data_pipeline_reviewed BOOLEAN DEFAULT FALSE,
    compute_reviewed BOOLEAN DEFAULT FALSE,
    storage_reviewed BOOLEAN DEFAULT FALSE,
    serving_reviewed BOOLEAN DEFAULT FALSE,
    observability_reviewed BOOLEAN DEFAULT FALSE,
    security_reviewed BOOLEAN DEFAULT FALSE,
    governance_reviewed BOOLEAN DEFAULT FALSE,
    findings TEXT,
    required_actions TEXT,
    status TEXT CHECK(status IN ('draft', 'approved', 'requires_action', 'closed')),
    FOREIGN KEY(project_id) REFERENCES ai_infrastructure_projects(project_id)
);

CREATE TABLE IF NOT EXISTS ai_infrastructure_incidents (
    incident_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    deployment_id TEXT,
    incident_date DATE NOT NULL,
    incident_type TEXT CHECK(incident_type IN ('pipeline_failure', 'data_quality', 'training_failure', 'serving_failure', 'latency', 'drift', 'security', 'governance', 'other')),
    severity TEXT CHECK(severity IN ('low', 'medium', 'high', 'critical', 'unknown')),
    description TEXT NOT NULL,
    root_cause TEXT,
    corrective_action TEXT,
    status TEXT CHECK(status IN ('open', 'investigating', 'mitigated', 'closed')),
    FOREIGN KEY(project_id) REFERENCES ai_infrastructure_projects(project_id),
    FOREIGN KEY(deployment_id) REFERENCES deployments(deployment_id)
);
