interface AgentMetric {
  name: string;
  value: number;
  warningThreshold: number;
  actionThreshold: number;
  unit?: string;
}

type MetricStatus = "normal" | "warning" | "action";

interface EvaluatedAgentMetric extends AgentMetric {
  status: MetricStatus;
  interpretation: string;
}

interface AgentSnapshot {
  systemId: string;
  systemName: string;
  generatedAt: string;
  metrics: AgentMetric[];
}

function evaluateMetric(metric: AgentMetric): EvaluatedAgentMetric {
  let status: MetricStatus = "normal";

  if (metric.value >= metric.actionThreshold) {
    status = "action";
  } else if (metric.value >= metric.warningThreshold) {
    status = "warning";
  }

  const interpretation =
    status === "action"
      ? `${metric.name} exceeds the action threshold and requires agent governance review.`
      : status === "warning"
        ? `${metric.name} exceeds the warning threshold and should be monitored.`
        : `${metric.name} is within the expected agent governance range.`;

  return {
    ...metric,
    status,
    interpretation
  };
}

function summarize(snapshot: AgentSnapshot): EvaluatedAgentMetric[] {
  return snapshot.metrics.map(evaluateMetric);
}

function renderDashboard(snapshot: AgentSnapshot, target: HTMLElement): void {
  const evaluated = summarize(snapshot);
  const actionCount = evaluated.filter((metric) => metric.status === "action").length;
  const warningCount = evaluated.filter((metric) => metric.status === "warning").length;

  const rows = evaluated
    .map((metric) => {
      const unit = metric.unit ? ` ${metric.unit}` : "";

      return `
        <tr>
          <td>${metric.name}</td>
          <td>${metric.value.toFixed(4)}${unit}</td>
          <td>${metric.warningThreshold.toFixed(4)}</td>
          <td>${metric.actionThreshold.toFixed(4)}</td>
          <td>${metric.status}</td>
          <td>${metric.interpretation}</td>
        </tr>
      `;
    })
    .join("");

  target.innerHTML = `
    <section class="agent-dashboard">
      <h1>${snapshot.systemName}</h1>
      <p><strong>Generated:</strong> ${snapshot.generatedAt}</p>
      <p><strong>Warnings:</strong> ${warningCount} | <strong>Actions:</strong> ${actionCount}</p>

      <table>
        <thead>
          <tr>
            <th>Metric</th>
            <th>Value</th>
            <th>Warning</th>
            <th>Action</th>
            <th>Status</th>
            <th>Interpretation</th>
          </tr>
        </thead>
        <tbody>
          ${rows}
        </tbody>
      </table>
    </section>
  `;
}

const exampleSnapshot: AgentSnapshot = {
  systemId: "agent-workflow-system-001",
  systemName: "AI Agent Workflow Governance Dashboard",
  generatedAt: new Date().toISOString(),
  metrics: [
    {
      name: "tool_call_failure_rate",
      value: 0.07,
      warningThreshold: 0.10,
      actionThreshold: 0.20
    },
    {
      name: "denied_action_attempt_rate",
      value: 0.04,
      warningThreshold: 0.08,
      actionThreshold: 0.15
    },
    {
      name: "failed_confirmation_rate",
      value: 0.03,
      warningThreshold: 0.06,
      actionThreshold: 0.12
    },
    {
      name: "prompt_injection_exposure_rate",
      value: 0.05,
      warningThreshold: 0.10,
      actionThreshold: 0.20
    },
    {
      name: "high_risk_tool_use_rate",
      value: 0.09,
      warningThreshold: 0.15,
      actionThreshold: 0.25
    }
  ]
};

const target = document.getElementById("app");

if (target) {
  renderDashboard(exampleSnapshot, target);
}

export {
  AgentMetric,
  EvaluatedAgentMetric,
  AgentSnapshot,
  evaluateMetric,
  summarize,
  renderDashboard
};
