-- Edge AI and Distributed Intelligence Metadata Schema

CREATE TABLE IF NOT EXISTS edge_ai_projects (
    project_id TEXT PRIMARY KEY,
    project_name TEXT NOT NULL,
    project_owner TEXT NOT NULL,
    intended_use TEXT NOT NULL,
    physical_system_context TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS edge_nodes (
    node_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    node_name TEXT NOT NULL,
    node_type TEXT CHECK(node_type IN ('sensor', 'microcontroller', 'gateway', 'edge_server', 'mobile_device', 'robot', 'vehicle', 'industrial_controller', 'cloud_service', 'other')),
    location_description TEXT,
    compute_capacity_score REAL,
    memory_capacity_score REAL,
    energy_budget_score REAL,
    network_reliability_score REAL,
    node_trust_score REAL,
    owner_or_operator TEXT,
    FOREIGN KEY(project_id) REFERENCES edge_ai_projects(project_id)
);

CREATE TABLE IF NOT EXISTS edge_models (
    model_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    model_name TEXT NOT NULL,
    model_version TEXT NOT NULL,
    model_type TEXT,
    model_compute_demand_score REAL,
    model_memory_demand_score REAL,
    model_energy_demand_score REAL,
    quantized BOOLEAN DEFAULT FALSE,
    compressed BOOLEAN DEFAULT FALSE,
    intended_node_type TEXT,
    FOREIGN KEY(project_id) REFERENCES edge_ai_projects(project_id)
);

CREATE TABLE IF NOT EXISTS edge_deployments (
    deployment_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    node_id TEXT NOT NULL,
    model_id TEXT NOT NULL,
    deployment_date DATE,
    edge_latency_ms REAL,
    cloud_latency_ms REAL,
    latency_budget_ms REAL,
    raw_bandwidth_mb_s REAL,
    edge_output_mb_s REAL,
    deployment_status TEXT CHECK(deployment_status IN ('planned', 'testing', 'active', 'paused', 'retired')),
    FOREIGN KEY(project_id) REFERENCES edge_ai_projects(project_id),
    FOREIGN KEY(node_id) REFERENCES edge_nodes(node_id),
    FOREIGN KEY(model_id) REFERENCES edge_models(model_id)
);

CREATE TABLE IF NOT EXISTS federated_rounds (
    round_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    model_id TEXT NOT NULL,
    round_number INTEGER,
    aggregation_method TEXT CHECK(aggregation_method IN ('fedavg', 'weighted_average', 'secure_aggregation', 'robust_aggregation', 'custom')),
    participating_nodes INTEGER,
    dropped_nodes INTEGER,
    non_iid_risk_score REAL,
    communication_cost_mb REAL,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    FOREIGN KEY(project_id) REFERENCES edge_ai_projects(project_id),
    FOREIGN KEY(model_id) REFERENCES edge_models(model_id)
);

CREATE TABLE IF NOT EXISTS node_update_reviews (
    update_review_id TEXT PRIMARY KEY,
    round_id TEXT NOT NULL,
    node_id TEXT NOT NULL,
    update_received BOOLEAN DEFAULT FALSE,
    update_validated BOOLEAN DEFAULT FALSE,
    anomaly_score REAL,
    trust_weight REAL,
    review_notes TEXT,
    FOREIGN KEY(round_id) REFERENCES federated_rounds(round_id),
    FOREIGN KEY(node_id) REFERENCES edge_nodes(node_id)
);

CREATE TABLE IF NOT EXISTS edge_security_controls (
    control_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    node_id TEXT,
    control_type TEXT CHECK(control_type IN ('secure_boot', 'signed_updates', 'attestation', 'encryption', 'access_control', 'secure_aggregation', 'differential_privacy', 'intrusion_detection', 'incident_response', 'other')),
    control_status TEXT CHECK(control_status IN ('planned', 'active', 'needs_update', 'missing', 'retired')),
    control_owner TEXT,
    notes TEXT,
    FOREIGN KEY(project_id) REFERENCES edge_ai_projects(project_id),
    FOREIGN KEY(node_id) REFERENCES edge_nodes(node_id)
);

CREATE TABLE IF NOT EXISTS distributed_governance_reviews (
    review_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    review_date DATE NOT NULL,
    reviewer TEXT NOT NULL,
    node_inventory_reviewed BOOLEAN DEFAULT FALSE,
    update_control_reviewed BOOLEAN DEFAULT FALSE,
    data_rights_reviewed BOOLEAN DEFAULT FALSE,
    security_reviewed BOOLEAN DEFAULT FALSE,
    latency_safety_reviewed BOOLEAN DEFAULT FALSE,
    auditability_reviewed BOOLEAN DEFAULT FALSE,
    accountability_reviewed BOOLEAN DEFAULT FALSE,
    findings TEXT,
    required_actions TEXT,
    status TEXT CHECK(status IN ('draft', 'approved', 'requires_action', 'closed')),
    FOREIGN KEY(project_id) REFERENCES edge_ai_projects(project_id)
);
