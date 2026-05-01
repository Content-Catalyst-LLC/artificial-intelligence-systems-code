use std::env;
use std::fs;
use std::path::Path;

#[derive(Debug)]
struct EnvironmentalRecord {
    zone_id: String,
    variable_name: String,
    value: f64,
    sensor_health: f64,
    uncertainty: f64,
}

fn parse_record(line: &str) -> Result<EnvironmentalRecord, String> {
    let parts: Vec<&str> = line.split(',').collect();

    if parts.len() != 5 {
        return Err(format!("Expected 5 columns, found {}", parts.len()));
    }

    let value = parts[2]
        .trim()
        .parse::<f64>()
        .map_err(|_| "Invalid value".to_string())?;

    let sensor_health = parts[3]
        .trim()
        .parse::<f64>()
        .map_err(|_| "Invalid sensor_health".to_string())?;

    let uncertainty = parts[4]
        .trim()
        .parse::<f64>()
        .map_err(|_| "Invalid uncertainty".to_string())?;

    Ok(EnvironmentalRecord {
        zone_id: parts[0].trim().to_string(),
        variable_name: parts[1].trim().to_string(),
        value,
        sensor_health,
        uncertainty,
    })
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let default_path = "../data/sample_environmental_sensor_records.csv".to_string();
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

                if !record.value.is_finite() {
                    println!("FAIL: {} {} has invalid value", record.zone_id, record.variable_name);
                    needs_review = true;
                }

                if record.sensor_health < 0.70 {
                    println!("WARN: {} low sensor health {:.3}", record.zone_id, record.sensor_health);
                    needs_review = true;
                }

                if record.uncertainty > 0.30 {
                    println!("WARN: {} high uncertainty {:.3}", record.zone_id, record.uncertainty);
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

    println!("Environmental sensor validation summary");
    println!("Total records: {}", total);
    println!("Records requiring review: {}", review);

    if review > 0 {
        std::process::exit(1);
    }
}
