// Defensive AI security governance record validator.

type AISecurityRecord = {
  assetName: string;
  exposure: number;
  impact: number;
  likelihood: number;
  controlStrength: number;
  highImpactTool: boolean;
  humanApprovalRequired: boolean;
};

function validateRecord(record: AISecurityRecord): string[] {
  const errors: string[] = [];

  if (!record.assetName) errors.push("Missing assetName.");

  for (const [key, value] of Object.entries({
    exposure: record.exposure,
    impact: record.impact,
    likelihood: record.likelihood,
    controlStrength: record.controlStrength
  })) {
    if (value < 0 || value > 1) {
      errors.push(`${key} must be between 0 and 1.`);
    }
  }

  if (record.highImpactTool && !record.humanApprovalRequired) {
    errors.push("High-impact tools require human approval.");
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
  humanApprovalRequired: true
};

console.log(validateRecord(example));
