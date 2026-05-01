interface ResilienceMetric {
  name: string;
  value: number;
  warningThreshold: number;
  actionThreshold: number;
  unit?: string;
}

type MetricStatus = "normal" | "warning" | "action";

interface EvaluatedResilienceMetric extends ResilienceMetric {
  status: MetricStatus;
  interpretation: string;
}

interface ResilienceSnapshot {
  systemId: string;
  systemName: string;
  generatedAt: string;
  metrics: ResilienceMetric[];
}

function evaluateMetric(metric: ResilienceMetric): EvaluatedResilienceMetric {
  let status: MetricStatus = "normal";

  if (metric.value >= metric.actionThreshold) {
    status = "action";
  } else if (metric.value >= metric.warningThreshold) {
    status = "warning";
  }

  const interpretation =
    status === "action"
      ? `${metric.name} exceeds the action threshold and requires adversarial resilience review.`
      : status === "warning"
        ? `${metric.name} exceeds the warning threshold and should be investigated.`
        : `${metric.name} is within the expected resilience range.`;

  return {
    ...metric,
    status,
    interpretation
  };
}

function summarize(snapshot: ResilienceSnapshot): EvaluatedResilienceMetric[] {
  return snapshot.metrics.map(evaluateMetric);
}

function renderDashboard(snapshot: ResilienceSnapshot, target: HTMLElement): void {
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
    <section class="resilience-dashboard">
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

const exampleSnapshot: ResilienceSnapshot = {
  systemId: "adversarial-resilience-system-001",
  systemName: "Adversarial Resilience Governance Dashboard",
  generatedAt: new Date().toISOString(),
  metrics: [
    {
      name: "adversarial_performance_drop",
      value: 0.18,
      warningThreshold: 0.20,
      actionThreshold: 0.30
    },
    {
      name: "attack_success_rate",
      value: 0.14,
      warningThreshold: 0.20,
      actionThreshold: 0.35
    },
    {
      name: "prompt_injection_success_rate",
      value: 0.09,
      warningThreshold: 0.12,
      actionThreshold: 0.25
    },
    {
      name: "containment_failure_rate",
      value: 0.05,
      warningThreshold: 0.08,
      actionThreshold: 0.15
    },
    {
      name: "high_severity_incident_rate",
      value: 0.03,
      warningThreshold: 0.05,
      actionThreshold: 0.10
    }
  ]
};

const target = document.getElementById("app");

if (target) {
  renderDashboard(exampleSnapshot, target);
}

export {
  ResilienceMetric,
  EvaluatedResilienceMetric,
  ResilienceSnapshot,
  evaluateMetric,
  summarize,
  renderDashboard
};
