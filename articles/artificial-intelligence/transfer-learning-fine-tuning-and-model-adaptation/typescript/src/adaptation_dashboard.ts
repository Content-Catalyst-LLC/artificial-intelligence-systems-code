interface AdaptationMetric {
  name: string;
  value: number;
  warningThreshold: number;
  actionThreshold: number;
  unit?: string;
}

type MetricStatus = "normal" | "warning" | "action";

interface EvaluatedAdaptationMetric extends AdaptationMetric {
  status: MetricStatus;
  interpretation: string;
}

interface AdaptationSnapshot {
  systemId: string;
  systemName: string;
  generatedAt: string;
  metrics: AdaptationMetric[];
}

function evaluateMetric(metric: AdaptationMetric): EvaluatedAdaptationMetric {
  let status: MetricStatus = "normal";

  if (metric.value >= metric.actionThreshold) {
    status = "action";
  } else if (metric.value >= metric.warningThreshold) {
    status = "warning";
  }

  const interpretation =
    status === "action"
      ? `${metric.name} exceeds the action threshold and requires adaptation governance review.`
      : status === "warning"
        ? `${metric.name} exceeds the warning threshold and should be monitored.`
        : `${metric.name} is within the expected model adaptation governance range.`;

  return {
    ...metric,
    status,
    interpretation
  };
}

function summarize(snapshot: AdaptationSnapshot): EvaluatedAdaptationMetric[] {
  return snapshot.metrics.map(evaluateMetric);
}

function renderDashboard(snapshot: AdaptationSnapshot, target: HTMLElement): void {
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
    <section class="adaptation-dashboard">
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

const exampleSnapshot: AdaptationSnapshot = {
  systemId: "model-adaptation-001",
  systemName: "Transfer Learning and Fine-Tuning Governance Dashboard",
  generatedAt: new Date().toISOString(),
  metrics: [
    {
      name: "negative_transfer_rate",
      value: 0.06,
      warningThreshold: 0.10,
      actionThreshold: 0.20
    },
    {
      name: "low_retention_rate",
      value: 0.12,
      warningThreshold: 0.15,
      actionThreshold: 0.30
    },
    {
      name: "unapproved_sensitive_adaptations",
      value: 1,
      warningThreshold: 2,
      actionThreshold: 5
    },
    {
      name: "adapter_sprawl_index",
      value: 0.18,
      warningThreshold: 0.25,
      actionThreshold: 0.45
    }
  ]
};

const target = document.getElementById("app");

if (target) {
  renderDashboard(exampleSnapshot, target);
}

export {
  AdaptationMetric,
  EvaluatedAdaptationMetric,
  AdaptationSnapshot,
  evaluateMetric,
  summarize,
  renderDashboard
};
