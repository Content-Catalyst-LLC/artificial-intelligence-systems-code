-- AI information integrity and media-system governance schema.
-- This schema supports provenance tracking, source attribution,
-- correction monitoring, amplification-risk analysis, and public reporting.

CREATE TABLE media_systems (
    system_id INTEGER PRIMARY KEY,
    system_name TEXT NOT NULL,
    purpose TEXT NOT NULL,
    owner_team TEXT NOT NULL,
    deployment_context TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE content_records (
    content_id INTEGER PRIMARY KEY,
    system_id INTEGER NOT NULL,
    content_identifier TEXT NOT NULL,
    content_type TEXT NOT NULL,
    source_name TEXT,
    source_type TEXT NOT NULL,
    ai_generated INTEGER NOT NULL,
    ai_assisted INTEGER NOT NULL,
    published_at TEXT,
    FOREIGN KEY (system_id) REFERENCES media_systems(system_id)
);

CREATE TABLE provenance_records (
    provenance_id INTEGER PRIMARY KEY,
    content_id INTEGER NOT NULL,
    provenance_available INTEGER NOT NULL,
    provenance_type TEXT,
    creator_claim TEXT,
    edit_history_available INTEGER NOT NULL,
    cryptographic_signature_available INTEGER NOT NULL,
    verification_status TEXT NOT NULL,
    checked_at TEXT,
    FOREIGN KEY (content_id) REFERENCES content_records(content_id)
);

CREATE TABLE integrity_risk_scores (
    score_id INTEGER PRIMARY KEY,
    content_id INTEGER NOT NULL,
    source_credibility REAL NOT NULL,
    claim_uncertainty REAL NOT NULL,
    amplification_ratio REAL NOT NULL,
    public_impact REAL NOT NULL,
    verification_strength REAL NOT NULL,
    information_integrity_risk REAL NOT NULL,
    risk_band TEXT NOT NULL,
    scored_at TEXT NOT NULL,
    FOREIGN KEY (content_id) REFERENCES content_records(content_id)
);

CREATE TABLE corrections (
    correction_id INTEGER PRIMARY KEY,
    content_id INTEGER NOT NULL,
    correction_text TEXT NOT NULL,
    original_reach INTEGER,
    correction_reach INTEGER,
    correction_effectiveness REAL,
    issued_at TEXT NOT NULL,
    FOREIGN KEY (content_id) REFERENCES content_records(content_id)
);

CREATE TABLE platform_governance_actions (
    action_id INTEGER PRIMARY KEY,
    content_id INTEGER NOT NULL,
    action_type TEXT NOT NULL,
    action_reason TEXT,
    human_reviewed INTEGER NOT NULL,
    appeal_available INTEGER NOT NULL,
    action_time TEXT NOT NULL,
    FOREIGN KEY (content_id) REFERENCES content_records(content_id)
);

CREATE TABLE media_integrity_reports (
    report_id INTEGER PRIMARY KEY,
    system_id INTEGER NOT NULL,
    reporting_period TEXT NOT NULL,
    provenance_coverage REAL,
    source_diversity REAL,
    correction_effectiveness REAL,
    low_integrity_amplification REAL,
    public_summary_url TEXT,
    FOREIGN KEY (system_id) REFERENCES media_systems(system_id)
);

-- Governance query: high-risk content without provenance.
SELECT
    m.system_name,
    c.content_identifier,
    c.content_type,
    c.source_type,
    p.provenance_available,
    r.information_integrity_risk,
    r.risk_band
FROM content_records c
JOIN media_systems m ON c.system_id = m.system_id
JOIN provenance_records p ON c.content_id = p.content_id
JOIN integrity_risk_scores r ON c.content_id = r.content_id
WHERE p.provenance_available = 0
  AND r.risk_band = 'high';

-- Governance query: correction effectiveness by source type.
SELECT
    c.source_type,
    AVG(co.correction_effectiveness) AS mean_correction_effectiveness,
    COUNT(co.correction_id) AS corrections
FROM corrections co
JOIN content_records c ON co.content_id = c.content_id
GROUP BY c.source_type;
