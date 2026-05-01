use std::env;
use std::fs;
use std::path::Path;

#[derive(Debug)]
struct PlanningRecord {
    record_id: String,
    plan_cost: f64,
    uncertainty_risk: f64,
    constraint_violation_risk: f64,
    irreversibility_risk: f64,
    governance_readiness: f64,
    review_required: bool,
}

fn parse_bool(value: &str) -> bool {
    matches!(value.trim().to_lowercase().as_str(), "true" | "1" | "yes")
}

fn parse_record(line: &str) -> Result<PlanningRecord, String> {
    let parts: Vec<&str> = line.split(',').collect();

    if parts.len() != 7 {
        return Err(format!("Expected 7 columns, found {}", parts.len()));
    }

    Ok(PlanningRecord {
        record_id: parts[0].trim().to_string(),
        plan_cost: parts[1].trim().parse::<f64>().map_err(|_| "Invalid plan_cost".to_string())?,
        uncertainty_risk: parts[2].trim().parse::<f64>().map_err(|_| "Invalid uncertainty_risk".to_string())?,
        constraint_violation_risk: parts[3].trim().parse::<f64>().map_err(|_| "Invalid constraint_violation_risk".to_string())?,
        irreversibility_risk: parts[4].trim().parse::<f64>().map_err(|_| "Invalid irreversibility_risk".to_string())?,
        governance_readiness: parts[5].trim().parse::<f64>().map_err(|_| "Invalid governance_readiness".to_string())?,
        review_required: parse_bool(parts[6]),
    })
}

fn in_unit_interval(value: f64) -> bool {
    value >= 0.0 && value <= 1.0
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let default_path = "../data/sample_planning_records.csv".to_string();
    let file_path = args.get(1).unwrap_or(&default_path);

    let content = fs::read_to_string(Path::new(file_path)).unwrap_or_else(|error| {
        panic!("Could not read file '{}': {}", file_path, error);
    });

    let mut total = 0;
    let mut expected_review = 0;

    for (index, line) in content.lines().enumerate() {
        if index == 0 || line.trim().is_empty() {
            continue;
        }

        total += 1;

        match parse_record(line) {
            Ok(record) => {
                let values = [
                    record.plan_cost,
                    record.uncertainty_risk,
                    record.constraint_violation_risk,
                    record.irreversibility_risk,
                    record.governance_readiness,
                ];

                if values.iter().any(|value| !in_unit_interval(*value)) {
                    println!("FAIL: {} has metric outside [0,1]", record.record_id);
                }

                let planning_risk =
                    0.30 * record.plan_cost
                    + 0.25 * record.uncertainty_risk
                    + 0.25 * record.constraint_violation_risk
                    + 0.20 * record.irreversibility_risk;

                let should_review =
                    planning_risk > 0.28
                    || record.constraint_violation_risk > 0.20
                    || record.irreversibility_risk > 0.15
                    || record.uncertainty_risk > 0.45
                    || record.governance_readiness < 0.65;

                if should_review {
                    expected_review += 1;
                }

                if should_review && !record.review_required {
                    println!("FAIL: {} should be flagged for planning review", record.record_id);
                }
            }
            Err(error) => {
                println!("Line {} parse error: {}", index + 1, error);
                expected_review += 1;
            }
        }
    }

    println!("Planning validation summary");
    println!("Total records: {}", total);
    println!("Records expected to require review: {}", expected_review);

    if expected_review > 0 {
        std::process::exit(1);
    }
}
