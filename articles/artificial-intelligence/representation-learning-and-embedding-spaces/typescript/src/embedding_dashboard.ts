interface EmbeddingMetric {
  name: string;
  value: number;
  warningThreshold: number;
  actionThreshold: number;
  unit?: string;
}

type MetricStatus = "normal" | "warning" | "action";

interface EvaluatedEmbeddingMetric extends EmbeddingMetric {
  status: MetricStatus;
  interpretation: string;
}

interface EmbeddingSnapshot {
  systemId: string;
  systemName: string;
  generatedAt: string;
  metrics: EmbeddingMetric[];
}

function evaluateMetric(metric: EmbeddingMetric): EvaluatedEmbeddingMetric {
  let status: MetricStatus = "normal";

  if (metric.value >= metric.actionThreshold) {
    status = "action";
  } else if (metric.value >= metric.warningThreshold) {
    status = "warning";
  }

  const interpretation =
    status === "action"
      ? `${metric.name} exceeds the action threshold and requires embedding-system review.`
      : status === "warning"
        ? `${metric.name} exceeds the warning threshold and should be monitored.`
        : `${metric.name} is within the expected embedding governance range.`;

  return {
    ...metric,
    status,
    interpretation
  };
}

function summarize(snapshot: EmbeddingSnapshot): EvaluatedEmbeddingMetric[] {
  return snapshot.metrics.map(evaluateMetric);
}

function renderDashboard(snapshot: EmbeddingSnapshot, target: HTMLElement): void {
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
    <section class="embedding-dashboard">
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

const exampleSnapshot: EmbeddingSnapshot = {
  systemId: "embedding-system-001",
  systemName: "Embedding Space Governance Dashboard",
  generatedAt: new Date().toISOString(),
  metrics: [
    {
      name: "low_similarity_query_share",
      value: 0.12,
      warningThreshold: 0.20,
      actionThreshold: 0.35
    },
    {
      name: "stale_embedding_share",
      value: 0.18,
      warningThreshold: 0.25,
      actionThreshold: 0.40
    },
    {
      name: "open_bias_review_count",
      value: 1,
      warningThreshold: 2,
      actionThreshold: 5
    },
    {
      name: "index_drift_score",
      value: 0.16,
      warningThreshold: 0.25,
      actionThreshold: 0.45
    }
  ]
};

const target = document.getElementById("app");

if (target) {
  renderDashboard(exampleSnapshot, target);
}

export {
  EmbeddingMetric,
  EvaluatedEmbeddingMetric,
  EmbeddingSnapshot,
  evaluateMetric,
  summarize,
  renderDashboard
};
