interface SafetyMetric {
  name: string;
  value: number;
  warningThreshold: number;
  actionThreshold: number;
  unit?: string;
}

type SafetyStatus = "normal" | "warning" | "action";

interface EvaluatedMetric extends SafetyMetric {
  status: SafetyStatus;
  explanation: string;
}

interface SafetySnapshot {
  systemId: string;
  systemName: string;
  generatedAt: string;
  metrics: SafetyMetric[];
}

function evaluateMetric(metric: SafetyMetric): EvaluatedMetric {
  let status: SafetyStatus = "normal";

  if (metric.value >= metric.actionThreshold) {
    status = "action";
  } else if (metric.value >= metric.warningThreshold) {
    status = "warning";
  }

  const explanation =
    status === "action"
      ? `${metric.name} exceeds the action threshold and requires governance review.`
      : status === "warning"
        ? `${metric.name} exceeds the warning threshold and should be monitored.`
        : `${metric.name} is within the normal operating range.`;

  return {
    ...metric,
    status,
    explanation
  };
}

function summarizeSnapshot(snapshot: SafetySnapshot): EvaluatedMetric[] {
  return snapshot.metrics.map(evaluateMetric);
}

function countByStatus(metrics: EvaluatedMetric[]): Record<SafetyStatus, number> {
  return metrics.reduce(
    (accumulator, metric) => {
      accumulator[metric.status] += 1;
      return accumulator;
    },
    {
      normal: 0,
      warning: 0,
      action: 0
    } as Record<SafetyStatus, number>
  );
}

function renderDashboard(snapshot: SafetySnapshot, target: HTMLElement): void {
  const evaluated = summarizeSnapshot(snapshot);
  const counts = countByStatus(evaluated);

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
          <td>${metric.explanation}</td>
        </tr>
      `;
    })
    .join("");

  target.innerHTML = `
    <section class="safety-dashboard">
      <h1>${snapshot.systemName}</h1>
      <p><strong>Generated:</strong> ${snapshot.generatedAt}</p>

      <div class="summary-grid">
        <div><strong>Normal:</strong> ${counts.normal}</div>
        <div><strong>Warning:</strong> ${counts.warning}</div>
        <div><strong>Action:</strong> ${counts.action}</div>
      </div>

      <table>
        <thead>
          <tr>
            <th>Metric</th>
            <th>Value</th>
            <th>Warning Threshold</th>
            <th>Action Threshold</th>
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

const exampleSnapshot: SafetySnapshot = {
  systemId: "ai-safety-system-001",
  systemName: "AI Safety and System Reliability Dashboard",
  generatedAt: new Date().toISOString(),
  metrics: [
    {
      name: "missed_failure_rate",
      value: 0.018,
      warningThreshold: 0.01,
      actionThreshold: 0.025
    },
    {
      name: "expected_calibration_error",
      value: 0.061,
      warningThreshold: 0.05,
      actionThreshold: 0.10
    },
    {
      name: "data_drift_index",
      value: 0.19,
      warningThreshold: 0.10,
      actionThreshold: 0.25
    },
    {
      name: "human_review_rate",
      value: 0.214,
      warningThreshold: 0.35,
      actionThreshold: 0.50
    }
  ]
};

const target = document.getElementById("app");

if (target) {
  renderDashboard(exampleSnapshot, target);
}

export {
  SafetyMetric,
  SafetyStatus,
  EvaluatedMetric,
  SafetySnapshot,
  evaluateMetric,
  summarizeSnapshot,
  countByStatus,
  renderDashboard
};
