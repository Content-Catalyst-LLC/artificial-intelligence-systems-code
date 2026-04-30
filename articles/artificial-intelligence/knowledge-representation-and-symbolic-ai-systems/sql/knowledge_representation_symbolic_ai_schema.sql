-- Knowledge Representation and Symbolic AI Systems Metadata Schema

CREATE TABLE IF NOT EXISTS knowledge_bases (
    knowledge_base_id TEXT PRIMARY KEY,
    knowledge_base_name TEXT NOT NULL,
    domain_name TEXT NOT NULL,
    representation_type TEXT CHECK(representation_type IN ('logic', 'rules', 'ontology', 'knowledge_graph', 'frames', 'semantic_network', 'hybrid')),
    version_label TEXT,
    owner_team TEXT,
    provenance_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ontology_classes (
    class_id TEXT PRIMARY KEY,
    knowledge_base_id TEXT NOT NULL,
    class_name TEXT NOT NULL,
    parent_class_id TEXT,
    class_definition TEXT,
    active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY(knowledge_base_id) REFERENCES knowledge_bases(knowledge_base_id),
    FOREIGN KEY(parent_class_id) REFERENCES ontology_classes(class_id)
);

CREATE TABLE IF NOT EXISTS semantic_triples (
    triple_id TEXT PRIMARY KEY,
    knowledge_base_id TEXT NOT NULL,
    subject TEXT NOT NULL,
    predicate TEXT NOT NULL,
    object TEXT NOT NULL,
    confidence_score REAL,
    provenance_source TEXT,
    active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY(knowledge_base_id) REFERENCES knowledge_bases(knowledge_base_id)
);

CREATE TABLE IF NOT EXISTS symbolic_rules (
    rule_id TEXT PRIMARY KEY,
    knowledge_base_id TEXT NOT NULL,
    rule_name TEXT NOT NULL,
    rule_type TEXT CHECK(rule_type IN ('inference', 'constraint', 'default', 'exception', 'governance', 'safety', 'workflow')),
    premise_text TEXT NOT NULL,
    conclusion_text TEXT NOT NULL,
    priority INTEGER DEFAULT 0,
    active BOOLEAN DEFAULT TRUE,
    owner TEXT,
    review_status TEXT CHECK(review_status IN ('draft', 'approved', 'deprecated', 'requires_review')),
    FOREIGN KEY(knowledge_base_id) REFERENCES knowledge_bases(knowledge_base_id)
);

CREATE TABLE IF NOT EXISTS frame_definitions (
    frame_id TEXT PRIMARY KEY,
    knowledge_base_id TEXT NOT NULL,
    frame_name TEXT NOT NULL,
    frame_description TEXT,
    parent_frame_id TEXT,
    active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY(knowledge_base_id) REFERENCES knowledge_bases(knowledge_base_id),
    FOREIGN KEY(parent_frame_id) REFERENCES frame_definitions(frame_id)
);

CREATE TABLE IF NOT EXISTS frame_slots (
    slot_id TEXT PRIMARY KEY,
    frame_id TEXT NOT NULL,
    slot_name TEXT NOT NULL,
    slot_value_type TEXT,
    default_value TEXT,
    required BOOLEAN DEFAULT FALSE,
    FOREIGN KEY(frame_id) REFERENCES frame_definitions(frame_id)
);

CREATE TABLE IF NOT EXISTS inference_runs (
    inference_run_id TEXT PRIMARY KEY,
    knowledge_base_id TEXT NOT NULL,
    run_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    query_text TEXT,
    inference_engine TEXT,
    run_status TEXT CHECK(run_status IN ('started', 'complete', 'failed', 'requires_review')),
    FOREIGN KEY(knowledge_base_id) REFERENCES knowledge_bases(knowledge_base_id)
);

CREATE TABLE IF NOT EXISTS inference_trace_steps (
    trace_step_id TEXT PRIMARY KEY,
    inference_run_id TEXT NOT NULL,
    step_number INTEGER NOT NULL,
    step_type TEXT CHECK(step_type IN ('fact_lookup', 'rule_match', 'rule_fire', 'constraint_check', 'default_apply', 'exception_override', 'conclusion')),
    fact_triple_id TEXT,
    rule_id TEXT,
    step_summary TEXT NOT NULL,
    FOREIGN KEY(inference_run_id) REFERENCES inference_runs(inference_run_id),
    FOREIGN KEY(fact_triple_id) REFERENCES semantic_triples(triple_id),
    FOREIGN KEY(rule_id) REFERENCES symbolic_rules(rule_id)
);

CREATE TABLE IF NOT EXISTS inferred_conclusions (
    conclusion_id TEXT PRIMARY KEY,
    inference_run_id TEXT NOT NULL,
    subject TEXT NOT NULL,
    predicate TEXT NOT NULL,
    object TEXT NOT NULL,
    confidence_score REAL,
    explanation_summary TEXT,
    human_review_required BOOLEAN DEFAULT FALSE,
    FOREIGN KEY(inference_run_id) REFERENCES inference_runs(inference_run_id)
);

CREATE TABLE IF NOT EXISTS governance_reviews (
    review_id TEXT PRIMARY KEY,
    knowledge_base_id TEXT NOT NULL,
    review_date DATE NOT NULL,
    reviewer TEXT NOT NULL,
    review_scope TEXT,
    findings TEXT,
    required_actions TEXT,
    status TEXT CHECK(status IN ('draft', 'approved', 'requires_action', 'closed')),
    FOREIGN KEY(knowledge_base_id) REFERENCES knowledge_bases(knowledge_base_id)
);
