interface ClinicalMetric {
  name: string;
  value: number;
  warningThreshold: number;
  actionThreshold: number;
  lowerIsWorse: boolean;
  unit?: string;
}

type MetricStatus = "normal" | "warning" | "action";

interface EvaluatedClinicalMetric extends ClinicalMetric {
  status: MetricStatus;
  interpretation: string;
}

interface ClinicalSnapshot {
  systemId: string;
  systemName: string;
  generatedAt: string;
  metrics: ClinicalMetric[];
}

function evaluateMetric(metric: ClinicalMetric): EvaluatedClinicalMetric {
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
      ? `${metric.name} is at an action threshold and requires clinical AI governance review.`
      : status === "warning"
        ? `${metric.name} is at a warning threshold and should be investigated.`
        : `${metric.name} is within the expected clinical AI monitoring range.`;

  return {
    ...metric,
    status,
    interpretation
  };
}

function summarize(snapshot: ClinicalSnapshot): EvaluatedClinicalMetric[] {
  return snapshot.metrics.map(evaluateMetric);
}

function renderDashboard(snapshot: ClinicalSnapshot, target: HTMLElement): void {
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
    <section class="clinical-ai-dashboard">
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

const exampleSnapshot: ClinicalSnapshot = {
  systemId: "clinical-ai-system-001",
  systemName: "Clinical AI Governance Dashboard",
  generatedAt: new Date().toISOString(),
  metrics: [
    {
      name: "sensitivity",
      value: 0.78,
      warningThreshold: 0.72,
      actionThreshold: 0.65,
      lowerIsWorse: true
    },
    {
      name: "specificity",
      value: 0.69,
      warningThreshold: 0.60,
      actionThreshold: 0.50,
      lowerIsWorse: true
    },
    {
      name: "expected_calibration_error",
      value: 0.052,
      warningThreshold: 0.080,
      actionThreshold: 0.120,
      lowerIsWorse: false
    },
    {
      name: "alert_rate",
      value: 0.31,
      warningThreshold: 0.40,
      actionThreshold: 0.55,
      lowerIsWorse: false
    },
    {
      name: "false_negative_rate",
      value: 0.15,
      warningThreshold: 0.20,
      actionThreshold: 0.30,
      lowerIsWorse: false
    }
  ]
};

const target = document.getElementById("app");

if (target) {
  renderDashboard(exampleSnapshot, target);
}

export {
  ClinicalMetric,
  EvaluatedClinicalMetric,
  ClinicalSnapshot,
  evaluateMetric,
  summarize,
  renderDashboard
};
