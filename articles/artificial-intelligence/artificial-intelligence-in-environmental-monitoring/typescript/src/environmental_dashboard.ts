interface EnvironmentalMetric {
  name: string;
  value: number;
  warningThreshold: number;
  actionThreshold: number;
  unit?: string;
}

type MetricStatus = "normal" | "warning" | "action";

interface EvaluatedEnvironmentalMetric extends EnvironmentalMetric {
  status: MetricStatus;
  interpretation: string;
}

interface EnvironmentalSnapshot {
  systemId: string;
  systemName: string;
  generatedAt: string;
  metrics: EnvironmentalMetric[];
}

function evaluateMetric(metric: EnvironmentalMetric): EvaluatedEnvironmentalMetric {
  let status: MetricStatus = "normal";

  if (metric.value >= metric.actionThreshold) {
    status = "action";
  } else if (metric.value >= metric.warningThreshold) {
    status = "warning";
  }

  const interpretation =
    status === "action"
      ? `${metric.name} exceeds the action threshold and requires immediate environmental review.`
      : status === "warning"
        ? `${metric.name} exceeds the warning threshold and should be monitored.`
        : `${metric.name} is within the expected monitoring range.`;

  return {
    ...metric,
    status,
    interpretation
  };
}

function summarize(snapshot: EnvironmentalSnapshot): EvaluatedEnvironmentalMetric[] {
  return snapshot.metrics.map(evaluateMetric);
}

function renderDashboard(snapshot: EnvironmentalSnapshot, target: HTMLElement): void {
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
    <section class="environmental-monitoring-dashboard">
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

const exampleSnapshot: EnvironmentalSnapshot = {
  systemId: "environmental-monitoring-001",
  systemName: "AI Environmental Monitoring Dashboard",
  generatedAt: new Date().toISOString(),
  metrics: [
    {
      name: "mean_environmental_stress_probability",
      value: 0.42,
      warningThreshold: 0.50,
      actionThreshold: 0.65
    },
    {
      name: "mean_anomaly_score",
      value: 0.81,
      warningThreshold: 1.00,
      actionThreshold: 1.50
    },
    {
      name: "data_quality_risk",
      value: 0.17,
      warningThreshold: 0.25,
      actionThreshold: 0.35
    },
    {
      name: "open_alert_count",
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
  EnvironmentalMetric,
  EvaluatedEnvironmentalMetric,
  EnvironmentalSnapshot,
  evaluateMetric,
  summarize,
  renderDashboard
};
