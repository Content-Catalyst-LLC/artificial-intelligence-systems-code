type GovernanceRecord = {
  caseId: string;
  expectedRisk: number;
  uncertainty: number;
  rightsSensitive: boolean;
  vulnerableContext: boolean;
  route: "human_review" | "standard_processing";
};

function validateRecord(record: GovernanceRecord): string[] {
  const errors: string[] = [];

  if (!record.caseId) errors.push("Missing caseId.");

  if (record.expectedRisk < 0 || record.expectedRisk > 1) {
    errors.push("expectedRisk must be between 0 and 1.");
  }

  if (record.uncertainty < 0 || record.uncertainty > 1) {
    errors.push("uncertainty must be between 0 and 1.");
  }

  const shouldReview =
    record.expectedRisk >= 0.18 ||
    record.uncertainty >= 0.55 ||
    record.rightsSensitive ||
    record.vulnerableContext;

  if (shouldReview && record.route !== "human_review") {
    errors.push("Record should route to human_review under governance rules.");
  }

  return errors;
}

const example: GovernanceRecord = {
  caseId: "CASE-001",
  expectedRisk: 0.21,
  uncertainty: 0.35,
  rightsSensitive: false,
  vulnerableContext: false,
  route: "human_review"
};

console.log(validateRecord(example));
