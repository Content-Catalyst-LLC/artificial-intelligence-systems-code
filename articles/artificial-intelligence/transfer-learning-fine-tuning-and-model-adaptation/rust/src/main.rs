use std::env;
use std::fs;
use std::path::Path;

#[derive(Debug)]
struct AdaptationRecord {
    run_id: String,
    method: String,
    transfer_gain: f64,
    retention_score: f64,
    sensitive_domain: bool,
}

fn parse_bool(value: &str) -> bool {
    matches!(value.trim().to_lowercase().as_str(), "true" | "1" | "yes")
}

fn parse_record(line: &str) -> Result<AdaptationRecord, String> {
    let parts: Vec<&str> = line.split(',').collect();

    if parts.len() != 5 {
        return Err(format!("Expected 5 columns, found {}", parts.len()));
    }

    Ok(AdaptationRecord {
        run_id: parts[0].trim().to_string(),
        method: parts[1].trim().to_string(),
        transfer_gain: parts[2].trim().parse::<f64>().map_err(|_| "Invalid transfer_gain".to_string())?,
        retention_score: parts[3].trim().parse::<f64>().map_err(|_| "Invalid retention_score".to_string())?,
        sensitive_domain: parse_bool(parts[4]),
    })
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let default_path = "../data/sample_adaptation_records.csv".to_string();
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

                if record.transfer_gain < 0.0 {
                    println!("FAIL: {} has negative transfer", record.run_id);
                    needs_review = true;
                }

                if record.retention_score < 0.80 {
                    println!("FAIL: {} has low source capability retention", record.run_id);
                    needs_review = true;
                }

                if record.sensitive_domain {
                    println!("WARN: {} is sensitive-domain adaptation and requires approval", record.run_id);
                    needs_review = true;
                }

                if ![
                    "base_model_zero_shot",
                    "linear_head_only",
                    "full_fine_tuning",
                    "regularized_fine_tuning",
                    "adapter_tuning",
                    "lora",
                    "qlora",
                ].contains(&record.method.as_str()) {
                    println!("FAIL: {} uses unsupported adaptation method", record.run_id);
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

    println!("Adaptation metadata validation summary");
    println!("Total records: {}", total);
    println!("Records requiring review: {}", review);

    if review > 0 {
        std::process::exit(1);
    }
}
