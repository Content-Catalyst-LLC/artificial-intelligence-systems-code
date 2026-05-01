-- AI Agents, Tool Use, and Workflow Automation
-- SQL schema for agent registries, tool catalogs, workflow runs,
-- tool-call logs, permission checks, human approvals, sandbox events,
-- incidents, and governance reviews.

CREATE TABLE IF NOT EXISTS agent_system (
    agent_system_id TEXT PRIMARY KEY,
    agent_name TEXT NOT NULL,
    agent_version TEXT NOT NULL,
    intended_use TEXT NOT NULL,
    prohibited_use TEXT,
    owner TEXT NOT NULL,
    deployment_status TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS tool_catalog (
    tool_id TEXT PRIMARY KEY,
    tool_name TEXT NOT NULL,
    tool_type TEXT NOT NULL,
    risk_level TEXT NOT NULL,
    read_only INTEGER DEFAULT 1,
    requires_confirmation INTEGER DEFAULT 0,
    requires_human_approval INTEGER DEFAULT 0,
    rollback_available INTEGER DEFAULT 0,
    owner TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS agent_tool_permission (
    permission_id TEXT PRIMARY KEY,
    agent_system_id TEXT NOT NULL,
    tool_id TEXT NOT NULL,
    permission_scope TEXT NOT NULL,
    allowed_actions TEXT NOT NULL,
    approval_status TEXT NOT NULL,
    approved_by TEXT,
    approved_at TIMESTAMP,
    FOREIGN KEY (agent_system_id) REFERENCES agent_system(agent_system_id),
    FOREIGN KEY (tool_id) REFERENCES tool_catalog(tool_id)
);

CREATE TABLE IF NOT EXISTS workflow_run (
    workflow_run_id TEXT PRIMARY KEY,
    agent_system_id TEXT NOT NULL,
    workflow_type TEXT NOT NULL,
    user_or_process TEXT,
    task_hash TEXT NOT NULL,
    workflow_status TEXT NOT NULL,
    step_count INTEGER DEFAULT 0,
    started_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    FOREIGN KEY (agent_system_id) REFERENCES agent_system(agent_system_id)
);

CREATE TABLE IF NOT EXISTS agent_state_snapshot (
    state_snapshot_id TEXT PRIMARY KEY,
    workflow_run_id TEXT NOT NULL,
    step_index INTEGER NOT NULL,
    state_hash TEXT NOT NULL,
    state_summary TEXT,
    memory_scope TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (workflow_run_id) REFERENCES workflow_run(workflow_run_id)
);

CREATE TABLE IF NOT EXISTS tool_call_log (
    tool_call_id TEXT PRIMARY KEY,
    workflow_run_id TEXT NOT NULL,
    tool_id TEXT NOT NULL,
    step_index INTEGER NOT NULL,
    argument_hash TEXT NOT NULL,
    argument_validation_status TEXT NOT NULL,
    execution_status TEXT NOT NULL,
    output_hash TEXT,
    latency_ms INTEGER,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (workflow_run_id) REFERENCES workflow_run(workflow_run_id),
    FOREIGN KEY (tool_id) REFERENCES tool_catalog(tool_id)
);

CREATE TABLE IF NOT EXISTS permission_check_log (
    permission_check_id TEXT PRIMARY KEY,
    workflow_run_id TEXT NOT NULL,
    tool_call_id TEXT,
    user_or_process TEXT,
    resource_id TEXT,
    action_name TEXT NOT NULL,
    access_decision TEXT NOT NULL,
    decision_reason TEXT,
    checked_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (workflow_run_id) REFERENCES workflow_run(workflow_run_id),
    FOREIGN KEY (tool_call_id) REFERENCES tool_call_log(tool_call_id)
);

CREATE TABLE IF NOT EXISTS human_approval_log (
    approval_id TEXT PRIMARY KEY,
    workflow_run_id TEXT NOT NULL,
    tool_call_id TEXT,
    approval_type TEXT NOT NULL,
    approver TEXT,
    approval_decision TEXT NOT NULL,
    approval_reason TEXT,
    approved_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (workflow_run_id) REFERENCES workflow_run(workflow_run_id),
    FOREIGN KEY (tool_call_id) REFERENCES tool_call_log(tool_call_id)
);

CREATE TABLE IF NOT EXISTS sandbox_execution_event (
    sandbox_event_id TEXT PRIMARY KEY,
    workflow_run_id TEXT NOT NULL,
    tool_call_id TEXT,
    sandbox_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    network_access INTEGER DEFAULT 0,
    file_write_access INTEGER DEFAULT 0,
    secrets_accessed INTEGER DEFAULT 0,
    exit_code INTEGER,
    event_status TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (workflow_run_id) REFERENCES workflow_run(workflow_run_id),
    FOREIGN KEY (tool_call_id) REFERENCES tool_call_log(tool_call_id)
);

CREATE TABLE IF NOT EXISTS agent_evaluation_result (
    evaluation_result_id TEXT PRIMARY KEY,
    agent_system_id TEXT NOT NULL,
    workflow_type TEXT NOT NULL,
    evaluation_name TEXT NOT NULL,
    metric_name TEXT NOT NULL,
    metric_value REAL NOT NULL,
    reviewer TEXT,
    evaluated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (agent_system_id) REFERENCES agent_system(agent_system_id)
);

CREATE TABLE IF NOT EXISTS agent_incident_record (
    incident_id TEXT PRIMARY KEY,
    agent_system_id TEXT NOT NULL,
    workflow_run_id TEXT,
    incident_type TEXT NOT NULL,
    severity TEXT NOT NULL,
    incident_status TEXT NOT NULL,
    description TEXT NOT NULL,
    remediation_summary TEXT,
    detected_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP,
    FOREIGN KEY (agent_system_id) REFERENCES agent_system(agent_system_id),
    FOREIGN KEY (workflow_run_id) REFERENCES workflow_run(workflow_run_id)
);

CREATE TABLE IF NOT EXISTS agent_governance_review (
    governance_review_id TEXT PRIMARY KEY,
    agent_system_id TEXT NOT NULL,
    review_type TEXT NOT NULL,
    reviewer TEXT NOT NULL,
    review_date DATE NOT NULL,
    decision TEXT NOT NULL,
    decision_rationale TEXT NOT NULL,
    required_actions TEXT,
    next_review_date DATE,
    FOREIGN KEY (agent_system_id) REFERENCES agent_system(agent_system_id)
);

CREATE TABLE IF NOT EXISTS agent_monitoring_signal (
    monitoring_signal_id TEXT PRIMARY KEY,
    agent_system_id TEXT NOT NULL,
    signal_name TEXT NOT NULL,
    signal_value REAL NOT NULL,
    threshold_warning REAL,
    threshold_action REAL,
    signal_status TEXT NOT NULL,
    measured_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (agent_system_id) REFERENCES agent_system(agent_system_id)
);

CREATE INDEX IF NOT EXISTS idx_agent_tool_permission_system
ON agent_tool_permission(agent_system_id, tool_id, approval_status);

CREATE INDEX IF NOT EXISTS idx_workflow_run_agent_time
ON workflow_run(agent_system_id, started_at, workflow_status);

CREATE INDEX IF NOT EXISTS idx_tool_call_workflow_step
ON tool_call_log(workflow_run_id, step_index, execution_status);

CREATE INDEX IF NOT EXISTS idx_permission_check_workflow
ON permission_check_log(workflow_run_id, access_decision);

CREATE INDEX IF NOT EXISTS idx_agent_eval_system_metric
ON agent_evaluation_result(agent_system_id, metric_name, workflow_type);

CREATE VIEW IF NOT EXISTS v_agent_high_risk_tool_calls AS
SELECT
    wr.workflow_run_id,
    ag.agent_name,
    tc.tool_call_id,
    tc.step_index,
    t.tool_name,
    t.risk_level,
    tc.argument_validation_status,
    tc.execution_status
FROM tool_call_log tc
JOIN workflow_run wr
    ON tc.workflow_run_id = wr.workflow_run_id
JOIN agent_system ag
    ON wr.agent_system_id = ag.agent_system_id
JOIN tool_catalog t
    ON tc.tool_id = t.tool_id
WHERE t.risk_level IN ('external_action', 'sensitive')
   OR tc.argument_validation_status != 'passed'
   OR tc.execution_status != 'success';

CREATE VIEW IF NOT EXISTS v_agent_permission_or_approval_failures AS
SELECT
    wr.workflow_run_id,
    ag.agent_name,
    pc.action_name,
    pc.access_decision,
    pc.decision_reason,
    ha.approval_decision
FROM workflow_run wr
JOIN agent_system ag
    ON wr.agent_system_id = ag.agent_system_id
LEFT JOIN permission_check_log pc
    ON wr.workflow_run_id = pc.workflow_run_id
LEFT JOIN human_approval_log ha
    ON wr.workflow_run_id = ha.workflow_run_id
WHERE pc.access_decision IN ('denied', 'requires_review')
   OR ha.approval_decision IN ('rejected', 'requires_changes');
