use std::env;
use std::fs;
use std::path::Path;

#[derive(Debug)]
struct DecisionRecord {
    option_id: String,
    predicted_risk: f64,
    uncertainty: f64,
    expected_utility: f64,
    human_review_required: bool,
}

fn parse_bool(value: &str) -> bool {
    matches!(value.trim().to_lowercase().as_str(), "true" | "1" | "yes")
}

fn parse_record(line: &str) -> Result<DecisionRecord, String> {
    let parts: Vec<&str> = line.split(',').collect();

    if parts.len() != 5 {
        return Err(format!("Expected 5 columns, found {}", parts.len()));
    }

    Ok(DecisionRecord {
        option_id: parts[0].trim().to_string(),
        predicted_risk: parts[1].trim().parse::<f64>().map_err(|_| "Invalid predicted_risk".to_string())?,
        uncertainty: parts[2].trim().parse::<f64>().map_err(|_| "Invalid uncertainty".to_string())?,
        expected_utility: parts[3].trim().parse::<f64>().map_err(|_| "Invalid expected_utility".to_string())?,
        human_review_required: parse_bool(parts[4]),
    })
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let default_path = "../data/sample_decision_records.csv".to_string();
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

                if !(0.0..=1.0).contains(&record.predicted_risk) {
                    println!("FAIL: {} predicted risk outside [0,1]", record.option_id);
                    needs_review = true;
                }

                if record.uncertainty > 0.30 && !record.human_review_required {
                    println!("FAIL: {} high uncertainty but no human review flag", record.option_id);
                    needs_review = true;
                }

                if !record.expected_utility.is_finite() {
                    println!("FAIL: {} invalid utility value", record.option_id);
                    needs_review = true;
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

    println!("Decision record validation summary");
    println!("Total records: {}", total);
    println!("Records requiring review: {}", review);

    if review > 0 {
        std::process::exit(1);
    }
}
