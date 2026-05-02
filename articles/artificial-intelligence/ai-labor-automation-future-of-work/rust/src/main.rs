// Task-redesign classifier for workplace AI governance.

fn automation_pressure(ai_capability: f64, routineness: f64, human_judgment: f64) -> f64 {
    ai_capability * routineness * (1.0 - human_judgment)
}

fn augmentation_potential(ai_capability: f64, human_judgment: f64, task_value: f64) -> f64 {
    ai_capability * human_judgment * task_value
}

fn deskilling_risk(ai_capability: f64, training_function: f64, human_judgment: f64) -> f64 {
    ai_capability * training_function * (1.0 - human_judgment)
}

fn classify_task(automation: f64, augmentation: f64, human_judgment: f64) -> &'static str {
    if automation > 0.35 && human_judgment < 0.40 {
        "candidate_for_careful_automation"
    } else if augmentation > 0.35 {
        "candidate_for_augmentation"
    } else if human_judgment > 0.80 {
        "protect_human_judgment"
    } else {
        "redesign_with_monitoring"
    }
}

fn main() {
    let ai_capability = 0.85;
    let routineness = 0.70;
    let human_judgment = 0.35;
    let task_value = 0.65;
    let training_function = 0.40;

    let automation = automation_pressure(ai_capability, routineness, human_judgment);
    let augmentation = augmentation_potential(ai_capability, human_judgment, task_value);
    let deskilling = deskilling_risk(ai_capability, training_function, human_judgment);
    let category = classify_task(automation, augmentation, human_judgment);

    println!("Automation pressure: {:.3}", automation);
    println!("Augmentation potential: {:.3}", augmentation);
    println!("Deskilling risk: {:.3}", deskilling);
    println!("Redesign category: {}", category);
}
