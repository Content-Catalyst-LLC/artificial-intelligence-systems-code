interface ExplanationMetric {
  name: string;
  value: number;
  threshold: number;
  higherIsBetter: boolean;
}

type ReviewStatus = "pass" | "review";

interface EvaluatedExplanationMetric extends ExplanationMetric {
  status: ReviewStatus;
  interpretation: string;
}

interface ExplanationAuditSnapshot {
  systemId: string;
  systemName: string;
  generatedAt: string;
  metrics: ExplanationMetric[];
}

function evaluateMetric(metric: ExplanationMetric): EvaluatedExplanationMetric {
  const failed = metric.higherIsBetter
    ? metric.value < metric.threshold
    : metric.value > metric.threshold;

  const status: ReviewStatus = failed ? "review" : "pass";

  const interpretation =
    status === "review"
      ? `${metric.name} requires review before explanations are used for governance.`
      : `${metric.name} is within the approved explanation quality range.`;

  return {
    ...metric,
    status,
    interpretation
  };
}

function summarizeAudit(snapshot: ExplanationAuditSnapshot): EvaluatedExplanationMetric[] {
  return snapshot.metrics.map(evaluateMetric);
}

function renderExplanationDashboard(snapshot: ExplanationAuditSnapshot, target: HTMLElement): void {
  const evaluated = summarizeAudit(snapshot);
  const reviewCount = evaluated.filter((metric) => metric.status === "review").length;

  const rows = evaluated
    .map((metric) => {
      return `
        <tr>
          <td>${metric.name}</td>
          <td>${metric.value.toFixed(4)}</td>
          <td>${metric.threshold.toFixed(4)}</td>
          <td>${metric.status}</td>
          <td>${metric.interpretation}</td>
        </tr>
      `;
    })
    .join("");

  target.innerHTML = `
    <section class="xai-dashboard">
      <h1>${snapshot.systemName}</h1>
      <p><strong>Generated:</strong> ${snapshot.generatedAt}</p>
      <p><strong>Metrics requiring review:</strong> ${reviewCount}</p>

      <table>
        <thead>
          <tr>
            <th>Metric</th>
            <th>Value</th>
            <th>Threshold</th>
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

const exampleSnapshot: ExplanationAuditSnapshot = {
  systemId: "xai-system-001",
  systemName: "Explainable AI Governance Dashboard",
  generatedAt: new Date().toISOString(),
  metrics: [
    {
      name: "mean_explanation_stability",
      value: 0.78,
      threshold: 0.70,
      higherIsBetter: true
    },
    {
      name: "mean_explanation_fidelity",
      value: 0.86,
      threshold: 0.80,
      higherIsBetter: true
    },
    {
      name: "counterfactual_actionability",
      value: 0.74,
      threshold: 0.70,
      higherIsBetter: true
    },
    {
      name: "sensitive_feature_change_rate",
      value: 0.02,
      threshold: 0.05,
      higherIsBetter: false
    }
  ]
};

const target = document.getElementById("app");

if (target) {
  renderExplanationDashboard(exampleSnapshot, target);
}

export {
  ExplanationMetric,
  EvaluatedExplanationMetric,
  ExplanationAuditSnapshot,
  evaluateMetric,
  summarizeAudit,
  renderExplanationDashboard
};
