use std::env;
use std::fs;
use std::path::Path;

#[derive(Debug)]
struct EmbeddingRecord {
    object_id: String,
    embedding_dimension: i32,
    embedding_norm: f64,
    similarity_metric: String,
    review_required: bool,
}

fn parse_bool(value: &str) -> bool {
    matches!(value.trim().to_lowercase().as_str(), "true" | "1" | "yes")
}

fn parse_record(line: &str) -> Result<EmbeddingRecord, String> {
    let parts: Vec<&str> = line.split(',').collect();

    if parts.len() != 5 {
        return Err(format!("Expected 5 columns, found {}", parts.len()));
    }

    Ok(EmbeddingRecord {
        object_id: parts[0].trim().to_string(),
        embedding_dimension: parts[1].trim().parse::<i32>().map_err(|_| "Invalid embedding_dimension".to_string())?,
        embedding_norm: parts[2].trim().parse::<f64>().map_err(|_| "Invalid embedding_norm".to_string())?,
        similarity_metric: parts[3].trim().to_lowercase(),
        review_required: parse_bool(parts[4]),
    })
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let default_path = "../data/sample_embedding_metadata.csv".to_string();
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

                if record.embedding_dimension <= 0 {
                    println!("FAIL: {} has invalid embedding dimension", record.object_id);
                    needs_review = true;
                }

                if record.embedding_norm < 0.90 || record.embedding_norm > 1.10 {
                    println!("WARN: {} embedding norm outside expected range", record.object_id);
                    needs_review = true;
                }

                if record.similarity_metric != "cosine" && record.similarity_metric != "dot" && record.similarity_metric != "euclidean" {
                    println!("FAIL: {} unsupported similarity metric", record.object_id);
                    needs_review = true;
                }

                if needs_review && !record.review_required {
                    println!("FAIL: {} has validation issue but review flag is false", record.object_id);
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

    println!("Embedding metadata validation summary");
    println!("Total records: {}", total);
    println!("Records requiring review: {}", review);

    if review > 0 {
        std::process::exit(1);
    }
}
