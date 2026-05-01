use std::env;
use std::fs;
use std::path::Path;

#[derive(Debug)]
struct FoundationModelRecord {
    run_id: String,
    provenance_score: f64,
    privacy_risk: f64,
    bias_risk: f64,
    governance_readiness: f64,
    broad_reuse: bool,
}

fn parse_bool(value: &str) -> bool {
    matches!(value.trim().to_lowercase().as_str(), "true" | "1" | "yes")
}

fn parse_record(line: &str) -> Result<FoundationModelRecord, String> {
    let parts: Vec<&str> = line.split(',').collect();

    if parts.len() != 6 {
        return Err(format!("Expected 6 columns, found {}", parts.len()));
    }

    Ok(FoundationModelRecord {
        run_id: parts[0].trim().to_string(),
        provenance_score: parts[1].trim().parse::<f64>().map_err(|_| "Invalid provenance_score".to_string())?,
        privacy_risk: parts[2].trim().parse::<f64>().map_err(|_| "Invalid privacy_risk".to_string())?,
        bias_risk: parts[3].trim().parse::<f64>().map_err(|_| "Invalid bias_risk".to_string())?,
        governance_readiness: parts[4].trim().parse::<f64>().map_err(|_| "Invalid governance_readiness".to_string())?,
        broad_reuse: parse_bool(parts[5]),
    })
}

fn in_unit_interval(value: f64) -> bool {
    value >= 0.0 && value <= 1.0
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let default_path = "../data/sample_foundation_model_records.csv".to_string();
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

                if !in_unit_interval(record.provenance_score)
                    || !in_unit_interval(record.privacy_risk)
                    || !in_unit_interval(record.bias_risk)
                    || !in_unit_interval(record.governance_readiness)
                {
                    println!("FAIL: {} has score outside [0,1]", record.run_id);
                    needs_review = true;
                }

                if record.provenance_score < 0.50 {
                    println!("FAIL: {} has weak data provenance", record.run_id);
                    needs_review = true;
                }

                if record.privacy_risk > 0.45 {
                    println!("FAIL: {} has high privacy risk", record.run_id);
                    needs_review = true;
                }

                if record.bias_risk > 0.45 {
                    println!("WARN: {} has elevated bias risk", record.run_id);
                    needs_review = true;
                }

                if record.broad_reuse && record.governance_readiness < 0.65 {
                    println!("FAIL: {} has broad reuse but weak governance readiness", record.run_id);
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

    println!("Foundation model metadata validation summary");
    println!("Total records: {}", total);
    println!("Records requiring review: {}", review);

    if review > 0 {
        std::process::exit(1);
    }
}
