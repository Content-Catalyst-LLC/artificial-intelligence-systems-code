-- Knowledge Representation and Artificial Reasoning Metadata Schema

CREATE TABLE IF NOT EXISTS knowledge_systems (
    system_id TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    system_purpose TEXT NOT NULL,
    owner_team TEXT NOT NULL,
    risk_tier TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS knowledge_bases (
    knowledge_base_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    knowledge_base_name TEXT NOT NULL,
    representation_type TEXT CHECK(representation_type IN ('rules', 'ontology', 'knowledge_graph', 'frames', 'probabilistic_graph', 'hybrid')),
    domain_name TEXT,
    version_label TEXT,
    provenance_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(system_id) REFERENCES knowledge_systems(system_id)
);

CREATE TABLE IF NOT EXISTS entities (
    entity_id TEXT PRIMARY KEY,
    knowledge_base_id TEXT NOT NULL,
    entity_name TEXT NOT NULL,
    entity_type TEXT,
    definition TEXT,
    provenance_source TEXT,
    FOREIGN KEY(knowledge_base_id) REFERENCES knowledge_bases(knowledge_base_id)
);

CREATE TABLE IF NOT EXISTS triples (
    triple_id TEXT PRIMARY KEY,
    knowledge_base_id TEXT NOT NULL,
    subject_id TEXT NOT NULL,
    predicate TEXT NOT NULL,
    object_id TEXT NOT NULL,
    confidence_score REAL,
    provenance_source TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(knowledge_base_id) REFERENCES knowledge_bases(knowledge_base_id),
    FOREIGN KEY(subject_id) REFERENCES entities(entity_id),
    FOREIGN KEY(object_id) REFERENCES entities(entity_id)
);

CREATE TABLE IF NOT EXISTS rules (
    rule_id TEXT PRIMARY KEY,
    knowledge_base_id TEXT NOT NULL,
    rule_name TEXT NOT NULL,
    rule_type TEXT CHECK(rule_type IN ('deductive', 'default', 'probabilistic', 'constraint', 'causal')),
    premise_text TEXT NOT NULL,
    conclusion_text TEXT NOT NULL,
    active BOOLEAN DEFAULT TRUE,
    review_status TEXT,
    FOREIGN KEY(knowledge_base_id) REFERENCES knowledge_bases(knowledge_base_id)
);

CREATE TABLE IF NOT EXISTS inference_runs (
    inference_run_id TEXT PRIMARY KEY,
    knowledge_base_id TEXT NOT NULL,
    run_date DATE NOT NULL,
    query_text TEXT,
    reasoning_method TEXT,
    inferred_conclusion TEXT,
    confidence_score REAL,
    explanation_trace_uri TEXT,
    reviewer TEXT,
    review_status TEXT,
    FOREIGN KEY(knowledge_base_id) REFERENCES knowledge_bases(knowledge_base_id)
);

CREATE TABLE IF NOT EXISTS inference_trace_steps (
    trace_step_id TEXT PRIMARY KEY,
    inference_run_id TEXT NOT NULL,
    step_number INTEGER NOT NULL,
    rule_id TEXT,
    input_fact_text TEXT,
    output_fact_text TEXT,
    notes TEXT,
    FOREIGN KEY(inference_run_id) REFERENCES inference_runs(inference_run_id),
    FOREIGN KEY(rule_id) REFERENCES rules(rule_id)
);

CREATE TABLE IF NOT EXISTS governance_reviews (
    review_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    review_date DATE NOT NULL,
    reviewer TEXT NOT NULL,
    review_scope TEXT,
    findings TEXT,
    required_actions TEXT,
    status TEXT,
    FOREIGN KEY(system_id) REFERENCES knowledge_systems(system_id)
);
