interface DecisionMetric {
  name: string;
  value: number;
  warningThreshold: number;
  actionThreshold: number;
  unit?: string;
}

type MetricStatus = "normal" | "warning" | "action";

interface EvaluatedDecisionMetric extends DecisionMetric {
  status: MetricStatus;
  interpretation: string;
}

interface DecisionSnapshot {
  systemId: string;
  systemName: string;
  generatedAt: string;
  metrics: DecisionMetric[];
}

function evaluateMetric(metric: DecisionMetric): EvaluatedDecisionMetric {
  let status: MetricStatus = "normal";

  if (metric.value >= metric.actionThreshold) {
    status = "action";
  } else if (metric.value >= metric.warningThreshold) {
    status = "warning";
  }

  const interpretation =
    status === "action"
      ? `${metric.name} exceeds the action threshold and requires governance review.`
      : status === "warning"
        ? `${metric.name} exceeds the warning threshold and should be monitored.`
        : `${metric.name} is within the expected decision-support range.`;

  return {
    ...metric,
    status,
    interpretation
  };
}

function summarize(snapshot: DecisionSnapshot): EvaluatedDecisionMetric[] {
  return snapshot.metrics.map(evaluateMetric);
}

function renderDashboard(snapshot: DecisionSnapshot, target: HTMLElement): void {
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
    <section class="decision-support-dashboard">
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

const exampleSnapshot: DecisionSnapshot = {
  systemId: "decision-support-001",
  systemName: "AI Decision Support Governance Dashboard",
  generatedAt: new Date().toISOString(),
  metrics: [
    {
      name: "high_uncertainty_decision_share",
      value: 0.18,
      warningThreshold: 0.25,
      actionThreshold: 0.40
    },
    {
      name: "human_override_rate",
      value: 0.07,
      warningThreshold: 0.15,
      actionThreshold: 0.30
    },
    {
      name: "unreviewed_high_risk_count",
      value: 1,
      warningThreshold: 2,
      actionThreshold: 5
    },
    {
      name: "open_governance_actions",
      value: 3,
      warningThreshold: 5,
      actionThreshold: 10
    }
  ]
};

const target = document.getElementById("app");

if (target) {
  renderDashboard(exampleSnapshot, target);
}

export {
  DecisionMetric,
  EvaluatedDecisionMetric,
  DecisionSnapshot,
  evaluateMetric,
  summarize,
  renderDashboard
};
