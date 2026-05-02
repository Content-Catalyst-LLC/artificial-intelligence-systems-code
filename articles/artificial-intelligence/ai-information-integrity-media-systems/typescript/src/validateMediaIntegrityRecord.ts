// Media-integrity governance record validator.

type MediaIntegrityRecord = {
  contentId: string;
  aiGeneratedOrAssisted: boolean;
  syntheticMedia: boolean;
  provenanceAvailable: boolean;
  sourceCredibility: number;
  informationIntegrityRisk: number;
  correctionAvailable: boolean;
  humanReviewed: boolean;
  publicImpact: number;
};

function validateUnitInterval(name: string, value: number): string[] {
  if (value < 0 || value > 1) {
    return [`${name} must be between 0 and 1.`];
  }
  return [];
}

function validateRecord(record: MediaIntegrityRecord): string[] {
  const errors: string[] = [];

  if (!record.contentId) errors.push("Missing contentId.");

  errors.push(...validateUnitInterval("sourceCredibility", record.sourceCredibility));
  errors.push(...validateUnitInterval("informationIntegrityRisk", record.informationIntegrityRisk));
  errors.push(...validateUnitInterval("publicImpact", record.publicImpact));

  if (record.aiGeneratedOrAssisted && !record.provenanceAvailable) {
    errors.push("AI-generated or AI-assisted media should include provenance or disclosure where appropriate.");
  }

  if (record.syntheticMedia && record.publicImpact >= 0.70 && !record.provenanceAvailable) {
    errors.push("High-impact synthetic media requires provenance review.");
  }

  if (record.informationIntegrityRisk >= 0.50 && !record.correctionAvailable) {
    errors.push("High information-integrity risk requires a correction or review pathway.");
  }

  if (record.informationIntegrityRisk >= 0.50 && !record.humanReviewed) {
    errors.push("High information-integrity risk requires human review.");
  }

  return errors;
}

const example: MediaIntegrityRecord = {
  contentId: "C-001",
  aiGeneratedOrAssisted: true,
  syntheticMedia: true,
  provenanceAvailable: false,
  sourceCredibility: 0.40,
  informationIntegrityRisk: 0.62,
  correctionAvailable: true,
  humanReviewed: false,
  publicImpact: 0.85
};

console.log(validateRecord(example));
