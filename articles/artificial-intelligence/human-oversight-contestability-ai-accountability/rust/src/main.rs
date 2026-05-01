fn should_escalate(
    expected_risk: f64,
    uncertainty: f64,
    rights_sensitive: bool,
    vulnerable_context: bool,
    risk_threshold: f64,
    uncertainty_threshold: f64,
) -> bool {
    expected_risk >= risk_threshold
        || uncertainty >= uncertainty_threshold
        || rights_sensitive
        || vulnerable_context
}

fn main() {
    let expected_risk = 0.22;
    let uncertainty = 0.41;
    let rights_sensitive = false;
    let vulnerable_context = true;

    let escalate = should_escalate(
        expected_risk,
        uncertainty,
        rights_sensitive,
        vulnerable_context,
        0.18,
        0.55,
    );

    println!("Escalate to human review: {}", escalate);
}
