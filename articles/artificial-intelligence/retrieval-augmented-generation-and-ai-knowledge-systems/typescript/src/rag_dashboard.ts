interface RagMetric {
  name: string;
  value: number;
  warningThreshold: number;
  actionThreshold: number;
  unit?: string;
}

type MetricStatus = "normal" | "warning" | "action";

interface EvaluatedRagMetric extends RagMetric {
  status: MetricStatus;
  interpretation: string;
}

interface RagSnapshot {
  systemId: string;
  systemName: string;
  generatedAt: string;
  metrics: RagMetric[];
}

function evaluateMetric(metric: RagMetric): EvaluatedRagMetric {
  let status: MetricStatus = "normal";

  if (metric.value >= metric.actionThreshold) {
    status = "action";
  } else if (metric.value >= metric.warningThreshold) {
    status = "warning";
  }

  const interpretation =
    status === "action"
      ? `${metric.name} exceeds the action threshold and requires RAG knowledge-system governance review.`
      : status === "warning"
        ? `${metric.name} exceeds the warning threshold and should be monitored.`
        : `${metric.name} is within the expected RAG governance range.`;

  return {
    ...metric,
    status,
    interpretation
  };
}

function summarize(snapshot: RagSnapshot): EvaluatedRagMetric[] {
  return snapshot.metrics.map(evaluateMetric);
}

function renderDashboard(snapshot: RagSnapshot, target: HTMLElement): void {
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
    <section class="rag-dashboard">
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

const exampleSnapshot: RagSnapshot = {
  systemId: "rag-knowledge-system-001",
  systemName: "RAG Knowledge System Governance Dashboard",
  generatedAt: new Date().toISOString(),
  metrics: [
    {
      name: "unsupported_citation_rate",
      value: 0.07,
      warningThreshold: 0.10,
      actionThreshold: 0.20
    },
    {
      name: "low_grounding_rate",
      value: 0.12,
      warningThreshold: 0.18,
      actionThreshold: 0.30
    },
    {
      name: "stale_source_rate",
      value: 0.09,
      warningThreshold: 0.15,
      actionThreshold: 0.25
    },
    {
      name: "prompt_injection_detection_rate",
      value: 0.03,
      warningThreshold: 0.08,
      actionThreshold: 0.15
    },
    {
      name: "access_control_denial_rate",
      value: 0.04,
      warningThreshold: 0.08,
      actionThreshold: 0.16
    }
  ]
};

const target = document.getElementById("app");

if (target) {
  renderDashboard(exampleSnapshot, target);
}

export {
  RagMetric,
  EvaluatedRagMetric,
  RagSnapshot,
  evaluateMetric,
  summarize,
  renderDashboard
};
