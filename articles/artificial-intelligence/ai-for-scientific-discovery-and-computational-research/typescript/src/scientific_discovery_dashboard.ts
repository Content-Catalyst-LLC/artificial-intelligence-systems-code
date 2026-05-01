interface ResearchMetric {
  name: string;
  value: number;
  warningThreshold: number;
  actionThreshold: number;
  unit?: string;
}

type MetricStatus = "normal" | "warning" | "action";

interface EvaluatedResearchMetric extends ResearchMetric {
  status: MetricStatus;
  interpretation: string;
}

interface ResearchSnapshot {
  projectId: string;
  projectName: string;
  generatedAt: string;
  metrics: ResearchMetric[];
}

function evaluateMetric(metric: ResearchMetric): EvaluatedResearchMetric {
  let status: MetricStatus = "normal";

  if (metric.value >= metric.actionThreshold) {
    status = "action";
  } else if (metric.value >= metric.warningThreshold) {
    status = "warning";
  }

  const interpretation =
    status === "action"
      ? `${metric.name} exceeds the action threshold and requires scientific governance review.`
      : status === "warning"
        ? `${metric.name} exceeds the warning threshold and should be reviewed.`
        : `${metric.name} is within the expected research-control range.`;

  return {
    ...metric,
    status,
    interpretation
  };
}

function summarize(snapshot: ResearchSnapshot): EvaluatedResearchMetric[] {
  return snapshot.metrics.map(evaluateMetric);
}

function renderDashboard(snapshot: ResearchSnapshot, target: HTMLElement): void {
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
    <section class="scientific-discovery-dashboard">
      <h1>${snapshot.projectName}</h1>
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

const exampleSnapshot: ResearchSnapshot = {
  projectId: "scientific-discovery-001",
  projectName: "AI Scientific Discovery Governance Dashboard",
  generatedAt: new Date().toISOString(),
  metrics: [
    {
      name: "open_validation_failures",
      value: 1,
      warningThreshold: 2,
      actionThreshold: 5
    },
    {
      name: "high_uncertainty_candidate_share",
      value: 0.12,
      warningThreshold: 0.25,
      actionThreshold: 0.40
    },
    {
      name: "reproducibility_failure_rate",
      value: 0.03,
      warningThreshold: 0.05,
      actionThreshold: 0.10
    },
    {
      name: "unreviewed_hypothesis_count",
      value: 4,
      warningThreshold: 8,
      actionThreshold: 15
    }
  ]
};

const target = document.getElementById("app");

if (target) {
  renderDashboard(exampleSnapshot, target);
}

export {
  ResearchMetric,
  EvaluatedResearchMetric,
  ResearchSnapshot,
  evaluateMetric,
  summarize,
  renderDashboard
};
