-- Planning, Search, and Sequential Decision Systems
-- SQL schema for planning systems, states, actions, plans, policy evaluations,
-- search traces, human approvals, incidents, rollback, and governance review.

CREATE TABLE IF NOT EXISTS planning_system_registry (
    planning_system_id TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    system_version TEXT NOT NULL,
    system_type TEXT NOT NULL,
    intended_use TEXT NOT NULL,
    owner TEXT NOT NULL,
    deployment_status TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS state_definition (
    state_definition_id TEXT PRIMARY KEY,
    planning_system_id TEXT NOT NULL,
    state_variable_name TEXT NOT NULL,
    state_variable_type TEXT NOT NULL,
    required_for_safety INTEGER DEFAULT 0,
    known_limitation TEXT,
    FOREIGN KEY (planning_system_id) REFERENCES planning_system_registry(planning_system_id)
);

CREATE TABLE IF NOT EXISTS action_registry (
    action_id TEXT PRIMARY KEY,
    planning_system_id TEXT NOT NULL,
    action_name TEXT NOT NULL,
    action_type TEXT NOT NULL,
    risk_level TEXT NOT NULL,
    reversible INTEGER DEFAULT 1,
    requires_human_approval INTEGER DEFAULT 0,
    permission_scope TEXT NOT NULL,
    action_status TEXT NOT NULL,
    FOREIGN KEY (planning_system_id) REFERENCES planning_system_registry(planning_system_id)
);

CREATE TABLE IF NOT EXISTS planning_run (
    planning_run_id TEXT PRIMARY KEY,
    planning_system_id TEXT NOT NULL,
    run_context TEXT NOT NULL,
    planner_type TEXT NOT NULL,
    objective_summary TEXT NOT NULL,
    constraint_summary TEXT,
    run_status TEXT NOT NULL,
    started_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    FOREIGN KEY (planning_system_id) REFERENCES planning_system_registry(planning_system_id)
);

CREATE TABLE IF NOT EXISTS candidate_plan (
    candidate_plan_id TEXT PRIMARY KEY,
    planning_run_id TEXT NOT NULL,
    plan_name TEXT NOT NULL,
    plan_cost REAL,
    expected_value REAL,
    uncertainty_risk REAL,
    constraint_violation_risk REAL,
    irreversibility_risk REAL,
    planning_risk REAL,
    selected_flag INTEGER DEFAULT 0,
    review_required INTEGER DEFAULT 0,
    FOREIGN KEY (planning_run_id) REFERENCES planning_run(planning_run_id)
);

CREATE TABLE IF NOT EXISTS plan_action_step (
    plan_action_step_id TEXT PRIMARY KEY,
    candidate_plan_id TEXT NOT NULL,
    step_index INTEGER NOT NULL,
    action_id TEXT NOT NULL,
    expected_state_change TEXT,
    validation_status TEXT NOT NULL,
    executed_status TEXT DEFAULT 'not_executed',
    executed_at TIMESTAMP,
    FOREIGN KEY (candidate_plan_id) REFERENCES candidate_plan(candidate_plan_id),
    FOREIGN KEY (action_id) REFERENCES action_registry(action_id)
);

CREATE TABLE IF NOT EXISTS search_trace (
    search_trace_id TEXT PRIMARY KEY,
    planning_run_id TEXT NOT NULL,
    node_id TEXT NOT NULL,
    parent_node_id TEXT,
    node_state_summary TEXT NOT NULL,
    path_cost REAL,
    heuristic_cost REAL,
    priority_score REAL,
    expanded_flag INTEGER DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (planning_run_id) REFERENCES planning_run(planning_run_id)
);

CREATE TABLE IF NOT EXISTS policy_evaluation (
    policy_evaluation_id TEXT PRIMARY KEY,
    planning_system_id TEXT NOT NULL,
    policy_name TEXT NOT NULL,
    evaluation_environment TEXT NOT NULL,
    expected_return REAL,
    constraint_violation_rate REAL,
    human_override_rate REAL,
    failure_rate REAL,
    evaluation_status TEXT NOT NULL,
    evaluated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (planning_system_id) REFERENCES planning_system_registry(planning_system_id)
);

CREATE TABLE IF NOT EXISTS human_approval_event (
    human_approval_event_id TEXT PRIMARY KEY,
    candidate_plan_id TEXT,
    plan_action_step_id TEXT,
    approval_reason TEXT NOT NULL,
    approver TEXT NOT NULL,
    approval_decision TEXT NOT NULL,
    approval_notes TEXT,
    approved_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (candidate_plan_id) REFERENCES candidate_plan(candidate_plan_id),
    FOREIGN KEY (plan_action_step_id) REFERENCES plan_action_step(plan_action_step_id)
);

CREATE TABLE IF NOT EXISTS planning_incident (
    planning_incident_id TEXT PRIMARY KEY,
    planning_system_id TEXT NOT NULL,
    planning_run_id TEXT,
    incident_type TEXT NOT NULL,
    severity TEXT NOT NULL,
    incident_status TEXT NOT NULL,
    description TEXT NOT NULL,
    remediation_summary TEXT,
    detected_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP,
    FOREIGN KEY (planning_system_id) REFERENCES planning_system_registry(planning_system_id),
    FOREIGN KEY (planning_run_id) REFERENCES planning_run(planning_run_id)
);

CREATE TABLE IF NOT EXISTS planning_rollback_record (
    rollback_id TEXT PRIMARY KEY,
    planning_system_id TEXT NOT NULL,
    planning_run_id TEXT,
    rollback_reason TEXT NOT NULL,
    rollback_status TEXT NOT NULL,
    executed_by TEXT,
    executed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (planning_system_id) REFERENCES planning_system_registry(planning_system_id),
    FOREIGN KEY (planning_run_id) REFERENCES planning_run(planning_run_id)
);

CREATE TABLE IF NOT EXISTS planning_governance_review (
    governance_review_id TEXT PRIMARY KEY,
    planning_system_id TEXT NOT NULL,
    review_type TEXT NOT NULL,
    reviewer TEXT NOT NULL,
    review_date DATE NOT NULL,
    decision TEXT NOT NULL,
    decision_rationale TEXT NOT NULL,
    required_actions TEXT,
    next_review_date DATE,
    FOREIGN KEY (planning_system_id) REFERENCES planning_system_registry(planning_system_id)
);

CREATE INDEX IF NOT EXISTS idx_action_registry_system_risk
ON action_registry(planning_system_id, risk_level, requires_human_approval);

CREATE INDEX IF NOT EXISTS idx_candidate_plan_run_review
ON candidate_plan(planning_run_id, review_required, selected_flag);

CREATE INDEX IF NOT EXISTS idx_plan_action_step_plan_status
ON plan_action_step(candidate_plan_id, validation_status, executed_status);

CREATE INDEX IF NOT EXISTS idx_policy_evaluation_system_status
ON policy_evaluation(planning_system_id, evaluation_status);

CREATE VIEW IF NOT EXISTS v_plans_requiring_review AS
SELECT
    s.system_name,
    s.system_version,
    r.planning_run_id,
    p.candidate_plan_id,
    p.plan_name,
    p.plan_cost,
    p.uncertainty_risk,
    p.constraint_violation_risk,
    p.irreversibility_risk,
    p.planning_risk
FROM candidate_plan p
JOIN planning_run r
    ON p.planning_run_id = r.planning_run_id
JOIN planning_system_registry s
    ON r.planning_system_id = s.planning_system_id
WHERE p.review_required = 1
   OR p.constraint_violation_risk >= 0.20
   OR p.irreversibility_risk >= 0.15;

CREATE VIEW IF NOT EXISTS v_high_risk_actions AS
SELECT
    s.system_name,
    a.action_id,
    a.action_name,
    a.action_type,
    a.risk_level,
    a.reversible,
    a.requires_human_approval,
    a.permission_scope
FROM action_registry a
JOIN planning_system_registry s
    ON a.planning_system_id = s.planning_system_id
WHERE a.risk_level IN ('high', 'critical')
   OR a.requires_human_approval = 1
   OR a.reversible = 0;
