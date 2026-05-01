use std::env;
use std::fs;
use std::path::Path;

#[derive(Debug)]
struct MonitoringRecord {
    batch_id: String,
    max_feature_psi: f64,
    prediction_psi: f64,
    accuracy: f64,
    latency_ms: f64,
    incident_count: i32,
    review_required: bool,
}

fn parse_bool(value: &str) -> bool {
    matches!(value.trim().to_lowercase().as_str(), "true" | "1" | "yes")
}

fn parse_record(line: &str) -> Result<MonitoringRecord, String> {
    let parts: Vec<&str> = line.split(',').collect();

    if parts.len() != 7 {
        return Err(format!("Expected 7 columns, found {}", parts.len()));
    }

    Ok(MonitoringRecord {
        batch_id: parts[0].trim().to_string(),
        max_feature_psi: parts[1].trim().parse::<f64>().map_err(|_| "Invalid max_feature_psi".to_string())?,
        prediction_psi: parts[2].trim().parse::<f64>().map_err(|_| "Invalid prediction_psi".to_string())?,
        accuracy: parts[3].trim().parse::<f64>().map_err(|_| "Invalid accuracy".to_string())?,
        latency_ms: parts[4].trim().parse::<f64>().map_err(|_| "Invalid latency_ms".to_string())?,
        incident_count: parts[5].trim().parse::<i32>().map_err(|_| "Invalid incident_count".to_string())?,
        review_required: parse_bool(parts[6]),
    })
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let default_path = "../data/sample_monitoring_records.csv".to_string();
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
                let should_review =
                    record.max_feature_psi > 0.25
                    || record.prediction_psi > 0.25
                    || record.accuracy < 0.78
                    || record.latency_ms > 1200.0
                    || record.incident_count >= 2;

                if should_review {
                    expected_review += 1;
                }

                if should_review && !record.review_required {
                    println!("FAIL: {} should be flagged for review", record.batch_id);
                }

                if record.max_feature_psi < 0.0 || record.prediction_psi < 0.0 {
                    println!("FAIL: {} has negative drift score", record.batch_id);
                }

                if record.accuracy < 0.0 || record.accuracy > 1.0 {
                    println!("FAIL: {} has accuracy outside [0,1]", record.batch_id);
                }
            }
            Err(error) => {
                println!("Line {} parse error: {}", index + 1, error);
                expected_review += 1;
            }
        }
    }

    println!("AI observability validation summary");
    println!("Total records: {}", total);
    println!("Records expected to require review: {}", expected_review);

    if expected_review > 0 {
        std::process::exit(1);
    }
}
