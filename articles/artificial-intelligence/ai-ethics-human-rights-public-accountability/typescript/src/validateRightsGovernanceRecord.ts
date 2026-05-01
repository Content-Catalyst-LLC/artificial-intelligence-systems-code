// Rights-governance record validator for AI accountability workflows.

type RightsGovernanceRecord = {
  systemName: string;
  rightsImpactAssessmentComplete: boolean;
  explanationProvided: boolean;
  appealAvailable: boolean;
  remedyAvailable: boolean;
  residualRightsRisk: number;
};

function validateRecord(record: RightsGovernanceRecord): string[] {
  const errors: string[] = [];

  if (!record.systemName) errors.push("Missing systemName.");

  if (record.residualRightsRisk < 0 || record.residualRightsRisk > 1) {
    errors.push("residualRightsRisk must be between 0 and 1.");
  }

  if (!record.rightsImpactAssessmentComplete) {
    errors.push("Rights-impact assessment is required.");
  }

  if (record.residualRightsRisk >= 0.35 && !record.appealAvailable) {
    errors.push("High residual rights risk requires an appeal pathway.");
  }

  if (record.appealAvailable && !record.remedyAvailable) {
    errors.push("Appeal pathway must be connected to remedy.");
  }

  if (!record.explanationProvided) {
    errors.push("Affected people should receive an explanation.");
  }

  return errors;
}

const example: RightsGovernanceRecord = {
  systemName: "public-benefits-review",
  rightsImpactAssessmentComplete: true,
  explanationProvided: true,
  appealAvailable: true,
  remedyAvailable: true,
  residualRightsRisk: 0.38
};

console.log(validateRecord(example));
