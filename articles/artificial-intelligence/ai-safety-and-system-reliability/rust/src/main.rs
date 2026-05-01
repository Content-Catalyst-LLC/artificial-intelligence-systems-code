use std::env;
use std::fs;
use std::path::Path;

#[derive(Debug)]
struct SafetyEvent {
    event_id: String,
    predicted_probability: f64,
    uncertainty: f64,
    observed_outcome: u8,
    region: String,
    review_required: bool,
}

#[derive(Debug)]
struct SafetySummary {
    records: usize,
    flagged: usize,
    review_required: usize,
    missed_failures: usize,
    invalid_probability: usize,
    invalid_uncertainty: usize,
}

fn parse_bool(value: &str) -> bool {
    matches!(
        value.trim().to_lowercase().as_str(),
        "true" | "1" | "yes" | "y"
    )
}

fn parse_event(line: &str) -> Result<SafetyEvent, String> {
    let cols: Vec<&str> = line.split(',').collect();

    if cols.len() != 6 {
        return Err(format!("Expected 6 columns, found {}", cols.len()));
    }

    let predicted_probability = cols[1]
        .trim()
        .parse::<f64>()
        .map_err(|_| format!("Invalid predicted_probability for {}", cols[0]))?;

    let uncertainty = cols[2]
        .trim()
        .parse::<f64>()
        .map_err(|_| format!("Invalid uncertainty for {}", cols[0]))?;

    let observed_outcome = cols[3]
        .trim()
        .parse::<u8>()
        .map_err(|_| format!("Invalid observed_outcome for {}", cols[0]))?;

    Ok(SafetyEvent {
        event_id: cols[0].trim().to_string(),
        predicted_probability,
        uncertainty,
        observed_outcome,
        region: cols[4].trim().to_string(),
        review_required: parse_bool(cols[5]),
    })
}

fn summarize(events: &[SafetyEvent], decision_threshold: f64) -> SafetySummary {
    let mut summary = SafetySummary {
        records: events.len(),
        flagged: 0,
        review_required: 0,
        missed_failures: 0,
        invalid_probability: 0,
        invalid_uncertainty: 0,
    };

    for event in events {
        if !(0.0..=1.0).contains(&event.predicted_probability) {
            summary.invalid_probability += 1;
        }

        if !(0.0..=1.0).contains(&event.uncertainty) {
            summary.invalid_uncertainty += 1;
        }

        let flagged = event.predicted_probability >= decision_threshold;

        if flagged {
            summary.flagged += 1;
        }

        if event.review_required {
            summary.review_required += 1;
        }

        if !flagged && event.observed_outcome == 1 {
            summary.missed_failures += 1;
        }
    }

    summary
}

fn print_summary(summary: &SafetySummary) {
    let records = summary.records.max(1) as f64;

    println!("AI Safety Reliability CLI Summary");
    println!("=================================");
    println!("Records: {}", summary.records);
    println!("Flagged records: {}", summary.flagged);
    println!(
        "Flag rate: {:.4}",
        summary.flagged as f64 / records
    );
    println!("Human review required: {}", summary.review_required);
    println!(
        "Review rate: {:.4}",
        summary.review_required as f64 / records
    );
    println!("Missed failures: {}", summary.missed_failures);
    println!(
        "Missed failure rate: {:.4}",
        summary.missed_failures as f64 / records
    );
    println!("Invalid probability values: {}", summary.invalid_probability);
    println!("Invalid uncertainty values: {}", summary.invalid_uncertainty);
}

fn main() {
    let args: Vec<String> = env::args().collect();

    let csv_path = if args.len() > 1 {
        args[1].clone()
    } else {
        "../data/sample_safety_events.csv".to_string()
    };

    let path = Path::new(&csv_path);

    let content = fs::read_to_string(path).unwrap_or_else(|error| {
        panic!("Could not read CSV file '{}': {}", csv_path, error);
    });

    let mut events: Vec<SafetyEvent> = Vec::new();

    for (index, line) in content.lines().enumerate() {
        if index == 0 {
            continue;
        }

        if line.trim().is_empty() {
            continue;
        }

        match parse_event(line) {
            Ok(event) => events.push(event),
            Err(error) => eprintln!("Skipping line {}: {}", index + 1, error),
        }
    }

    let summary = summarize(&events, 0.70);
    print_summary(&summary);

    if summary.invalid_probability > 0 || summary.invalid_uncertainty > 0 {
        std::process::exit(2);
    }

    if summary.missed_failures > 0 {
        std::process::exit(1);
    }
}
