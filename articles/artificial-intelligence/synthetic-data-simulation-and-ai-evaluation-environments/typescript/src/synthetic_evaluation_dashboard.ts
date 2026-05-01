interface SyntheticEvaluationMetric {
  name: string;
  value: number;
  warningThreshold: number;
  actionThreshold: number;
  unit?: string;
}

type MetricStatus = "normal" | "warning" | "action";

interface EvaluatedSyntheticMetric extends SyntheticEvaluationMetric {
  status: MetricStatus;
  interpretation: string;
}

interface SyntheticEvaluationSnapshot {
  systemId: string;
  systemName: string;
  generatedAt: string;
  metrics: SyntheticEvaluationMetric[];
}

function evaluateMetric(metric: SyntheticEvaluationMetric): EvaluatedSyntheticMetric {
  let status: MetricStatus = "normal";

  if (metric.value >= metric.actionThreshold) {
    status = "action";
  } else if (metric.value >= metric.warningThreshold) {
    status = "warning";
  }

  const interpretation =
    status === "action"
      ? `${metric.name} exceeds the action threshold and requires synthetic-evaluation governance review.`
      : status === "warning"
        ? `${metric.name} exceeds the warning threshold and should be investigated.`
        : `${metric.name} is within the expected synthetic-evaluation range.`;

  return {
    ...metric,
    status,
    interpretation
  };
}

function summarize(snapshot: SyntheticEvaluationSnapshot): EvaluatedSyntheticMetric[] {
  return snapshot.metrics.map(evaluateMetric);
}

function renderDashboard(snapshot: SyntheticEvaluationSnapshot, target: HTMLElement): void {
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
    <section class="synthetic-evaluation-dashboard">
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

const exampleSnapshot: SyntheticEvaluationSnapshot = {
  systemId: "synthetic-evaluation-system-001",
  systemName: "Synthetic Data and Simulation Evaluation Dashboard",
  generatedAt: new Date().toISOString(),
  metrics: [
    {
      name: "fidelity_risk",
      value: 0.14,
      warningThreshold: 0.20,
      actionThreshold: 0.30
    },
    {
      name: "utility_gap",
      value: 0.03,
      warningThreshold: 0.05,
      actionThreshold: 0.10
    },
    {
      name: "privacy_proximity_risk",
      value: 0.02,
      warningThreshold: 0.05,
      actionThreshold: 0.10
    },
    {
      name: "rare_case_coverage_gap",
      value: 0.04,
      warningThreshold: 0.06,
      actionThreshold: 0.12
    },
    {
      name: "sim_to_real_gap",
      value: 0.11,
      warningThreshold: 0.18,
      actionThreshold: 0.30
    }
  ]
};

const target = document.getElementById("app");

if (target) {
  renderDashboard(exampleSnapshot, target);
}

export {
  SyntheticEvaluationMetric,
  EvaluatedSyntheticMetric,
  SyntheticEvaluationSnapshot,
  evaluateMetric,
  summarize,
  renderDashboard
};
