-- Learning Paradigms Metadata Schema
-- Supports the article "Supervised, Unsupervised, and Reinforcement Learning"

CREATE TABLE IF NOT EXISTS learning_systems (
    system_id TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    system_purpose TEXT NOT NULL,
    learning_paradigm TEXT CHECK(learning_paradigm IN ('supervised', 'unsupervised', 'reinforcement', 'self_supervised', 'semi_supervised', 'hybrid')),
    owner_team TEXT NOT NULL,
    risk_tier TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS learning_signals (
    signal_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    signal_type TEXT NOT NULL,
    label_source TEXT,
    feedback_timing TEXT,
    reward_source TEXT,
    known_limitations TEXT,
    FOREIGN KEY(system_id) REFERENCES learning_systems(system_id)
);

CREATE TABLE IF NOT EXISTS datasets (
    dataset_id TEXT PRIMARY KEY,
    dataset_name TEXT NOT NULL,
    data_source TEXT NOT NULL,
    has_labels BOOLEAN DEFAULT FALSE,
    has_rewards BOOLEAN DEFAULT FALSE,
    contains_sensitive_data BOOLEAN DEFAULT FALSE,
    data_version TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS training_runs (
    training_run_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    dataset_id TEXT NOT NULL,
    objective_name TEXT NOT NULL,
    model_family TEXT NOT NULL,
    optimizer TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(system_id) REFERENCES learning_systems(system_id),
    FOREIGN KEY(dataset_id) REFERENCES datasets(dataset_id)
);

CREATE TABLE IF NOT EXISTS evaluation_runs (
    evaluation_id TEXT PRIMARY KEY,
    training_run_id TEXT NOT NULL,
    evaluation_date DATE NOT NULL,
    evaluation_method TEXT NOT NULL,
    metric_name TEXT,
    metric_value REAL,
    generalization_notes TEXT,
    governance_notes TEXT,
    FOREIGN KEY(training_run_id) REFERENCES training_runs(training_run_id)
);

CREATE TABLE IF NOT EXISTS rl_policy_evaluations (
    policy_eval_id TEXT PRIMARY KEY,
    evaluation_id TEXT NOT NULL,
    environment_name TEXT NOT NULL,
    average_return REAL,
    episode_count INTEGER,
    exploration_policy TEXT,
    safety_notes TEXT,
    FOREIGN KEY(evaluation_id) REFERENCES evaluation_runs(evaluation_id)
);
