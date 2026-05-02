// AI documentation governance record validator.

type DocumentationRecord = {
  systemName: string;
  modelCardComplete: boolean;
  systemCardComplete: boolean;
  dataDocumentationComplete: boolean;
  riskRegisterComplete: boolean;
  auditEvidenceComplete: boolean;
  monitoringPlanComplete: boolean;
  incidentResponsePlanComplete: boolean;
  residualRisk: number;
  documentationCompleteness: number;
};

function validateUnitInterval(name: string, value: number): string[] {
  if (value < 0 || value > 1) {
    return [`${name} must be between 0 and 1.`];
  }
  return [];
}

function validateRecord(record: DocumentationRecord): string[] {
  const errors: string[] = [];

  if (!record.systemName) errors.push("Missing systemName.");

  errors.push(...validateUnitInterval("residualRisk", record.residualRisk));
  errors.push(...validateUnitInterval("documentationCompleteness", record.documentationCompleteness));

  if (!record.modelCardComplete) errors.push("Model card is incomplete.");
  if (!record.systemCardComplete) errors.push("System card is incomplete.");
  if (!record.dataDocumentationComplete) errors.push("Data documentation is incomplete.");
  if (!record.riskRegisterComplete) errors.push("Risk register is incomplete.");

  if (record.residualRisk >= 0.20 && !record.auditEvidenceComplete) {
    errors.push("High residual risk requires complete audit evidence.");
  }

  if (record.residualRisk >= 0.20 && !record.monitoringPlanComplete) {
    errors.push("High residual risk requires a monitoring plan.");
  }

  if (record.residualRisk >= 0.20 && !record.incidentResponsePlanComplete) {
    errors.push("High residual risk requires an incident response plan.");
  }

  if (record.documentationCompleteness < 0.70) {
    errors.push("Documentation completeness is below governance threshold.");
  }

  return errors;
}

const example: DocumentationRecord = {
  systemName: "high-impact-review-system",
  modelCardComplete: true,
  systemCardComplete: false,
  dataDocumentationComplete: true,
  riskRegisterComplete: true,
  auditEvidenceComplete: false,
  monitoringPlanComplete: true,
  incidentResponsePlanComplete: true,
  residualRisk: 0.23,
  documentationCompleteness: 0.64
};

console.log(validateRecord(example));
