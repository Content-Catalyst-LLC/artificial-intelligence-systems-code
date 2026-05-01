interface ObservabilityMetric {
  name: string;
  value: number;
  warningThreshold: number;
  actionThreshold: number;
  unit?: string;
}

type MetricStatus = "normal" | "warning" | "action";

interface EvaluatedObservabilityMetric extends ObservabilityMetric {
  status: MetricStatus;
  interpretation: string;
}

interface ObservabilitySnapshot {
  systemId: string;
  systemName: string;
  generatedAt: string;
  metrics: ObservabilityMetric[];
}

function evaluateMetric(metric: ObservabilityMetric): EvaluatedObservabilityMetric {
  let status: MetricStatus = "normal";

  if (metric.value >= metric.actionThreshold) {
    status = "action";
  } else if (metric.value >= metric.warningThreshold) {
    status = "warning";
  }

  const interpretation =
    status === "action"
      ? `${metric.name} exceeds the action threshold and requires observability governance review.`
      : status === "warning"
        ? `${metric.name} exceeds the warning threshold and should be investigated.`
        : `${metric.name} is within the expected monitoring range.`;

  return {
    ...metric,
    status,
    interpretation
  };
}

function summarize(snapshot: ObservabilitySnapshot): EvaluatedObservabilityMetric[] {
  return snapshot.metrics.map(evaluateMetric);
}

function renderDashboard(snapshot: ObservabilitySnapshot, target: HTMLElement): void {
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
    <section class="observability-dashboard">
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

const exampleSnapshot: ObservabilitySnapshot = {
  systemId: "ai-observability-system-001",
  systemName: "Model Monitoring and AI Observability Dashboard",
  generatedAt: new Date().toISOString(),
  metrics: [
    {
      name: "max_feature_psi",
      value: 0.21,
      warningThreshold: 0.20,
      actionThreshold: 0.35
    },
    {
      name: "prediction_psi",
      value: 0.18,
      warningThreshold: 0.20,
      actionThreshold: 0.35
    },
    {
      name: "performance_degradation",
      value: 0.07,
      warningThreshold: 0.08,
      actionThreshold: 0.15
    },
    {
      name: "missing_rate",
      value: 0.035,
      warningThreshold: 0.05,
      actionThreshold: 0.10
    },
    {
      name: "mean_latency_ms",
      value: 680.0,
      warningThreshold: 900.0,
      actionThreshold: 1200.0,
      unit: "ms"
    }
  ]
};

const target = document.getElementById("app");

if (target) {
  renderDashboard(exampleSnapshot, target);
}

export {
  ObservabilityMetric,
  EvaluatedObservabilityMetric,
  ObservabilitySnapshot,
  evaluateMetric,
  summarize,
  renderDashboard
};
