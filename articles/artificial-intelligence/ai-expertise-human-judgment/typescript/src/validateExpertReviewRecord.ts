type ExpertReviewRecord = {
  caseId: string;
  aiConfidence: number;
  contextComplexity: number;
  aiExpertDisagreement: number;
  observedAiReliance: number;
  warrantedAiReliance: number;
  finalDecisionDocumented: boolean;
};

function validateRecord(record: ExpertReviewRecord): string[] {
  const errors: string[] = [];

  if (!record.caseId) errors.push("Missing caseId.");

  if (record.aiConfidence < 0 || record.aiConfidence > 1) {
    errors.push("aiConfidence must be between 0 and 1.");
  }

  if (record.contextComplexity < 0 || record.contextComplexity > 1) {
    errors.push("contextComplexity must be between 0 and 1.");
  }

  if (record.observedAiReliance < 0 || record.observedAiReliance > 1) {
    errors.push("observedAiReliance must be between 0 and 1.");
  }

  if (record.warrantedAiReliance < 0 || record.warrantedAiReliance > 1) {
    errors.push("warrantedAiReliance must be between 0 and 1.");
  }

  if (record.contextComplexity > 0.65 && !record.finalDecisionDocumented) {
    errors.push("High-complexity cases require documented expert rationale.");
  }

  if (record.aiExpertDisagreement > 0.30 && !record.finalDecisionDocumented) {
    errors.push("High AI-expert disagreement requires documented review.");
  }

  if (
    record.observedAiReliance > record.warrantedAiReliance + 0.15 &&
    !record.finalDecisionDocumented
  ) {
    errors.push("Possible automation bias requires documented review.");
  }

  return errors;
}

const example: ExpertReviewRecord = {
  caseId: "CASE-001",
  aiConfidence: 0.81,
  contextComplexity: 0.72,
  aiExpertDisagreement: 0.34,
  observedAiReliance: 0.84,
  warrantedAiReliance: 0.58,
  finalDecisionDocumented: true
};

console.log(validateRecord(example));
