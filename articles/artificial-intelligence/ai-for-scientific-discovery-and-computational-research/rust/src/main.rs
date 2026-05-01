use std::env;
use std::fs;
use std::path::Path;

#[derive(Debug)]
struct CandidateRecord {
    candidate_id: String,
    predicted_property: f64,
    uncertainty_score: f64,
    acquisition_score: f64,
    safety_penalty: f64,
}

fn parse_record(line: &str) -> Result<CandidateRecord, String> {
    let parts: Vec<&str> = line.split(',').collect();

    if parts.len() != 5 {
        return Err(format!("Expected 5 columns, found {}", parts.len()));
    }

    Ok(CandidateRecord {
        candidate_id: parts[0].trim().to_string(),
        predicted_property: parts[1].trim().parse::<f64>().map_err(|_| "Invalid predicted_property".to_string())?,
        uncertainty_score: parts[2].trim().parse::<f64>().map_err(|_| "Invalid uncertainty_score".to_string())?,
        acquisition_score: parts[3].trim().parse::<f64>().map_err(|_| "Invalid acquisition_score".to_string())?,
        safety_penalty: parts[4].trim().parse::<f64>().map_err(|_| "Invalid safety_penalty".to_string())?,
    })
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let default_path = "../data/sample_candidate_predictions.csv".to_string();
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

                if !record.predicted_property.is_finite() || !record.acquisition_score.is_finite() {
                    println!("FAIL: {} has invalid numeric prediction values", record.candidate_id);
                    needs_review = true;
                }

                if record.uncertainty_score > 0.75 {
                    println!("WARN: {} has high uncertainty {:.3}", record.candidate_id, record.uncertainty_score);
                    needs_review = true;
                }

                if record.safety_penalty > 0.25 {
                    println!("WARN: {} has safety penalty {:.3}", record.candidate_id, record.safety_penalty);
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

    println!("Scientific candidate validation summary");
    println!("Total records: {}", total);
    println!("Records requiring review: {}", review);

    if review > 0 {
        std::process::exit(1);
    }
}
