// AI documentation governance record validator.

type DocumentationRecord = {
  systemName: string;
  modelCardComplete: boolean;
  riskRegisterComplete: boolean;
  auditEvidenceComplete: boolean;
  monitoringPlanComplete: boolean;
  residualRisk: number;
};

function validateRecord(record: DocumentationRecord): string[] {
  const errors: string[] = [];

  if (!record.systemName) errors.push("Missing systemName.");

  if (record.residualRisk < 0 || record.residualRisk > 1) {
    errors.push("residualRisk must be between 0 and 1.");
  }

  if (!record.modelCardComplete) {
    errors.push("Model card is incomplete.");
  }

  if (!record.riskRegisterComplete) {
    errors.push("Risk register is incomplete.");
  }

  if (record.residualRisk >= 0.20 && !record.auditEvidenceComplete) {
    errors.push("High residual risk requires complete audit evidence.");
  }

  if (record.residualRisk >= 0.20 && !record.monitoringPlanComplete) {
    errors.push("High residual risk requires a monitoring plan.");
  }

  return errors;
}

const example: DocumentationRecord = {
  systemName: "high-impact-review-system",
  modelCardComplete: true,
  riskRegisterComplete: true,
  auditEvidenceComplete: false,
  monitoringPlanComplete: true,
  residualRisk: 0.23
};

console.log(validateRecord(example));
