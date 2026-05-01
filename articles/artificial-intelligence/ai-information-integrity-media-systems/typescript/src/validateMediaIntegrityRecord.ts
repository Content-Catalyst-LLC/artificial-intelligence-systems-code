// Media-integrity governance record validator.

type MediaIntegrityRecord = {
  contentId: string;
  aiGenerated: boolean;
  provenanceAvailable: boolean;
  sourceCredibility: number;
  informationIntegrityRisk: number;
  correctionAvailable: boolean;
  publicImpact: number;
};

function validateRecord(record: MediaIntegrityRecord): string[] {
  const errors: string[] = [];

  if (!record.contentId) errors.push("Missing contentId.");

  for (const [key, value] of Object.entries({
    sourceCredibility: record.sourceCredibility,
    informationIntegrityRisk: record.informationIntegrityRisk,
    publicImpact: record.publicImpact
  })) {
    if (value < 0 || value > 1) {
      errors.push(`${key} must be between 0 and 1.`);
    }
  }

  if (record.aiGenerated && !record.provenanceAvailable) {
    errors.push("AI-generated media should include provenance or disclosure where appropriate.");
  }

  if (record.informationIntegrityRisk >= 0.50 && !record.correctionAvailable) {
    errors.push("High information-integrity risk requires a correction or review pathway.");
  }

  return errors;
}

const example: MediaIntegrityRecord = {
  contentId: "C-001",
  aiGenerated: true,
  provenanceAvailable: false,
  sourceCredibility: 0.40,
  informationIntegrityRisk: 0.62,
  correctionAvailable: true,
  publicImpact: 0.85
};

console.log(validateRecord(example));
