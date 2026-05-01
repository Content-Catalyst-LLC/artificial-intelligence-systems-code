interface LlmSystemMetric {
  name: string;
  value: number;
  warningThreshold: number;
  actionThreshold: number;
  unit?: string;
}

type MetricStatus = "normal" | "warning" | "action";

interface EvaluatedLlmSystemMetric extends LlmSystemMetric {
  status: MetricStatus;
  interpretation: string;
}

interface LlmSystemSnapshot {
  systemId: string;
  systemName: string;
  generatedAt: string;
  metrics: LlmSystemMetric[];
}

function evaluateMetric(metric: LlmSystemMetric): EvaluatedLlmSystemMetric {
  let status: MetricStatus = "normal";

  if (metric.value >= metric.actionThreshold) {
    status = "action";
  } else if (metric.value >= metric.warningThreshold) {
    status = "warning";
  }

  const interpretation =
    status === "action"
      ? `${metric.name} exceeds the action threshold and requires LLM system governance review.`
      : status === "warning"
        ? `${metric.name} exceeds the warning threshold and should be monitored.`
        : `${metric.name} is within the expected LLM system governance range.`;

  return {
    ...metric,
    status,
    interpretation
  };
}

function summarize(snapshot: LlmSystemSnapshot): EvaluatedLlmSystemMetric[] {
  return snapshot.metrics.map(evaluateMetric);
}

function renderDashboard(snapshot: LlmSystemSnapshot, target: HTMLElement): void {
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
    <section class="llm-system-dashboard">
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

const exampleSnapshot: LlmSystemSnapshot = {
  systemId: "llm-foundation-system-001",
  systemName: "LLM Foundation Model System Governance Dashboard",
  generatedAt: new Date().toISOString(),
  metrics: [
    {
      name: "low_grounding_rate",
      value: 0.16,
      warningThreshold: 0.20,
      actionThreshold: 0.35
    },
    {
      name: "prompt_injection_failure_rate",
      value: 0.07,
      warningThreshold: 0.10,
      actionThreshold: 0.20
    },
    {
      name: "privacy_control_failure_rate",
      value: 0.05,
      warningThreshold: 0.08,
      actionThreshold: 0.15
    },
    {
      name: "mean_latency_seconds",
      value: 3.8,
      warningThreshold: 6.0,
      actionThreshold: 10.0,
      unit: "seconds"
    },
    {
      name: "high_risk_unreviewed_count",
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
  LlmSystemMetric,
  EvaluatedLlmSystemMetric,
  LlmSystemSnapshot,
  evaluateMetric,
  summarize,
  renderDashboard
};
