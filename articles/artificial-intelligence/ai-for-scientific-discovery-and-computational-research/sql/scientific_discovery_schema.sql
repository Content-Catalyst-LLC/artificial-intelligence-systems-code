-- AI for Scientific Discovery and Computational Research
-- SQL schema for projects, datasets, experiments, simulations, candidates,
-- hypotheses, model runs, validation, and reproducibility metadata.

CREATE TABLE IF NOT EXISTS scientific_project (
    project_id TEXT PRIMARY KEY,
    project_name TEXT NOT NULL,
    scientific_domain TEXT NOT NULL,
    research_question TEXT NOT NULL,
    principal_investigator TEXT,
    public_purpose TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS scientific_dataset (
    dataset_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    dataset_name TEXT NOT NULL,
    dataset_role TEXT NOT NULL,
    source_description TEXT,
    measurement_method TEXT,
    known_limitations TEXT,
    license TEXT,
    version TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES scientific_project(project_id)
);

CREATE TABLE IF NOT EXISTS computational_environment (
    environment_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    environment_name TEXT NOT NULL,
    language_runtime TEXT,
    package_manifest_uri TEXT,
    container_uri TEXT,
    hardware_summary TEXT,
    random_seed TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES scientific_project(project_id)
);

CREATE TABLE IF NOT EXISTS scientific_candidate (
    candidate_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    candidate_type TEXT NOT NULL,
    candidate_description TEXT,
    feature_payload_uri TEXT,
    feasibility_score REAL,
    safety_score REAL,
    cost_score REAL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES scientific_project(project_id)
);

CREATE TABLE IF NOT EXISTS experiment_run (
    experiment_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    candidate_id TEXT,
    experiment_type TEXT NOT NULL,
    protocol_uri TEXT,
    experiment_status TEXT NOT NULL,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    measured_property REAL,
    uncertainty_value REAL,
    notes TEXT,
    FOREIGN KEY (project_id) REFERENCES scientific_project(project_id),
    FOREIGN KEY (candidate_id) REFERENCES scientific_candidate(candidate_id)
);

CREATE TABLE IF NOT EXISTS simulation_run (
    simulation_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    candidate_id TEXT,
    simulator_name TEXT NOT NULL,
    simulator_version TEXT,
    parameter_payload_uri TEXT,
    output_payload_uri TEXT,
    runtime_seconds REAL,
    simulation_status TEXT NOT NULL,
    completed_at TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES scientific_project(project_id),
    FOREIGN KEY (candidate_id) REFERENCES scientific_candidate(candidate_id)
);

CREATE TABLE IF NOT EXISTS ai_model_run (
    model_run_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    model_name TEXT NOT NULL,
    model_version TEXT,
    model_purpose TEXT NOT NULL,
    training_dataset_id TEXT,
    validation_dataset_id TEXT,
    environment_id TEXT,
    hyperparameter_payload_uri TEXT,
    metric_summary TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES scientific_project(project_id),
    FOREIGN KEY (training_dataset_id) REFERENCES scientific_dataset(dataset_id),
    FOREIGN KEY (validation_dataset_id) REFERENCES scientific_dataset(dataset_id),
    FOREIGN KEY (environment_id) REFERENCES computational_environment(environment_id)
);

CREATE TABLE IF NOT EXISTS candidate_prediction (
    prediction_id TEXT PRIMARY KEY,
    model_run_id TEXT NOT NULL,
    candidate_id TEXT NOT NULL,
    predicted_property REAL,
    uncertainty_score REAL,
    acquisition_score REAL,
    prediction_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    selected_for_experiment INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (model_run_id) REFERENCES ai_model_run(model_run_id),
    FOREIGN KEY (candidate_id) REFERENCES scientific_candidate(candidate_id)
);

CREATE TABLE IF NOT EXISTS scientific_hypothesis (
    hypothesis_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    hypothesis_text TEXT NOT NULL,
    generated_by TEXT NOT NULL,
    evidence_summary TEXT,
    causal_claim INTEGER NOT NULL DEFAULT 0,
    validation_status TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES scientific_project(project_id)
);

CREATE TABLE IF NOT EXISTS validation_record (
    validation_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    hypothesis_id TEXT,
    model_run_id TEXT,
    validation_type TEXT NOT NULL,
    validation_result TEXT NOT NULL,
    validation_metric TEXT,
    validation_value REAL,
    reviewer TEXT,
    review_date DATE,
    notes TEXT,
    FOREIGN KEY (project_id) REFERENCES scientific_project(project_id),
    FOREIGN KEY (hypothesis_id) REFERENCES scientific_hypothesis(hypothesis_id),
    FOREIGN KEY (model_run_id) REFERENCES ai_model_run(model_run_id)
);

CREATE TABLE IF NOT EXISTS reproducibility_record (
    reproducibility_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    result_reference TEXT NOT NULL,
    data_version TEXT,
    code_version TEXT,
    environment_id TEXT,
    rerun_status TEXT NOT NULL,
    reproduction_metric TEXT,
    reproduction_value REAL,
    tolerance_value REAL,
    passed INTEGER NOT NULL,
    checked_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES scientific_project(project_id),
    FOREIGN KEY (environment_id) REFERENCES computational_environment(environment_id)
);

CREATE VIEW IF NOT EXISTS v_selected_candidates AS
SELECT
    p.prediction_id,
    p.model_run_id,
    c.candidate_id,
    c.candidate_type,
    p.predicted_property,
    p.uncertainty_score,
    p.acquisition_score,
    c.feasibility_score,
    c.safety_score,
    c.cost_score
FROM candidate_prediction p
JOIN scientific_candidate c
    ON p.candidate_id = c.candidate_id
WHERE p.selected_for_experiment = 1;

CREATE VIEW IF NOT EXISTS v_reproducibility_failures AS
SELECT
    r.reproducibility_id,
    sp.project_name,
    r.result_reference,
    r.data_version,
    r.code_version,
    r.rerun_status,
    r.reproduction_metric,
    r.reproduction_value,
    r.tolerance_value,
    r.checked_at
FROM reproducibility_record r
JOIN scientific_project sp
    ON r.project_id = sp.project_id
WHERE r.passed = 0;
