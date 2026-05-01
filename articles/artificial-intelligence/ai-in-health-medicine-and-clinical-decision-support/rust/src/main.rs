use std::env;
use std::fs;
use std::path::Path;

#[derive(Debug)]
struct ClinicalAiRecord {
    record_id: String,
    sensitivity: f64,
    specificity: f64,
    calibration_error: f64,
    alert_rate: f64,
    false_negative_rate: f64,
    review_required: bool,
}

fn parse_bool(value: &str) -> bool {
    matches!(value.trim().to_lowercase().as_str(), "true" | "1" | "yes")
}

fn parse_record(line: &str) -> Result<ClinicalAiRecord, String> {
    let parts: Vec<&str> = line.split(',').collect();

    if parts.len() != 7 {
        return Err(format!("Expected 7 columns, found {}", parts.len()));
    }

    Ok(ClinicalAiRecord {
        record_id: parts[0].trim().to_string(),
        sensitivity: parts[1].trim().parse::<f64>().map_err(|_| "Invalid sensitivity".to_string())?,
        specificity: parts[2].trim().parse::<f64>().map_err(|_| "Invalid specificity".to_string())?,
        calibration_error: parts[3].trim().parse::<f64>().map_err(|_| "Invalid calibration_error".to_string())?,
        alert_rate: parts[4].trim().parse::<f64>().map_err(|_| "Invalid alert_rate".to_string())?,
        false_negative_rate: parts[5].trim().parse::<f64>().map_err(|_| "Invalid false_negative_rate".to_string())?,
        review_required: parse_bool(parts[6]),
    })
}

fn in_unit_interval(value: f64) -> bool {
    value >= 0.0 && value <= 1.0
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let default_path = "../data/sample_clinical_ai_monitoring_records.csv".to_string();
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
                    record.sensitivity,
                    record.specificity,
                    record.calibration_error,
                    record.alert_rate,
                    record.false_negative_rate,
                ];

                if values.iter().any(|value| !in_unit_interval(*value)) {
                    println!("FAIL: {} has metric outside [0,1]", record.record_id);
                }

                let should_review =
                    record.sensitivity < 0.70
                    || record.specificity < 0.60
                    || record.calibration_error > 0.08
                    || record.alert_rate > 0.45
                    || record.false_negative_rate > 0.20;

                if should_review {
                    expected_review += 1;
                }

                if should_review && !record.review_required {
                    println!("FAIL: {} should be flagged for clinical AI review", record.record_id);
                }
            }
            Err(error) => {
                println!("Line {} parse error: {}", index + 1, error);
                expected_review += 1;
            }
        }
    }

    println!("Clinical AI validation summary");
    println!("Total records: {}", total);
    println!("Records expected to require review: {}", expected_review);

    if expected_review > 0 {
        std::process::exit(1);
    }
}
