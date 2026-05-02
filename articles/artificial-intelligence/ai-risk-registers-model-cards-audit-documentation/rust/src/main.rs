// Documentation-priority checker for AI governance.

fn residual_risk(likelihood: f64, impact: f64, mitigation_strength: f64) -> f64 {
    likelihood * impact * (1.0 - mitigation_strength)
}

fn documentation_priority(
    residual_risk: f64,
    documentation_completeness: f64,
    staleness_score: f64,
) -> f64 {
    residual_risk * (1.0 - documentation_completeness) * (1.0 + 0.25 * staleness_score)
}

fn priority_band(score: f64) -> &'static str {
    if score < 0.05 {
        "low"
    } else if score < 0.10 {
        "moderate"
    } else {
        "high"
    }
}

fn main() {
    let risk = residual_risk(0.35, 0.90, 0.45);
    let priority = documentation_priority(risk, 0.60, 1.25);

    println!("Residual risk: {:.3}", risk);
    println!("Documentation priority: {:.3}", priority);
    println!("Priority band: {}", priority_band(priority));
}
