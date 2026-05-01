use std::env;
use std::fs;
use std::path::Path;

#[derive(Debug)]
struct AISystemRecord {
    system_id: String,
    risk_tier: String,
    governance_readiness: f64,
    monitoring_coverage: f64,
    human_oversight: f64,
}

fn parse_record(line: &str) -> Result<AISystemRecord, String> {
    let parts: Vec<&str> = line.split(',').collect();

    if parts.len() != 5 {
        return Err(format!("Expected 5 columns, found {}", parts.len()));
    }

    Ok(AISystemRecord {
        system_id: parts[0].trim().to_string(),
        risk_tier: parts[1].trim().to_lowercase(),
        governance_readiness: parts[2].trim().parse::<f64>().map_err(|_| "Invalid governance_readiness".to_string())?,
        monitoring_coverage: parts[3].trim().parse::<f64>().map_err(|_| "Invalid monitoring_coverage".to_string())?,
        human_oversight: parts[4].trim().parse::<f64>().map_err(|_| "Invalid human_oversight".to_string())?,
    })
}

fn score_in_range(value: f64) -> bool {
    value >= 0.0 && value <= 1.0
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let default_path = "../data/sample_ai_system_inventory.csv".to_string();
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

                if !score_in_range(record.governance_readiness)
                    || !score_in_range(record.monitoring_coverage)
                    || !score_in_range(record.human_oversight)
                {
                    println!("FAIL: {} has score outside [0,1]", record.system_id);
                    needs_review = true;
                }

                if record.risk_tier == "high" && record.human_oversight < 0.65 {
                    println!("FAIL: {} is high risk with weak human oversight", record.system_id);
                    needs_review = true;
                }

                if record.governance_readiness < 0.45 {
                    println!("WARN: {} has low governance readiness", record.system_id);
                    needs_review = true;
                }

                if record.monitoring_coverage < 0.40 {
                    println!("WARN: {} has low monitoring coverage", record.system_id);
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

    println!("AI system inventory validation summary");
    println!("Total records: {}", total);
    println!("Records requiring review: {}", review);

    if review > 0 {
        std::process::exit(1);
    }
}
