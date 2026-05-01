use std::env;
use std::fs;
use std::path::Path;

#[derive(Debug)]
struct ExplanationRecord {
    explanation_id: String,
    stability_score: f64,
    fidelity_score: f64,
    method_name: String,
    causal_review_required: bool,
}

fn parse_bool(value: &str) -> bool {
    matches!(value.trim().to_lowercase().as_str(), "true" | "1" | "yes")
}

fn parse_record(line: &str) -> Result<ExplanationRecord, String> {
    let parts: Vec<&str> = line.split(',').collect();

    if parts.len() != 5 {
        return Err(format!("Expected 5 columns, found {}", parts.len()));
    }

    let stability_score = parts[1]
        .trim()
        .parse::<f64>()
        .map_err(|_| "Invalid stability score".to_string())?;

    let fidelity_score = parts[2]
        .trim()
        .parse::<f64>()
        .map_err(|_| "Invalid fidelity score".to_string())?;

    Ok(ExplanationRecord {
        explanation_id: parts[0].trim().to_string(),
        stability_score,
        fidelity_score,
        method_name: parts[3].trim().to_string(),
        causal_review_required: parse_bool(parts[4]),
    })
}

fn main() {
    let args: Vec<String> = env::args().collect();

    let default_path = "../data/sample_explanation_audit.csv".to_string();
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
                let pass = record.stability_score >= 0.70 && record.fidelity_score >= 0.80;

                if !pass {
                    failed += 1;
                    println!(
                        "FAIL: {} method={} stability={:.3} fidelity={:.3}",
                        record.explanation_id,
                        record.method_name,
                        record.stability_score,
                        record.fidelity_score
                    );
                }

                if record.causal_review_required {
                    println!("REVIEW: {} requires causal review.", record.explanation_id);
                }
            }
            Err(error) => {
                failed += 1;
                println!("Line {} parse error: {}", index + 1, error);
            }
        }
    }

    println!("Explanation validation summary");
    println!("Total records: {}", total);
    println!("Failed records: {}", failed);

    if failed > 0 {
        std::process::exit(1);
    }
}
