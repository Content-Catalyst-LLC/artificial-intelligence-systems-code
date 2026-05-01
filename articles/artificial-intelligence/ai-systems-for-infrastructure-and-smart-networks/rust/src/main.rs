use std::env;
use std::fs;
use std::path::Path;

#[derive(Debug)]
struct TelemetryRecord {
    asset_id: String,
    metric_name: String,
    metric_value: f64,
    sensor_health: f64,
    latency_seconds: f64,
}

fn parse_record(line: &str) -> Result<TelemetryRecord, String> {
    let parts: Vec<&str> = line.split(',').collect();

    if parts.len() != 5 {
        return Err(format!("Expected 5 columns, found {}", parts.len()));
    }

    let metric_value = parts[2]
        .trim()
        .parse::<f64>()
        .map_err(|_| "Invalid metric_value".to_string())?;

    let sensor_health = parts[3]
        .trim()
        .parse::<f64>()
        .map_err(|_| "Invalid sensor_health".to_string())?;

    let latency_seconds = parts[4]
        .trim()
        .parse::<f64>()
        .map_err(|_| "Invalid latency_seconds".to_string())?;

    Ok(TelemetryRecord {
        asset_id: parts[0].trim().to_string(),
        metric_name: parts[1].trim().to_string(),
        metric_value,
        sensor_health,
        latency_seconds,
    })
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let default_path = "../data/sample_telemetry.csv".to_string();
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
                let mut record_failed = false;

                if record.sensor_health < 0.70 {
                    println!(
                        "WARNING: {} has low sensor health {:.3}",
                        record.asset_id,
                        record.sensor_health
                    );
                    record_failed = true;
                }

                if record.latency_seconds > 30.0 {
                    println!(
                        "WARNING: {} has high telemetry latency {:.3}s",
                        record.asset_id,
                        record.latency_seconds
                    );
                    record_failed = true;
                }

                if !record.metric_value.is_finite() {
                    println!("FAIL: {} has invalid metric value", record.asset_id);
                    record_failed = true;
                }

                if record_failed {
                    failed += 1;
                }
            }
            Err(error) => {
                println!("Line {} parse error: {}", index + 1, error);
                failed += 1;
            }
        }
    }

    println!("Smart infrastructure telemetry validation summary");
    println!("Total records: {}", total);
    println!("Records requiring review: {}", failed);

    if failed > 0 {
        std::process::exit(1);
    }
}
