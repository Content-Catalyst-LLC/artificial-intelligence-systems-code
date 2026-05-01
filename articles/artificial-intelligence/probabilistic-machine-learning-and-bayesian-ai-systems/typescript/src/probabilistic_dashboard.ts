interface ProbabilisticMetric {
  name: string;
  value: number;
  warningThreshold: number;
  actionThreshold: number;
  unit?: string;
}

type MetricStatus = "normal" | "warning" | "action";

interface EvaluatedProbabilisticMetric extends ProbabilisticMetric {
  status: MetricStatus;
  interpretation: string;
}

interface ProbabilisticSnapshot {
  systemId: string;
  systemName: string;
  generatedAt: string;
  metrics: ProbabilisticMetric[];
}

function evaluateMetric(metric: ProbabilisticMetric): EvaluatedProbabilisticMetric {
  let status: MetricStatus = "normal";

  if (metric.value >= metric.actionThreshold) {
    status = "action";
  } else if (metric.value >= metric.warningThreshold) {
    status = "warning";
  }

  const interpretation =
    status === "action"
      ? `${metric.name} exceeds the action threshold and requires Bayesian AI governance review.`
      : status === "warning"
        ? `${metric.name} exceeds the warning threshold and should be monitored.`
        : `${metric.name} is within the expected probabilistic AI governance range.`;

  return {
    ...metric,
    status,
    interpretation
  };
}

function summarize(snapshot: ProbabilisticSnapshot): EvaluatedProbabilisticMetric[] {
  return snapshot.metrics.map(evaluateMetric);
}

function renderDashboard(snapshot: ProbabilisticSnapshot, target: HTMLElement): void {
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
    <section class="probabilistic-dashboard">
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

const exampleSnapshot: ProbabilisticSnapshot = {
  systemId: "bayesian-ai-system-001",
  systemName: "Probabilistic Machine Learning Governance Dashboard",
  generatedAt: new Date().toISOString(),
  metrics: [
    {
      name: "mean_calibration_error",
      value: 0.06,
      warningThreshold: 0.08,
      actionThreshold: 0.12
    },
    {
      name: "high_uncertainty_case_share",
      value: 0.18,
      warningThreshold: 0.25,
      actionThreshold: 0.40
    },
    {
      name: "unreviewed_prior_count",
      value: 1,
      warningThreshold: 2,
      actionThreshold: 5
    },
    {
      name: "inference_diagnostic_warning_count",
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
  ProbabilisticMetric,
  EvaluatedProbabilisticMetric,
  ProbabilisticSnapshot,
  evaluateMetric,
  summarize,
  renderDashboard
};
