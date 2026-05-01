interface PortfolioMetric {
  name: string;
  value: number;
  warningThreshold: number;
  actionThreshold: number;
  unit?: string;
}

type MetricStatus = "normal" | "warning" | "action";

interface EvaluatedPortfolioMetric extends PortfolioMetric {
  status: MetricStatus;
  interpretation: string;
}

interface PortfolioSnapshot {
  portfolioId: string;
  portfolioName: string;
  generatedAt: string;
  metrics: PortfolioMetric[];
}

function evaluateMetric(metric: PortfolioMetric): EvaluatedPortfolioMetric {
  let status: MetricStatus = "normal";

  if (metric.value >= metric.actionThreshold) {
    status = "action";
  } else if (metric.value >= metric.warningThreshold) {
    status = "warning";
  }

  const interpretation =
    status === "action"
      ? `${metric.name} exceeds the action threshold and requires portfolio governance review.`
      : status === "warning"
        ? `${metric.name} exceeds the warning threshold and should be monitored.`
        : `${metric.name} is within the expected AI systems governance range.`;

  return {
    ...metric,
    status,
    interpretation
  };
}

function summarize(snapshot: PortfolioSnapshot): EvaluatedPortfolioMetric[] {
  return snapshot.metrics.map(evaluateMetric);
}

function renderDashboard(snapshot: PortfolioSnapshot, target: HTMLElement): void {
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
    <section class="ai-systems-dashboard">
      <h1>${snapshot.portfolioName}</h1>
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

const exampleSnapshot: PortfolioSnapshot = {
  portfolioId: "ai-systems-portfolio-001",
  portfolioName: "AI Systems Discipline Governance Dashboard",
  generatedAt: new Date().toISOString(),
  metrics: [
    {
      name: "systems_requiring_review_share",
      value: 0.22,
      warningThreshold: 0.25,
      actionThreshold: 0.40
    },
    {
      name: "high_risk_low_oversight_count",
      value: 2,
      warningThreshold: 3,
      actionThreshold: 8
    },
    {
      name: "low_monitoring_system_share",
      value: 0.18,
      warningThreshold: 0.25,
      actionThreshold: 0.40
    },
    {
      name: "open_ai_incidents",
      value: 1,
      warningThreshold: 2,
      actionThreshold: 5
    }
  ]
};

const target = document.getElementById("app");

if (target) {
  renderDashboard(exampleSnapshot, target);
}

export {
  PortfolioMetric,
  EvaluatedPortfolioMetric,
  PortfolioSnapshot,
  evaluateMetric,
  summarize,
  renderDashboard
};
