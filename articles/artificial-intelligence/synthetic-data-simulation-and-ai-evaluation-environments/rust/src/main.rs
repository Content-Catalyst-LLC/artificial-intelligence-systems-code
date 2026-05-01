use std::env;
use std::fs;
use std::path::Path;

#[derive(Debug)]
struct SyntheticEvaluationRecord {
    record_id: String,
    fidelity_risk: f64,
    utility_gap: f64,
    privacy_proximity_risk: f64,
    rare_case_coverage_gap: f64,
    sim_to_real_gap: f64,
    review_required: bool,
}

fn parse_bool(value: &str) -> bool {
    matches!(value.trim().to_lowercase().as_str(), "true" | "1" | "yes")
}

fn parse_record(line: &str) -> Result<SyntheticEvaluationRecord, String> {
    let parts: Vec<&str> = line.split(',').collect();

    if parts.len() != 7 {
        return Err(format!("Expected 7 columns, found {}", parts.len()));
    }

    Ok(SyntheticEvaluationRecord {
        record_id: parts[0].trim().to_string(),
        fidelity_risk: parts[1].trim().parse::<f64>().map_err(|_| "Invalid fidelity_risk".to_string())?,
        utility_gap: parts[2].trim().parse::<f64>().map_err(|_| "Invalid utility_gap".to_string())?,
        privacy_proximity_risk: parts[3].trim().parse::<f64>().map_err(|_| "Invalid privacy_proximity_risk".to_string())?,
        rare_case_coverage_gap: parts[4].trim().parse::<f64>().map_err(|_| "Invalid rare_case_coverage_gap".to_string())?,
        sim_to_real_gap: parts[5].trim().parse::<f64>().map_err(|_| "Invalid sim_to_real_gap".to_string())?,
        review_required: parse_bool(parts[6]),
    })
}

fn in_unit_interval(value: f64) -> bool {
    value >= 0.0 && value <= 1.0
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let default_path = "../data/sample_synthetic_evaluation_records.csv".to_string();
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
                    record.fidelity_risk,
                    record.utility_gap,
                    record.privacy_proximity_risk,
                    record.rare_case_coverage_gap,
                    record.sim_to_real_gap,
                ];

                if values.iter().any(|value| !in_unit_interval(*value)) {
                    println!("FAIL: {} has metric outside [0,1]", record.record_id);
                }

                let should_review =
                    record.fidelity_risk > 0.25
                    || record.utility_gap > 0.05
                    || record.privacy_proximity_risk > 0.05
                    || record.rare_case_coverage_gap > 0.06
                    || record.sim_to_real_gap > 0.18;

                if should_review {
                    expected_review += 1;
                }

                if should_review && !record.review_required {
                    println!("FAIL: {} should be flagged for governance review", record.record_id);
                }
            }
            Err(error) => {
                println!("Line {} parse error: {}", index + 1, error);
                expected_review += 1;
            }
        }
    }

    println!("Synthetic evaluation validation summary");
    println!("Total records: {}", total);
    println!("Records expected to require review: {}", expected_review);

    if expected_review > 0 {
        std::process::exit(1);
    }
}
