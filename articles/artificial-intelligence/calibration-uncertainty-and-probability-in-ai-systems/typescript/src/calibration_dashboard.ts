interface CalibrationMetric {
  name: string;
  value: number;
  warningThreshold: number;
  actionThreshold: number;
  unit?: string;
}

type MetricStatus = "normal" | "warning" | "action";

interface EvaluatedCalibrationMetric extends CalibrationMetric {
  status: MetricStatus;
  interpretation: string;
}

interface CalibrationSnapshot {
  systemId: string;
  systemName: string;
  generatedAt: string;
  metrics: CalibrationMetric[];
}

function evaluateMetric(metric: CalibrationMetric): EvaluatedCalibrationMetric {
  let status: MetricStatus = "normal";

  if (metric.value >= metric.actionThreshold) {
    status = "action";
  } else if (metric.value >= metric.warningThreshold) {
    status = "warning";
  }

  const interpretation =
    status === "action"
      ? `${metric.name} exceeds the action threshold and requires calibration governance review.`
      : status === "warning"
        ? `${metric.name} exceeds the warning threshold and should be investigated.`
        : `${metric.name} is within the expected calibration and uncertainty range.`;

  return {
    ...metric,
    status,
    interpretation
  };
}

function summarize(snapshot: CalibrationSnapshot): EvaluatedCalibrationMetric[] {
  return snapshot.metrics.map(evaluateMetric);
}

function renderDashboard(snapshot: CalibrationSnapshot, target: HTMLElement): void {
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
    <section class="calibration-dashboard">
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

const exampleSnapshot: CalibrationSnapshot = {
  systemId: "calibration-uncertainty-system-001",
  systemName: "Calibration and Uncertainty Governance Dashboard",
  generatedAt: new Date().toISOString(),
  metrics: [
    {
      name: "expected_calibration_error",
      value: 0.064,
      warningThreshold: 0.080,
      actionThreshold: 0.120
    },
    {
      name: "brier_score",
      value: 0.196,
      warningThreshold: 0.220,
      actionThreshold: 0.280
    },
    {
      name: "negative_log_likelihood",
      value: 0.612,
      warningThreshold: 0.700,
      actionThreshold: 0.900
    },
    {
      name: "mean_entropy",
      value: 0.482,
      warningThreshold: 0.620,
      actionThreshold: 0.700
    },
    {
      name: "human_review_rate",
      value: 0.426,
      warningThreshold: 0.500,
      actionThreshold: 0.650
    }
  ]
};

const target = document.getElementById("app");

if (target) {
  renderDashboard(exampleSnapshot, target);
}

export {
  CalibrationMetric,
  EvaluatedCalibrationMetric,
  CalibrationSnapshot,
  evaluateMetric,
  summarize,
  renderDashboard
};
