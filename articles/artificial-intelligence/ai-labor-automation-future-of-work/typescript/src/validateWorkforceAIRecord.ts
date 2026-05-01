// Workforce AI governance record validator.

type WorkforceAIRecord = {
  systemName: string;
  workerConsultationComplete: boolean;
  trainingPlanAvailable: boolean;
  appealPathwayAvailable: boolean;
  meanAIExposure: number;
  monitoringBurden: number;
  affectsDisciplineOrTermination: boolean;
};

function validateRecord(record: WorkforceAIRecord): string[] {
  const errors: string[] = [];

  if (!record.systemName) errors.push("Missing systemName.");

  for (const [key, value] of Object.entries({
    meanAIExposure: record.meanAIExposure,
    monitoringBurden: record.monitoringBurden
  })) {
    if (value < 0 || value > 1) {
      errors.push(`${key} must be between 0 and 1.`);
    }
  }

  if (record.meanAIExposure >= 0.60 && !record.trainingPlanAvailable) {
    errors.push("High AI exposure requires a training or transition plan.");
  }

  if (record.monitoringBurden >= 0.60 && !record.workerConsultationComplete) {
    errors.push("High monitoring burden requires worker consultation.");
  }

  if (record.affectsDisciplineOrTermination && !record.appealPathwayAvailable) {
    errors.push("Systems affecting discipline or termination require an appeal pathway.");
  }

  return errors;
}

const example: WorkforceAIRecord = {
  systemName: "workplace-ai-evaluation-system",
  workerConsultationComplete: true,
  trainingPlanAvailable: true,
  appealPathwayAvailable: true,
  meanAIExposure: 0.66,
  monitoringBurden: 0.62,
  affectsDisciplineOrTermination: true
};

console.log(validateRecord(example));
