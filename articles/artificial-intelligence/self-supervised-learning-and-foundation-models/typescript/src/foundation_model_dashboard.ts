interface FoundationMetric {
  name: string;
  value: number;
  warningThreshold: number;
  actionThreshold: number;
  unit?: string;
}

type MetricStatus = "normal" | "warning" | "action";

interface EvaluatedFoundationMetric extends FoundationMetric {
  status: MetricStatus;
  interpretation: string;
}

interface FoundationSnapshot {
  systemId: string;
  systemName: string;
  generatedAt: string;
  metrics: FoundationMetric[];
}

function evaluateMetric(metric: FoundationMetric): EvaluatedFoundationMetric {
  let status: MetricStatus = "normal";

  if (metric.value >= metric.actionThreshold) {
    status = "action";
  } else if (metric.value >= metric.warningThreshold) {
    status = "warning";
  }

  const interpretation =
    status === "action"
      ? `${metric.name} exceeds the action threshold and requires foundation-model governance review.`
      : status === "warning"
        ? `${metric.name} exceeds the warning threshold and should be monitored.`
        : `${metric.name} is within the expected foundation-model governance range.`;

  return {
    ...metric,
    status,
    interpretation
  };
}

function summarize(snapshot: FoundationSnapshot): EvaluatedFoundationMetric[] {
  return snapshot.metrics.map(evaluateMetric);
}

function renderDashboard(snapshot: FoundationSnapshot, target: HTMLElement): void {
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
    <section class="foundation-model-dashboard">
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

const exampleSnapshot: FoundationSnapshot = {
  systemId: "foundation-model-001",
  systemName: "Self-Supervised Learning and Foundation Model Governance Dashboard",
  generatedAt: new Date().toISOString(),
  metrics: [
    {
      name: "weak_provenance_run_share",
      value: 0.14,
      warningThreshold: 0.20,
      actionThreshold: 0.35
    },
    {
      name: "high_privacy_risk_run_share",
      value: 0.08,
      warningThreshold: 0.15,
      actionThreshold: 0.30
    },
    {
      name: "open_bias_review_count",
      value: 1,
      warningThreshold: 2,
      actionThreshold: 5
    },
    {
      name: "broad_reuse_low_governance_count",
      value: 2,
      warningThreshold: 3,
      actionThreshold: 8
    }
  ]
};

const target = document.getElementById("app");

if (target) {
  renderDashboard(exampleSnapshot, target);
}

export {
  FoundationMetric,
  EvaluatedFoundationMetric,
  FoundationSnapshot,
  evaluateMetric,
  summarize,
  renderDashboard
};
