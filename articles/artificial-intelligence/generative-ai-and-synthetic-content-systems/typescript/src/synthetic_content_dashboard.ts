interface SyntheticContentMetric {
  name: string;
  value: number;
  warningThreshold: number;
  actionThreshold: number;
  unit?: string;
}

type MetricStatus = "normal" | "warning" | "action";

interface EvaluatedSyntheticContentMetric extends SyntheticContentMetric {
  status: MetricStatus;
  interpretation: string;
}

interface SyntheticContentSnapshot {
  systemId: string;
  systemName: string;
  generatedAt: string;
  metrics: SyntheticContentMetric[];
}

function evaluateMetric(metric: SyntheticContentMetric): EvaluatedSyntheticContentMetric {
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
        : `${metric.name} is within the expected synthetic-content governance range.`;

  return {
    ...metric,
    status,
    interpretation
  };
}

function summarize(snapshot: SyntheticContentSnapshot): EvaluatedSyntheticContentMetric[] {
  return snapshot.metrics.map(evaluateMetric);
}

function renderDashboard(snapshot: SyntheticContentSnapshot, target: HTMLElement): void {
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
    <section class="synthetic-content-dashboard">
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

const exampleSnapshot: SyntheticContentSnapshot = {
  systemId: "synthetic-content-001",
  systemName: "Generative AI Synthetic Content Governance Dashboard",
  generatedAt: new Date().toISOString(),
  metrics: [
    {
      name: "high_risk_artifact_share",
      value: 0.14,
      warningThreshold: 0.20,
      actionThreshold: 0.35
    },
    {
      name: "missing_provenance_share",
      value: 0.22,
      warningThreshold: 0.25,
      actionThreshold: 0.40
    },
    {
      name: "unreviewed_sensitive_artifacts",
      value: 2,
      warningThreshold: 3,
      actionThreshold: 8
    },
    {
      name: "open_synthetic_content_incidents",
      value: 1,
      warningThreshold: 2,
      actionThreshold: 5
    }
  ]
};

const target = document.getElementById("app");

if (target) {
  renderDashboard(exampleSnapshot, target);
}

export {
  SyntheticContentMetric,
  EvaluatedSyntheticContentMetric,
  SyntheticContentSnapshot,
  evaluateMetric,
  summarize,
  renderDashboard
};
