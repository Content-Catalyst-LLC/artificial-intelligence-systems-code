use std::env;
use std::fs;
use std::path::Path;

#[derive(Debug)]
struct RagEvaluationRecord {
    eval_id: String,
    grounding_score: f64,
    citation_fidelity: f64,
    source_authority: f64,
    freshness_score: f64,
    access_control_score: f64,
    unknown_answer: bool,
    abstained: bool,
}

fn parse_bool(value: &str) -> bool {
    matches!(value.trim().to_lowercase().as_str(), "true" | "1" | "yes")
}

fn parse_record(line: &str) -> Result<RagEvaluationRecord, String> {
    let parts: Vec<&str> = line.split(',').collect();

    if parts.len() != 8 {
        return Err(format!("Expected 8 columns, found {}", parts.len()));
    }

    Ok(RagEvaluationRecord {
        eval_id: parts[0].trim().to_string(),
        grounding_score: parts[1].trim().parse::<f64>().map_err(|_| "Invalid grounding_score".to_string())?,
        citation_fidelity: parts[2].trim().parse::<f64>().map_err(|_| "Invalid citation_fidelity".to_string())?,
        source_authority: parts[3].trim().parse::<f64>().map_err(|_| "Invalid source_authority".to_string())?,
        freshness_score: parts[4].trim().parse::<f64>().map_err(|_| "Invalid freshness_score".to_string())?,
        access_control_score: parts[5].trim().parse::<f64>().map_err(|_| "Invalid access_control_score".to_string())?,
        unknown_answer: parse_bool(parts[6]),
        abstained: parse_bool(parts[7]),
    })
}

fn in_unit_interval(value: f64) -> bool {
    value >= 0.0 && value <= 1.0
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let default_path = "../data/sample_rag_evaluation_records.csv".to_string();
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

                if !in_unit_interval(record.grounding_score)
                    || !in_unit_interval(record.citation_fidelity)
                    || !in_unit_interval(record.source_authority)
                    || !in_unit_interval(record.freshness_score)
                    || !in_unit_interval(record.access_control_score)
                {
                    println!("FAIL: {} has score outside [0,1]", record.eval_id);
                    needs_review = true;
                }

                if record.grounding_score < 0.60 {
                    println!("FAIL: {} has weak grounding", record.eval_id);
                    needs_review = true;
                }

                if record.citation_fidelity < 0.60 {
                    println!("FAIL: {} has weak citation fidelity", record.eval_id);
                    needs_review = true;
                }

                if record.source_authority < 0.55 {
                    println!("WARN: {} has low source authority", record.eval_id);
                    needs_review = true;
                }

                if record.freshness_score < 0.45 {
                    println!("WARN: {} has stale-source risk", record.eval_id);
                    needs_review = true;
                }

                if record.access_control_score < 0.75 {
                    println!("FAIL: {} has access-control concern", record.eval_id);
                    needs_review = true;
                }

                if record.unknown_answer && !record.abstained {
                    println!("FAIL: {} should have abstained because evidence was absent", record.eval_id);
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

    println!("RAG evaluation validation summary");
    println!("Total records: {}", total);
    println!("Records requiring review: {}", review);

    if review > 0 {
        std::process::exit(1);
    }
}
