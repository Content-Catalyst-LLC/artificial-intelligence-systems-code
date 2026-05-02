fn automation_bias_flag(observed_reliance: f64, warranted_reliance: f64) -> bool {
    observed_reliance > warranted_reliance + 0.15
}

fn review_required(
    context_complexity: f64,
    ai_expert_disagreement: f64,
    observed_reliance: f64,
    warranted_reliance: f64,
) -> bool {
    context_complexity > 0.70
        || ai_expert_disagreement > 0.30
        || automation_bias_flag(observed_reliance, warranted_reliance)
}

fn main() {
    let observed_reliance = 0.82;
    let warranted_reliance = 0.60;
    let context_complexity = 0.74;
    let ai_expert_disagreement = 0.22;

    let bias_flag = automation_bias_flag(observed_reliance, warranted_reliance);
    let review_flag = review_required(
        context_complexity,
        ai_expert_disagreement,
        observed_reliance,
        warranted_reliance,
    );

    println!("Automation bias flag: {}", bias_flag);
    println!("Review required: {}", review_flag);
}
