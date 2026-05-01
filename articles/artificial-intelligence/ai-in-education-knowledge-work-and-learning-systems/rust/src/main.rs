use std::env;
use std::fs;
use std::path::Path;

#[derive(Debug)]
struct LearningAiRecord {
    record_id: String,
    learning_gain: f64,
    independent_transfer: f64,
    assistance_gap: f64,
    feedback_quality: f64,
    privacy_risk: f64,
    review_required: bool,
}

fn parse_bool(value: &str) -> bool {
    matches!(value.trim().to_lowercase().as_str(), "true" | "1" | "yes")
}

fn parse_record(line: &str) -> Result<LearningAiRecord, String> {
    let parts: Vec<&str> = line.split(',').collect();

    if parts.len() != 7 {
        return Err(format!("Expected 7 columns, found {}", parts.len()));
    }

    Ok(LearningAiRecord {
        record_id: parts[0].trim().to_string(),
        learning_gain: parts[1].trim().parse::<f64>().map_err(|_| "Invalid learning_gain".to_string())?,
        independent_transfer: parts[2].trim().parse::<f64>().map_err(|_| "Invalid independent_transfer".to_string())?,
        assistance_gap: parts[3].trim().parse::<f64>().map_err(|_| "Invalid assistance_gap".to_string())?,
        feedback_quality: parts[4].trim().parse::<f64>().map_err(|_| "Invalid feedback_quality".to_string())?,
        privacy_risk: parts[5].trim().parse::<f64>().map_err(|_| "Invalid privacy_risk".to_string())?,
        review_required: parse_bool(parts[6]),
    })
}

fn in_expected_range(value: f64, lower: f64, upper: f64) -> bool {
    value >= lower && value <= upper
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let default_path = "../data/sample_learning_ai_monitoring_records.csv".to_string();
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
                if !in_expected_range(record.learning_gain, -1.0, 1.0)
                    || !in_expected_range(record.independent_transfer, 0.0, 1.0)
                    || !in_expected_range(record.assistance_gap, -1.0, 1.0)
                    || !in_expected_range(record.feedback_quality, 0.0, 1.0)
                    || !in_expected_range(record.privacy_risk, 0.0, 1.0)
                {
                    println!("FAIL: {} has metric outside expected range", record.record_id);
                }

                let should_review =
                    record.learning_gain < 0.03
                    || record.independent_transfer < 0.50
                    || record.assistance_gap > 0.20
                    || record.feedback_quality < 0.40
                    || record.privacy_risk > 0.45;

                if should_review {
                    expected_review += 1;
                }

                if should_review && !record.review_required {
                    println!("FAIL: {} should be flagged for learning-system review", record.record_id);
                }
            }
            Err(error) => {
                println!("Line {} parse error: {}", index + 1, error);
                expected_review += 1;
            }
        }
    }

    println!("Learning AI validation summary");
    println!("Total records: {}", total);
    println!("Records expected to require review: {}", expected_review);

    if expected_review > 0 {
        std::process::exit(1);
    }
}
