use std::env;
use std::fs;
use std::path::Path;

#[derive(Debug)]
struct CalibrationRecord {
    record_id: String,
    mean_confidence: f64,
    observed_rate: f64,
    brier_score: f64,
    nll: f64,
    entropy: f64,
    review_required: bool,
}

fn parse_bool(value: &str) -> bool {
    matches!(value.trim().to_lowercase().as_str(), "true" | "1" | "yes")
}

fn parse_record(line: &str) -> Result<CalibrationRecord, String> {
    let parts: Vec<&str> = line.split(',').collect();

    if parts.len() != 7 {
        return Err(format!("Expected 7 columns, found {}", parts.len()));
    }

    Ok(CalibrationRecord {
        record_id: parts[0].trim().to_string(),
        mean_confidence: parts[1].trim().parse::<f64>().map_err(|_| "Invalid mean_confidence".to_string())?,
        observed_rate: parts[2].trim().parse::<f64>().map_err(|_| "Invalid observed_rate".to_string())?,
        brier_score: parts[3].trim().parse::<f64>().map_err(|_| "Invalid brier_score".to_string())?,
        nll: parts[4].trim().parse::<f64>().map_err(|_| "Invalid nll".to_string())?,
        entropy: parts[5].trim().parse::<f64>().map_err(|_| "Invalid entropy".to_string())?,
        review_required: parse_bool(parts[6]),
    })
}

fn in_unit_interval(value: f64) -> bool {
    value >= 0.0 && value <= 1.0
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let default_path = "../data/sample_calibration_records.csv".to_string();
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
                let calibration_gap = (record.mean_confidence - record.observed_rate).abs();

                let should_review =
                    calibration_gap > 0.08
                    || record.brier_score > 0.22
                    || record.nll > 0.70
                    || record.entropy > 0.62;

                if should_review {
                    expected_review += 1;
                }

                let bounded_scores = [
                    record.mean_confidence,
                    record.observed_rate,
                    record.brier_score,
                    record.entropy,
                ];

                if bounded_scores.iter().any(|value| !in_unit_interval(*value)) {
                    println!("FAIL: {} has bounded score outside [0,1]", record.record_id);
                }

                if record.nll < 0.0 {
                    println!("FAIL: {} has negative NLL", record.record_id);
                }

                if should_review && !record.review_required {
                    println!("FAIL: {} should be flagged for calibration review", record.record_id);
                }
            }
            Err(error) => {
                println!("Line {} parse error: {}", index + 1, error);
                expected_review += 1;
            }
        }
    }

    println!("Calibration validation summary");
    println!("Total records: {}", total);
    println!("Records expected to require review: {}", expected_review);

    if expected_review > 0 {
        std::process::exit(1);
    }
}
