// Information-integrity risk checker.

fn information_integrity_risk(
    claim_uncertainty: f64,
    amplification_risk: f64,
    public_impact: f64,
    provenance_gap: f64,
    verification_strength: f64,
    correction_gap: f64,
    human_review_gap: f64,
) -> f64 {
    0.22 * claim_uncertainty
        + 0.18 * amplification_risk
        + 0.18 * public_impact
        + 0.18 * provenance_gap
        + 0.14 * (1.0 - verification_strength)
        + 0.05 * correction_gap
        + 0.05 * human_review_gap
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

fn review_required(score: f64, provenance_gap: f64, public_impact: f64) -> bool {
    score >= 0.50 || (provenance_gap > 0.0 && public_impact >= 0.80)
}

fn main() {
    let risk = information_integrity_risk(0.75, 0.92, 0.85, 1.0, 0.25, 1.0, 1.0);

    println!("Information integrity risk: {:.3}", risk);
    println!("Risk band: {}", risk_band(risk));
    println!("Review required: {}", review_required(risk, 1.0, 0.85));
}
