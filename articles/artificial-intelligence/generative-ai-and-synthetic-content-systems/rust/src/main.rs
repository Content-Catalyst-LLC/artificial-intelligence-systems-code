use std::env;
use std::fs;
use std::path::Path;

#[derive(Debug)]
struct ContentRecord {
    artifact_id: String,
    grounding_score: f64,
    provenance_score: f64,
    policy_risk: f64,
    human_review_completed: bool,
}

fn parse_bool(value: &str) -> bool {
    matches!(value.trim().to_lowercase().as_str(), "true" | "1" | "yes")
}

fn parse_record(line: &str) -> Result<ContentRecord, String> {
    let parts: Vec<&str> = line.split(',').collect();

    if parts.len() != 5 {
        return Err(format!("Expected 5 columns, found {}", parts.len()));
    }

    Ok(ContentRecord {
        artifact_id: parts[0].trim().to_string(),
        grounding_score: parts[1].trim().parse::<f64>().map_err(|_| "Invalid grounding_score".to_string())?,
        provenance_score: parts[2].trim().parse::<f64>().map_err(|_| "Invalid provenance_score".to_string())?,
        policy_risk: parts[3].trim().parse::<f64>().map_err(|_| "Invalid policy_risk".to_string())?,
        human_review_completed: parse_bool(parts[4]),
    })
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let default_path = "../data/sample_synthetic_content_records.csv".to_string();
    let file_path = args.get(1).unwrap_or(&default_path);

    let content = fs::read_to_string(Path::new(file_path)).unwrap_or_else(|error| {
        panic!("Could not read file '{}': {}", file_path, error);
    });

    let mut total = 0;
    let mut failed = 0;

    for (index, line) in content.lines().enumerate() {
        if index == 0 || line.trim().is_empty() {
            continue;
        }

        total += 1;

        match parse_record(line) {
            Ok(record) => {
                let mut needs_review = false;

                if !(0.0..=1.0).contains(&record.grounding_score)
                    || !(0.0..=1.0).contains(&record.provenance_score)
                    || !(0.0..=1.0).contains(&record.policy_risk)
                {
                    println!("FAIL: {} has score outside [0,1]", record.artifact_id);
                    needs_review = true;
                }

                if record.policy_risk > 0.45 && !record.human_review_completed {
                    println!("FAIL: {} high risk without completed human review", record.artifact_id);
                    needs_review = true;
                }

                if record.grounding_score < 0.50 {
                    println!("WARN: {} low grounding score", record.artifact_id);
                    needs_review = true;
                }

                if record.provenance_score < 0.45 {
                    println!("WARN: {} low provenance score", record.artifact_id);
                    needs_review = true;
                }

                if needs_review {
                    failed += 1;
                }
            }
            Err(error) => {
                println!("Line {} parse error: {}", index + 1, error);
                failed += 1;
            }
        }
    }

    println!("Synthetic content validation summary");
    println!("Total records: {}", total);
    println!("Records requiring review: {}", failed);

    if failed > 0 {
        std::process::exit(1);
    }
}
