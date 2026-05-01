// Information-integrity risk checker.

fn information_integrity_risk(
    claim_uncertainty: f64,
    amplification_risk: f64,
    public_impact: f64,
    provenance_gap: f64,
    verification_strength: f64,
) -> f64 {
    0.25 * claim_uncertainty
        + 0.20 * amplification_risk
        + 0.20 * public_impact
        + 0.20 * provenance_gap
        + 0.15 * (1.0 - verification_strength)
}

fn risk_band(score: f64) -> &'static str {
    if score < 0.30 {
        "low"
    } else if score < 0.50 {
        "moderate"
    } else {
        "high"
    }
}

fn main() {
    let risk = information_integrity_risk(0.75, 0.92, 0.85, 1.0, 0.25);

    println!("Information integrity risk: {:.3}", risk);
    println!("Risk band: {}", risk_band(risk));
}
