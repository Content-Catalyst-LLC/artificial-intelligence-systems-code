interface PlanningMetric {
  name: string;
  value: number;
  warningThreshold: number;
  actionThreshold: number;
  unit?: string;
}

type MetricStatus = "normal" | "warning" | "action";

interface EvaluatedPlanningMetric extends PlanningMetric {
  status: MetricStatus;
  interpretation: string;
}

interface PlanningSnapshot {
  systemId: string;
  systemName: string;
  generatedAt: string;
  metrics: PlanningMetric[];
}

function evaluateMetric(metric: PlanningMetric): EvaluatedPlanningMetric {
  let status: MetricStatus = "normal";

  if (metric.value >= metric.actionThreshold) {
    status = "action";
  } else if (metric.value >= metric.warningThreshold) {
    status = "warning";
  }

  const interpretation =
    status === "action"
      ? `${metric.name} exceeds the action threshold and requires planning governance review.`
      : status === "warning"
        ? `${metric.name} exceeds the warning threshold and should be investigated.`
        : `${metric.name} is within the expected planning governance range.`;

  return {
    ...metric,
    status,
    interpretation
  };
}

function summarize(snapshot: PlanningSnapshot): EvaluatedPlanningMetric[] {
  return snapshot.metrics.map(evaluateMetric);
}

function renderDashboard(snapshot: PlanningSnapshot, target: HTMLElement): void {
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
    <section class="planning-dashboard">
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

const exampleSnapshot: PlanningSnapshot = {
  systemId: "planning-sequential-decision-system-001",
  systemName: "Planning and Sequential Decision Governance Dashboard",
  generatedAt: new Date().toISOString(),
  metrics: [
    {
      name: "planning_risk",
      value: 0.21,
      warningThreshold: 0.25,
      actionThreshold: 0.35
    },
    {
      name: "constraint_violation_risk",
      value: 0.09,
      warningThreshold: 0.15,
      actionThreshold: 0.25
    },
    {
      name: "irreversibility_risk",
      value: 0.04,
      warningThreshold: 0.10,
      actionThreshold: 0.20
    },
    {
      name: "human_override_rate",
      value: 0.07,
      warningThreshold: 0.12,
      actionThreshold: 0.20
    },
    {
      name: "traceability_gap",
      value: 0.05,
      warningThreshold: 0.10,
      actionThreshold: 0.18
    }
  ]
};

const target = document.getElementById("app");

if (target) {
  renderDashboard(exampleSnapshot, target);
}

export {
  PlanningMetric,
  EvaluatedPlanningMetric,
  PlanningSnapshot,
  evaluateMetric,
  summarize,
  renderDashboard
};
