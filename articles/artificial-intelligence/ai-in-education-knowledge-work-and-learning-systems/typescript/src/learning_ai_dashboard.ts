interface LearningMetric {
  name: string;
  value: number;
  warningThreshold: number;
  actionThreshold: number;
  lowerIsWorse: boolean;
  unit?: string;
}

type MetricStatus = "normal" | "warning" | "action";

interface EvaluatedLearningMetric extends LearningMetric {
  status: MetricStatus;
  interpretation: string;
}

interface LearningSnapshot {
  systemId: string;
  systemName: string;
  generatedAt: string;
  metrics: LearningMetric[];
}

function evaluateMetric(metric: LearningMetric): EvaluatedLearningMetric {
  let status: MetricStatus = "normal";

  if (metric.lowerIsWorse) {
    if (metric.value <= metric.actionThreshold) {
      status = "action";
    } else if (metric.value <= metric.warningThreshold) {
      status = "warning";
    }
  } else {
    if (metric.value >= metric.actionThreshold) {
      status = "action";
    } else if (metric.value >= metric.warningThreshold) {
      status = "warning";
    }
  }

  const interpretation =
    status === "action"
      ? `${metric.name} is at an action threshold and requires learning-system governance review.`
      : status === "warning"
        ? `${metric.name} is at a warning threshold and should be investigated.`
        : `${metric.name} is within the expected learning-system monitoring range.`;

  return {
    ...metric,
    status,
    interpretation
  };
}

function summarize(snapshot: LearningSnapshot): EvaluatedLearningMetric[] {
  return snapshot.metrics.map(evaluateMetric);
}

function renderDashboard(snapshot: LearningSnapshot, target: HTMLElement): void {
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
    <section class="learning-ai-dashboard">
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

const exampleSnapshot: LearningSnapshot = {
  systemId: "learning-ai-system-001",
  systemName: "Education AI and Learning-System Governance Dashboard",
  generatedAt: new Date().toISOString(),
  metrics: [
    {
      name: "learning_gain",
      value: 0.13,
      warningThreshold: 0.05,
      actionThreshold: 0.02,
      lowerIsWorse: true
    },
    {
      name: "independent_transfer",
      value: 0.64,
      warningThreshold: 0.55,
      actionThreshold: 0.45,
      lowerIsWorse: true
    },
    {
      name: "assistance_gap",
      value: 0.12,
      warningThreshold: 0.18,
      actionThreshold: 0.25,
      lowerIsWorse: false
    },
    {
      name: "feedback_quality",
      value: 0.68,
      warningThreshold: 0.45,
      actionThreshold: 0.35,
      lowerIsWorse: true
    },
    {
      name: "privacy_risk",
      value: 0.28,
      warningThreshold: 0.45,
      actionThreshold: 0.60,
      lowerIsWorse: false
    },
    {
      name: "assessment_substitution_risk",
      value: 0.31,
      warningThreshold: 0.50,
      actionThreshold: 0.65,
      lowerIsWorse: false
    }
  ]
};

const target = document.getElementById("app");

if (target) {
  renderDashboard(exampleSnapshot, target);
}

export {
  LearningMetric,
  EvaluatedLearningMetric,
  LearningSnapshot,
  evaluateMetric,
  summarize,
  renderDashboard
};
