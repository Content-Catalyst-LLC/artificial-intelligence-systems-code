-- Reinforcement Learning in Dynamic Environments Metadata Schema

CREATE TABLE IF NOT EXISTS rl_experiments (
    experiment_id TEXT PRIMARY KEY,
    experiment_name TEXT NOT NULL,
    environment_name TEXT NOT NULL,
    algorithm_name TEXT NOT NULL,
    experiment_owner TEXT NOT NULL,
    deployment_context TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS rl_environment_specs (
    environment_id TEXT PRIMARY KEY,
    experiment_id TEXT NOT NULL,
    state_space_description TEXT NOT NULL,
    action_space_description TEXT NOT NULL,
    reward_function_description TEXT NOT NULL,
    transition_dynamic_description TEXT,
    partial_observability BOOLEAN DEFAULT FALSE,
    non_stationary BOOLEAN DEFAULT FALSE,
    safety_constraints TEXT,
    FOREIGN KEY(experiment_id) REFERENCES rl_experiments(experiment_id)
);

CREATE TABLE IF NOT EXISTS rl_episodes (
    episode_id TEXT PRIMARY KEY,
    experiment_id TEXT NOT NULL,
    episode_number INTEGER NOT NULL,
    phase TEXT,
    total_reward REAL,
    steps INTEGER,
    reached_goal BOOLEAN,
    constraint_violations INTEGER,
    hazard_visits INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(experiment_id) REFERENCES rl_experiments(experiment_id)
);

CREATE TABLE IF NOT EXISTS rl_transitions (
    transition_id TEXT PRIMARY KEY,
    episode_id TEXT NOT NULL,
    step_number INTEGER NOT NULL,
    state_id TEXT NOT NULL,
    action_id TEXT NOT NULL,
    reward REAL NOT NULL,
    next_state_id TEXT NOT NULL,
    done BOOLEAN DEFAULT FALSE,
    constraint_violation BOOLEAN DEFAULT FALSE,
    FOREIGN KEY(episode_id) REFERENCES rl_episodes(episode_id)
);

CREATE TABLE IF NOT EXISTS rl_policy_snapshots (
    policy_snapshot_id TEXT PRIMARY KEY,
    experiment_id TEXT NOT NULL,
    snapshot_episode INTEGER NOT NULL,
    state_id TEXT NOT NULL,
    best_action_id TEXT,
    estimated_value REAL,
    exploration_rate REAL,
    policy_notes TEXT,
    FOREIGN KEY(experiment_id) REFERENCES rl_experiments(experiment_id)
);

CREATE TABLE IF NOT EXISTS rl_safety_reviews (
    review_id TEXT PRIMARY KEY,
    experiment_id TEXT NOT NULL,
    review_date DATE NOT NULL,
    reviewer TEXT NOT NULL,
    reward_function_reviewed BOOLEAN DEFAULT FALSE,
    exploration_safety_reviewed BOOLEAN DEFAULT FALSE,
    constraint_handling_reviewed BOOLEAN DEFAULT FALSE,
    fallback_reviewed BOOLEAN DEFAULT FALSE,
    monitoring_reviewed BOOLEAN DEFAULT FALSE,
    findings TEXT,
    required_actions TEXT,
    status TEXT CHECK(status IN ('draft', 'approved', 'requires_action', 'closed')),
    FOREIGN KEY(experiment_id) REFERENCES rl_experiments(experiment_id)
);
