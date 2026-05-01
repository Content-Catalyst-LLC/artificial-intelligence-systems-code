// Defensive residual-risk checker.
// This example does not implement attack techniques.

fn residual_risk(exposure: f64, impact: f64, likelihood: f64, control_strength: f64) -> f64 {
    let inherent_risk = exposure * impact * likelihood;
    inherent_risk * (1.0 - control_strength)
}

fn risk_band(score: f64) -> &'static str {
    if score < 0.10 {
        "low"
    } else if score < 0.20 {
        "moderate"
    } else {
        "high"
    }
}

fn main() {
    let score = residual_risk(0.90, 0.95, 0.70, 0.55);
    println!("Residual risk: {:.3}", score);
    println!("Risk band: {}", risk_band(score));
}
