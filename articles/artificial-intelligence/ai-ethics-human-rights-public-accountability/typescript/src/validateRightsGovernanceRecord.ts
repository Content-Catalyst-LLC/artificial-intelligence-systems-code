// Rights-governance record validator for AI accountability workflows.

type RightsGovernanceRecord = {
  systemName: string;
  rightsImpactAssessmentComplete: boolean;
  explanationProvided: boolean;
  appealAvailable: boolean;
  remedyAvailable: boolean;
  publicReportingAvailable: boolean;
  stakeholderParticipationDocumented: boolean;
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

  if (record.residualRightsRisk >= 0.35 && !record.publicReportingAvailable) {
    errors.push("High-risk public-interest systems should support public reporting.");
  }

  if (record.residualRightsRisk >= 0.35 && !record.stakeholderParticipationDocumented) {
    errors.push("High-risk systems should document stakeholder participation.");
  }

  return errors;
}

const example: RightsGovernanceRecord = {
  systemName: "public-benefits-review",
  rightsImpactAssessmentComplete: true,
  explanationProvided: true,
  appealAvailable: true,
  remedyAvailable: true,
  publicReportingAvailable: true,
  stakeholderParticipationDocumented: true,
  residualRightsRisk: 0.38
};

console.log(validateRecord(example));
