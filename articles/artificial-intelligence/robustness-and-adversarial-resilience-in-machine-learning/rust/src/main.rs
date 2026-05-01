use std::env;
use std::fs;
use std::path::Path;

#[derive(Debug)]
struct RobustnessRecord {
    eval_id: String,
    clean_performance: f64,
    adversarial_performance: f64,
    attack_success_rate: f64,
    containment_score: f64,
    recovery_score: f64,
    incident_severity: i32,
    review_required: bool,
}

fn parse_bool(value: &str) -> bool {
    matches!(value.trim().to_lowercase().as_str(), "true" | "1" | "yes")
}

fn parse_record(line: &str) -> Result<RobustnessRecord, String> {
    let parts: Vec<&str> = line.split(',').collect();

    if parts.len() != 8 {
        return Err(format!("Expected 8 columns, found {}", parts.len()));
    }

    Ok(RobustnessRecord {
        eval_id: parts[0].trim().to_string(),
        clean_performance: parts[1].trim().parse::<f64>().map_err(|_| "Invalid clean_performance".to_string())?,
        adversarial_performance: parts[2].trim().parse::<f64>().map_err(|_| "Invalid adversarial_performance".to_string())?,
        attack_success_rate: parts[3].trim().parse::<f64>().map_err(|_| "Invalid attack_success_rate".to_string())?,
        containment_score: parts[4].trim().parse::<f64>().map_err(|_| "Invalid containment_score".to_string())?,
        recovery_score: parts[5].trim().parse::<f64>().map_err(|_| "Invalid recovery_score".to_string())?,
        incident_severity: parts[6].trim().parse::<i32>().map_err(|_| "Invalid incident_severity".to_string())?,
        review_required: parse_bool(parts[7]),
    })
}

fn in_unit_interval(value: f64) -> bool {
    value >= 0.0 && value <= 1.0
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let default_path = "../data/sample_robustness_records.csv".to_string();
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
                let adversarial_drop = record.clean_performance - record.adversarial_performance;

                let should_review =
                    adversarial_drop > 0.22
                    || record.attack_success_rate > 0.30
                    || record.containment_score < 0.65
                    || record.recovery_score < 0.60
                    || record.incident_severity >= 4;

                if should_review {
                    expected_review += 1;
                }

                let scores = [
                    record.clean_performance,
                    record.adversarial_performance,
                    record.attack_success_rate,
                    record.containment_score,
                    record.recovery_score,
                ];

                if scores.iter().any(|value| !in_unit_interval(*value)) {
                    println!("FAIL: {} has score outside [0,1]", record.eval_id);
                }

                if should_review && !record.review_required {
                    println!("FAIL: {} should be flagged for adversarial resilience review", record.eval_id);
                }
            }
            Err(error) => {
                println!("Line {} parse error: {}", index + 1, error);
                expected_review += 1;
            }
        }
    }

    println!("Adversarial resilience validation summary");
    println!("Total records: {}", total);
    println!("Records expected to require review: {}", expected_review);

    if expected_review > 0 {
        std::process::exit(1);
    }
}
