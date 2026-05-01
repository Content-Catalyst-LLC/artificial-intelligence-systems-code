interface InfrastructureMetric {
  name: string;
  value: number;
  warningThreshold: number;
  actionThreshold: number;
  unit?: string;
}

type MetricStatus = "normal" | "warning" | "action";

interface EvaluatedInfrastructureMetric extends InfrastructureMetric {
  status: MetricStatus;
  interpretation: string;
}

interface InfrastructureSnapshot {
  systemId: string;
  systemName: string;
  generatedAt: string;
  metrics: InfrastructureMetric[];
}

function evaluateMetric(metric: InfrastructureMetric): EvaluatedInfrastructureMetric {
  let status: MetricStatus = "normal";

  if (metric.value >= metric.actionThreshold) {
    status = "action";
  } else if (metric.value >= metric.warningThreshold) {
    status = "warning";
  }

  const interpretation =
    status === "action"
      ? `${metric.name} exceeds the action threshold and requires immediate review.`
      : status === "warning"
        ? `${metric.name} exceeds the warning threshold and should be monitored.`
        : `${metric.name} is within the expected operating range.`;

  return {
    ...metric,
    status,
    interpretation
  };
}

function summarize(snapshot: InfrastructureSnapshot): EvaluatedInfrastructureMetric[] {
  return snapshot.metrics.map(evaluateMetric);
}

function renderDashboard(snapshot: InfrastructureSnapshot, target: HTMLElement): void {
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
    <section class="smart-infrastructure-dashboard">
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

const exampleSnapshot: InfrastructureSnapshot = {
  systemId: "smart-network-001",
  systemName: "Smart Infrastructure Governance Dashboard",
  generatedAt: new Date().toISOString(),
  metrics: [
    {
      name: "mean_failure_probability",
      value: 0.31,
      warningThreshold: 0.45,
      actionThreshold: 0.60
    },
    {
      name: "data_quality_risk",
      value: 0.18,
      warningThreshold: 0.20,
      actionThreshold: 0.35
    },
    {
      name: "telemetry_latency_seconds",
      value: 7.8,
      warningThreshold: 15.0,
      actionThreshold: 30.0,
      unit: "seconds"
    },
    {
      name: "high_criticality_asset_share",
      value: 0.14,
      warningThreshold: 0.20,
      actionThreshold: 0.35
    }
  ]
};

const target = document.getElementById("app");

if (target) {
  renderDashboard(exampleSnapshot, target);
}

export {
  InfrastructureMetric,
  EvaluatedInfrastructureMetric,
  InfrastructureSnapshot,
  evaluateMetric,
  summarize,
  renderDashboard
};
