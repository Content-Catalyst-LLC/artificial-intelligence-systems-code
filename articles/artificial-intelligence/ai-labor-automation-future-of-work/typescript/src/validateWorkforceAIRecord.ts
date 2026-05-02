// Workforce AI governance record validator.

type WorkforceAIRecord = {
  systemName: string;
  workerConsultationComplete: boolean;
  trainingPlanAvailable: boolean;
  appealPathwayAvailable: boolean;
  privacySafeguardsDocumented: boolean;
  gainSharingReviewed: boolean;
  meanAIExposure: number;
  monitoringBurden: number;
  workerVoice: number;
  affectsDisciplineOrTermination: boolean;
};

function validateUnitInterval(name: string, value: number): string[] {
  if (value < 0 || value > 1) {
    return [`${name} must be between 0 and 1.`];
  }
  return [];
}

function validateRecord(record: WorkforceAIRecord): string[] {
  const errors: string[] = [];

  if (!record.systemName) errors.push("Missing systemName.");

  errors.push(...validateUnitInterval("meanAIExposure", record.meanAIExposure));
  errors.push(...validateUnitInterval("monitoringBurden", record.monitoringBurden));
  errors.push(...validateUnitInterval("workerVoice", record.workerVoice));

  if (record.meanAIExposure >= 0.60 && !record.trainingPlanAvailable) {
    errors.push("High AI exposure requires a training or transition plan.");
  }

  if (record.monitoringBurden >= 0.60 && !record.workerConsultationComplete) {
    errors.push("High monitoring burden requires worker consultation.");
  }

  if (record.monitoringBurden >= 0.60 && !record.privacySafeguardsDocumented) {
    errors.push("High monitoring burden requires documented privacy safeguards.");
  }

  if (record.affectsDisciplineOrTermination && !record.appealPathwayAvailable) {
    errors.push("Systems affecting discipline or termination require an appeal pathway.");
  }

  if (record.meanAIExposure >= 0.60 && !record.gainSharingReviewed) {
    errors.push("High-exposure workplace AI systems should review productivity gain sharing.");
  }

  if (record.workerVoice < 0.40 && !record.workerConsultationComplete) {
    errors.push("Low worker voice requires documented consultation.");
  }

  return errors;
}

const example: WorkforceAIRecord = {
  systemName: "workplace-ai-evaluation-system",
  workerConsultationComplete: true,
  trainingPlanAvailable: true,
  appealPathwayAvailable: true,
  privacySafeguardsDocumented: true,
  gainSharingReviewed: true,
  meanAIExposure: 0.66,
  monitoringBurden: 0.62,
  workerVoice: 0.48,
  affectsDisciplineOrTermination: true
};

console.log(validateRecord(example));
