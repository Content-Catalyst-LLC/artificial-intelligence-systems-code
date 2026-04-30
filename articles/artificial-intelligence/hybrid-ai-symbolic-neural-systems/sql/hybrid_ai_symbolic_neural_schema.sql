-- Hybrid AI: Symbolic + Neural Systems Metadata Schema

CREATE TABLE IF NOT EXISTS hybrid_ai_systems (
    system_id TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    system_purpose TEXT NOT NULL,
    owner_team TEXT NOT NULL,
    neural_component_description TEXT,
    symbolic_component_description TEXT,
    deployment_status TEXT CHECK(deployment_status IN ('proposed', 'development', 'pilot', 'production', 'paused', 'retired')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS neural_model_versions (
    model_version_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    model_family TEXT NOT NULL,
    training_dataset_uri TEXT,
    objective_name TEXT,
    model_card_uri TEXT,
    git_commit_hash TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(system_id) REFERENCES hybrid_ai_systems(system_id)
);

CREATE TABLE IF NOT EXISTS symbolic_knowledge_bases (
    knowledge_base_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    knowledge_base_name TEXT NOT NULL,
    representation_type TEXT CHECK(representation_type IN ('rules', 'ontology', 'knowledge_graph', 'semantic_layer', 'hybrid')),
    version_label TEXT,
    provenance_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(system_id) REFERENCES hybrid_ai_systems(system_id)
);

CREATE TABLE IF NOT EXISTS symbolic_facts (
    fact_id TEXT PRIMARY KEY,
    knowledge_base_id TEXT NOT NULL,
    subject TEXT NOT NULL,
    predicate TEXT NOT NULL,
    object TEXT NOT NULL,
    confidence_score REAL,
    provenance_source TEXT,
    active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY(knowledge_base_id) REFERENCES symbolic_knowledge_bases(knowledge_base_id)
);

CREATE TABLE IF NOT EXISTS symbolic_rules (
    rule_id TEXT PRIMARY KEY,
    knowledge_base_id TEXT NOT NULL,
    rule_name TEXT NOT NULL,
    rule_type TEXT CHECK(rule_type IN ('constraint', 'inference', 'governance', 'safety', 'workflow')),
    premise_text TEXT NOT NULL,
    conclusion_text TEXT NOT NULL,
    active BOOLEAN DEFAULT TRUE,
    owner TEXT,
    review_status TEXT,
    FOREIGN KEY(knowledge_base_id) REFERENCES symbolic_knowledge_bases(knowledge_base_id)
);

CREATE TABLE IF NOT EXISTS hybrid_decision_runs (
    run_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    model_version_id TEXT,
    knowledge_base_id TEXT,
    run_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    input_reference TEXT,
    neural_output TEXT,
    final_decision TEXT,
    decision_source TEXT CHECK(decision_source IN ('neural_only', 'symbolic_only', 'neural_and_symbolic', 'human_review', 'no_decision')),
    human_review_required BOOLEAN DEFAULT FALSE,
    FOREIGN KEY(system_id) REFERENCES hybrid_ai_systems(system_id),
    FOREIGN KEY(model_version_id) REFERENCES neural_model_versions(model_version_id),
    FOREIGN KEY(knowledge_base_id) REFERENCES symbolic_knowledge_bases(knowledge_base_id)
);

CREATE TABLE IF NOT EXISTS hybrid_trace_steps (
    trace_step_id TEXT PRIMARY KEY,
    run_id TEXT NOT NULL,
    step_number INTEGER NOT NULL,
    step_type TEXT CHECK(step_type IN ('neural_prediction', 'retrieval', 'fact_lookup', 'rule_check', 'constraint_violation', 'human_review', 'final_decision')),
    step_summary TEXT NOT NULL,
    evidence_reference TEXT,
    rule_id TEXT,
    fact_id TEXT,
    FOREIGN KEY(run_id) REFERENCES hybrid_decision_runs(run_id),
    FOREIGN KEY(rule_id) REFERENCES symbolic_rules(rule_id),
    FOREIGN KEY(fact_id) REFERENCES symbolic_facts(fact_id)
);

CREATE TABLE IF NOT EXISTS constraint_violations (
    violation_id TEXT PRIMARY KEY,
    run_id TEXT NOT NULL,
    rule_id TEXT NOT NULL,
    violation_severity TEXT CHECK(violation_severity IN ('low', 'medium', 'high', 'critical')),
    violation_summary TEXT NOT NULL,
    remediation_status TEXT CHECK(remediation_status IN ('open', 'reviewed', 'mitigated', 'accepted', 'closed')),
    FOREIGN KEY(run_id) REFERENCES hybrid_decision_runs(run_id),
    FOREIGN KEY(rule_id) REFERENCES symbolic_rules(rule_id)
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
    FOREIGN KEY(system_id) REFERENCES hybrid_ai_systems(system_id)
);
