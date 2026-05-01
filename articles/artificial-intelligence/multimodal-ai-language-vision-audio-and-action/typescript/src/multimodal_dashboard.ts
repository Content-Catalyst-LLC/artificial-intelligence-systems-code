interface MultimodalMetric {
  name: string;
  value: number;
  warningThreshold: number;
  actionThreshold: number;
  unit?: string;
}

type MetricStatus = "normal" | "warning" | "action";

interface EvaluatedMultimodalMetric extends MultimodalMetric {
  status: MetricStatus;
  interpretation: string;
}

interface MultimodalSnapshot {
  systemId: string;
  systemName: string;
  generatedAt: string;
  metrics: MultimodalMetric[];
}

function evaluateMetric(metric: MultimodalMetric): EvaluatedMultimodalMetric {
  let status: MetricStatus = "normal";

  if (metric.value >= metric.actionThreshold) {
    status = "action";
  } else if (metric.value >= metric.warningThreshold) {
    status = "warning";
  }

  const interpretation =
    status === "action"
      ? `${metric.name} exceeds the action threshold and requires multimodal AI governance review.`
      : status === "warning"
        ? `${metric.name} exceeds the warning threshold and should be monitored.`
        : `${metric.name} is within the expected multimodal AI governance range.`;

  return {
    ...metric,
    status,
    interpretation
  };
}

function summarize(snapshot: MultimodalSnapshot): EvaluatedMultimodalMetric[] {
  return snapshot.metrics.map(evaluateMetric);
}

function renderDashboard(snapshot: MultimodalSnapshot, target: HTMLElement): void {
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
    <section class="multimodal-dashboard">
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

const exampleSnapshot: MultimodalSnapshot = {
  systemId: "multimodal-ai-system-001",
  systemName: "Multimodal AI Governance Dashboard",
  generatedAt: new Date().toISOString(),
  metrics: [
    {
      name: "low_alignment_rate",
      value: 0.14,
      warningThreshold: 0.18,
      actionThreshold: 0.30
    },
    {
      name: "low_grounding_rate",
      value: 0.12,
      warningThreshold: 0.18,
      actionThreshold: 0.30
    },
    {
      name: "modality_conflict_rate",
      value: 0.09,
      warningThreshold: 0.15,
      actionThreshold: 0.25
    },
    {
      name: "privacy_control_failure_rate",
      value: 0.05,
      warningThreshold: 0.08,
      actionThreshold: 0.15
    },
    {
      name: "unsafe_action_block_rate",
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
  MultimodalMetric,
  EvaluatedMultimodalMetric,
  MultimodalSnapshot,
  evaluateMetric,
  summarize,
  renderDashboard
};
