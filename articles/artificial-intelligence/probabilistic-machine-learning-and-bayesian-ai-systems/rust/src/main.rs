use std::env;
use std::fs;
use std::path::Path;

#[derive(Debug)]
struct ForecastRecord {
    case_id: String,
    predicted_probability: f64,
    outcome: i32,
    evidence_quality: f64,
    review_required: bool,
}

fn parse_bool(value: &str) -> bool {
    matches!(value.trim().to_lowercase().as_str(), "true" | "1" | "yes")
}

fn parse_record(line: &str) -> Result<ForecastRecord, String> {
    let parts: Vec<&str> = line.split(',').collect();

    if parts.len() != 5 {
        return Err(format!("Expected 5 columns, found {}", parts.len()));
    }

    Ok(ForecastRecord {
        case_id: parts[0].trim().to_string(),
        predicted_probability: parts[1].trim().parse::<f64>().map_err(|_| "Invalid predicted_probability".to_string())?,
        outcome: parts[2].trim().parse::<i32>().map_err(|_| "Invalid outcome".to_string())?,
        evidence_quality: parts[3].trim().parse::<f64>().map_err(|_| "Invalid evidence_quality".to_string())?,
        review_required: parse_bool(parts[4]),
    })
}

fn in_unit_interval(value: f64) -> bool {
    value >= 0.0 && value <= 1.0
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let default_path = "../data/sample_probabilistic_forecasts.csv".to_string();
    let file_path = args.get(1).unwrap_or(&default_path);

    let content = fs::read_to_string(Path::new(file_path)).unwrap_or_else(|error| {
        panic!("Could not read file '{}': {}", file_path, error);
    });

    let mut total = 0;
    let mut review = 0;

    for (index, line) in content.lines().enumerate() {
        if index == 0 || line.trim().is_empty() {
            continue;
        }

        total += 1;

        match parse_record(line) {
            Ok(record) => {
                let mut needs_review = false;

                if !in_unit_interval(record.predicted_probability) {
                    println!("FAIL: {} probability outside [0,1]", record.case_id);
                    needs_review = true;
                }

                if !in_unit_interval(record.evidence_quality) {
                    println!("FAIL: {} evidence quality outside [0,1]", record.case_id);
                    needs_review = true;
                }

                if record.outcome != 0 && record.outcome != 1 {
                    println!("FAIL: {} outcome must be 0 or 1", record.case_id);
                    needs_review = true;
                }

                if record.predicted_probability > 0.25 || record.evidence_quality < 0.50 {
                    needs_review = true;
                }

                if needs_review && !record.review_required {
                    println!("FAIL: {} should be flagged for review", record.case_id);
                }

                if needs_review {
                    review += 1;
                }
            }
            Err(error) => {
                println!("Line {} parse error: {}", index + 1, error);
                review += 1;
            }
        }
    }

    println!("Probabilistic forecast validation summary");
    println!("Total records: {}", total);
    println!("Records requiring review: {}", review);

    if review > 0 {
        std::process::exit(1);
    }
}
