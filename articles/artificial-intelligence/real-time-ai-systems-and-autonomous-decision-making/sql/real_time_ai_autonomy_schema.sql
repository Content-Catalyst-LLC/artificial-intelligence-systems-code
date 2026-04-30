-- Real-Time AI Systems and Autonomous Decision-Making Metadata Schema

CREATE TABLE IF NOT EXISTS real_time_ai_systems (
    system_id TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    system_purpose TEXT NOT NULL,
    owner_team TEXT NOT NULL,
    deployment_context TEXT,
    autonomy_level TEXT CHECK(autonomy_level IN ('advisory', 'human_in_loop', 'human_on_loop', 'supervised_autonomy', 'full_autonomy', 'unknown')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS real_time_tasks (
    task_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    task_name TEXT NOT NULL,
    task_type TEXT CHECK(task_type IN ('sensing', 'preprocessing', 'inference', 'tracking', 'planning', 'control', 'safety_monitor', 'communication', 'logging', 'other')),
    execution_time_ms REAL,
    period_ms REAL,
    deadline_ms REAL,
    criticality TEXT CHECK(criticality IN ('low', 'medium', 'high', 'critical')),
    FOREIGN KEY(system_id) REFERENCES real_time_ai_systems(system_id)
);

CREATE TABLE IF NOT EXISTS latency_observations (
    observation_id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    observation_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    latency_ms REAL NOT NULL,
    deadline_ms REAL NOT NULL,
    deadline_miss BOOLEAN DEFAULT FALSE,
    jitter_ms REAL,
    load_condition TEXT,
    FOREIGN KEY(task_id) REFERENCES real_time_tasks(task_id)
);

CREATE TABLE IF NOT EXISTS autonomy_actions (
    action_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    action_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    observation_reference TEXT,
    selected_action TEXT NOT NULL,
    ai_action_allowed BOOLEAN DEFAULT TRUE,
    fallback_action_used BOOLEAN DEFAULT FALSE,
    risk_score REAL,
    safety_threshold REAL,
    outcome_notes TEXT,
    FOREIGN KEY(system_id) REFERENCES real_time_ai_systems(system_id)
);

CREATE TABLE IF NOT EXISTS runtime_assurance_events (
    event_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    event_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    event_type TEXT CHECK(event_type IN ('deadline_miss', 'risk_threshold_exceeded', 'fallback_triggered', 'sensor_fault', 'model_fault', 'communication_delay', 'operator_override', 'incident')),
    severity TEXT CHECK(severity IN ('low', 'medium', 'high', 'critical')),
    containment_action TEXT,
    resolved BOOLEAN DEFAULT FALSE,
    notes TEXT,
    FOREIGN KEY(system_id) REFERENCES real_time_ai_systems(system_id)
);

CREATE TABLE IF NOT EXISTS governance_reviews (
    review_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    review_date DATE NOT NULL,
    reviewer TEXT NOT NULL,
    timing_reviewed BOOLEAN DEFAULT FALSE,
    schedulability_reviewed BOOLEAN DEFAULT FALSE,
    safety_reviewed BOOLEAN DEFAULT FALSE,
    fallback_reviewed BOOLEAN DEFAULT FALSE,
    runtime_monitoring_reviewed BOOLEAN DEFAULT FALSE,
    findings TEXT,
    required_actions TEXT,
    status TEXT CHECK(status IN ('draft', 'approved', 'requires_action', 'closed')),
    FOREIGN KEY(system_id) REFERENCES real_time_ai_systems(system_id)
);
