// Defensive AI security governance record validator.

type AISecurityRecord = {
  assetName: string;
  exposure: number;
  impact: number;
  likelihood: number;
  controlStrength: number;
  highImpactTool: boolean;
  humanApprovalRequired: boolean;
  loggingEnabled: boolean;
  rollbackAvailable: boolean;
};

function validateUnitInterval(name: string, value: number): string[] {
  if (value < 0 || value > 1) {
    return [`${name} must be between 0 and 1.`];
  }
  return [];
}

function validateRecord(record: AISecurityRecord): string[] {
  const errors: string[] = [];

  if (!record.assetName) errors.push("Missing assetName.");

  errors.push(...validateUnitInterval("exposure", record.exposure));
  errors.push(...validateUnitInterval("impact", record.impact));
  errors.push(...validateUnitInterval("likelihood", record.likelihood));
  errors.push(...validateUnitInterval("controlStrength", record.controlStrength));

  if (record.highImpactTool && !record.humanApprovalRequired) {
    errors.push("High-impact tools require human approval.");
  }

  if (record.highImpactTool && !record.loggingEnabled) {
    errors.push("High-impact tools require logging.");
  }

  if (record.highImpactTool && !record.rollbackAvailable) {
    errors.push("High-impact tools should have rollback or containment procedures.");
  }

  return errors;
}

const example: AISecurityRecord = {
  assetName: "tool_api_gateway",
  exposure: 0.90,
  impact: 0.95,
  likelihood: 0.70,
  controlStrength: 0.55,
  highImpactTool: true,
  humanApprovalRequired: true,
  loggingEnabled: true,
  rollbackAvailable: true
};

console.log(validateRecord(example));
