// Residual ethical-risk checker for rights-based AI governance.

fn residual_rights_risk(
    harm_probability: f64,
    harm_impact: f64,
    vulnerability_exposure: f64,
    institutional_power: f64,
    governance_control_strength: f64,
) -> f64 {
    let inherent = 0.30 * harm_probability
        + 0.30 * harm_impact
        + 0.20 * vulnerability_exposure
        + 0.20 * institutional_power;

    inherent * (1.0 - governance_control_strength)
}

fn risk_band(score: f64) -> &'static str {
    if score < 0.20 {
        "low"
    } else if score < 0.35 {
        "moderate"
    } else {
        "high"
    }
}

fn main() {
    let score = residual_rights_risk(0.35, 0.90, 0.90, 0.95, 0.45);
    println!("Residual rights risk: {:.3}", score);
    println!("Risk band: {}", risk_band(score));
}
