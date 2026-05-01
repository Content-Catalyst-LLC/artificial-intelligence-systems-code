-- Data Governance, Provenance, and Lineage in AI Systems Metadata Schema

CREATE TABLE IF NOT EXISTS governance_projects (
    project_id TEXT PRIMARY KEY,
    project_name TEXT NOT NULL,
    intended_ai_use TEXT NOT NULL,
    governance_owner TEXT NOT NULL,
    data_owner TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS provenance_entities (
    entity_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    entity_name TEXT NOT NULL,
    entity_type TEXT CHECK(entity_type IN ('source_dataset', 'derived_dataset', 'feature_table', 'model', 'evaluation_report', 'deployment_log', 'monitoring_report', 'documentation', 'other')),
    entity_version TEXT,
    storage_location TEXT,
    created_at TIMESTAMP,
    sensitivity_level TEXT CHECK(sensitivity_level IN ('public', 'internal', 'confidential', 'restricted', 'unknown')),
    license_or_rights TEXT,
    retention_policy TEXT,
    FOREIGN KEY(project_id) REFERENCES governance_projects(project_id)
);

CREATE TABLE IF NOT EXISTS provenance_activities (
    activity_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    activity_name TEXT NOT NULL,
    activity_type TEXT CHECK(activity_type IN ('ingestion', 'cleaning', 'transformation', 'labeling', 'feature_engineering', 'training', 'evaluation', 'deployment', 'monitoring', 'review', 'other')),
    started_at TIMESTAMP,
    ended_at TIMESTAMP,
    code_reference TEXT,
    environment_reference TEXT,
    FOREIGN KEY(project_id) REFERENCES governance_projects(project_id)
);

CREATE TABLE IF NOT EXISTS provenance_agents (
    agent_id TEXT PRIMARY KEY,
    agent_name TEXT NOT NULL,
    agent_type TEXT CHECK(agent_type IN ('person', 'team', 'organization', 'software_service', 'workflow', 'other')),
    contact_or_owner TEXT,
    role_description TEXT
);

CREATE TABLE IF NOT EXISTS provenance_relations (
    relation_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    source_id TEXT NOT NULL,
    relation_type TEXT CHECK(relation_type IN ('used_by', 'generated', 'derived_from', 'attributed_to', 'associated_with', 'responsible_for', 'reviewed', 'executed', 'approved', 'other')),
    target_id TEXT NOT NULL,
    relation_timestamp TIMESTAMP,
    notes TEXT,
    FOREIGN KEY(project_id) REFERENCES governance_projects(project_id)
);

CREATE TABLE IF NOT EXISTS data_quality_checks (
    quality_check_id TEXT PRIMARY KEY,
    entity_id TEXT NOT NULL,
    check_name TEXT NOT NULL,
    check_type TEXT CHECK(check_type IN ('accuracy', 'completeness', 'consistency', 'timeliness', 'representativeness', 'schema_validity', 'missingness', 'drift', 'rights', 'other')),
    metric_value REAL,
    threshold_value REAL,
    status TEXT CHECK(status IN ('pass', 'warning', 'fail', 'not_reviewed')),
    checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reviewer TEXT,
    notes TEXT,
    FOREIGN KEY(entity_id) REFERENCES provenance_entities(entity_id)
);

CREATE TABLE IF NOT EXISTS dataset_documentation (
    documentation_id TEXT PRIMARY KEY,
    entity_id TEXT NOT NULL,
    documentation_type TEXT CHECK(documentation_type IN ('datasheet', 'data_card', 'model_card', 'risk_card', 'readme', 'other')),
    documentation_location TEXT,
    intended_use TEXT,
    prohibited_use TEXT,
    known_limitations TEXT,
    maintenance_notes TEXT,
    documentation_complete BOOLEAN DEFAULT FALSE,
    FOREIGN KEY(entity_id) REFERENCES provenance_entities(entity_id)
);

CREATE TABLE IF NOT EXISTS access_controls (
    access_control_id TEXT PRIMARY KEY,
    entity_id TEXT NOT NULL,
    role_name TEXT NOT NULL,
    permission_type TEXT CHECK(permission_type IN ('read', 'write', 'admin', 'execute', 'approve', 'none')),
    purpose_limitation TEXT,
    expiration_date DATE,
    approved_by TEXT,
    FOREIGN KEY(entity_id) REFERENCES provenance_entities(entity_id)
);

CREATE TABLE IF NOT EXISTS governance_reviews (
    review_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    review_date DATE NOT NULL,
    reviewer TEXT NOT NULL,
    provenance_reviewed BOOLEAN DEFAULT FALSE,
    lineage_reviewed BOOLEAN DEFAULT FALSE,
    documentation_reviewed BOOLEAN DEFAULT FALSE,
    data_quality_reviewed BOOLEAN DEFAULT FALSE,
    rights_reviewed BOOLEAN DEFAULT FALSE,
    reproducibility_reviewed BOOLEAN DEFAULT FALSE,
    findings TEXT,
    required_actions TEXT,
    status TEXT CHECK(status IN ('draft', 'approved', 'requires_action', 'closed')),
    FOREIGN KEY(project_id) REFERENCES governance_projects(project_id)
);

CREATE TABLE IF NOT EXISTS lineage_impact_assessments (
    impact_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    source_entity_id TEXT NOT NULL,
    affected_entity_id TEXT NOT NULL,
    affected_entity_type TEXT,
    impact_type TEXT CHECK(impact_type IN ('quality_defect', 'schema_change', 'rights_change', 'privacy_issue', 'drift', 'deprecation', 'other')),
    severity TEXT CHECK(severity IN ('low', 'medium', 'high', 'critical', 'unknown')),
    mitigation_plan TEXT,
    status TEXT CHECK(status IN ('open', 'investigating', 'mitigated', 'closed')),
    FOREIGN KEY(project_id) REFERENCES governance_projects(project_id),
    FOREIGN KEY(source_entity_id) REFERENCES provenance_entities(entity_id)
);
