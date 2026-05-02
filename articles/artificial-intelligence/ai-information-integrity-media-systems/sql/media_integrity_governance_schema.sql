-- AI information integrity and media-system governance schema.
-- This schema supports provenance tracking, source attribution, synthetic-media review,
-- correction monitoring, amplification-risk analysis, governance actions, public reporting,
-- and rights-respecting media-system accountability.
--
-- Do not store sensitive, personal, confidential, private newsroom,
-- platform-internal, unpublished source, legally restricted, security-sensitive,
-- election-sensitive, harassment-related, or nonconsensual media data without
-- appropriate controls.

CREATE TABLE media_systems (
    system_id INTEGER PRIMARY KEY,
    system_name TEXT NOT NULL,
    purpose TEXT NOT NULL,
    owner_team TEXT NOT NULL,
    deployment_context TEXT NOT NULL,
    deployment_status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT
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
    synthetic_media INTEGER DEFAULT 0,
    public_interest_context INTEGER DEFAULT 0,
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
    chain_of_custody_summary TEXT,
    verification_status TEXT NOT NULL,
    checked_at TEXT,
    FOREIGN KEY (content_id) REFERENCES content_records(content_id)
);

CREATE TABLE source_records (
    source_id INTEGER PRIMARY KEY,
    system_id INTEGER NOT NULL,
    source_name TEXT NOT NULL,
    source_type TEXT NOT NULL,
    source_credibility REAL,
    editorial_accountability_available INTEGER DEFAULT 0,
    correction_policy_available INTEGER DEFAULT 0,
    public_interest_source INTEGER DEFAULT 0,
    last_reviewed TEXT,
    FOREIGN KEY (system_id) REFERENCES media_systems(system_id)
);

CREATE TABLE integrity_risk_scores (
    score_id INTEGER PRIMARY KEY,
    content_id INTEGER NOT NULL,
    source_credibility REAL NOT NULL,
    claim_uncertainty REAL NOT NULL,
    amplification_ratio REAL NOT NULL,
    public_impact REAL NOT NULL,
    verification_strength REAL NOT NULL,
    provenance_gap REAL NOT NULL,
    correction_gap REAL,
    information_integrity_risk REAL NOT NULL,
    risk_band TEXT NOT NULL,
    scored_at TEXT NOT NULL,
    FOREIGN KEY (content_id) REFERENCES content_records(content_id)
);

CREATE TABLE corrections (
    correction_id INTEGER PRIMARY KEY,
    content_id INTEGER NOT NULL,
    correction_text TEXT NOT NULL,
    correction_type TEXT,
    original_reach INTEGER,
    correction_reach INTEGER,
    correction_effectiveness REAL,
    issued_at TEXT NOT NULL,
    visible_to_original_audience INTEGER DEFAULT 0,
    FOREIGN KEY (content_id) REFERENCES content_records(content_id)
);

CREATE TABLE platform_governance_actions (
    action_id INTEGER PRIMARY KEY,
    content_id INTEGER NOT NULL,
    action_type TEXT NOT NULL,
    action_reason TEXT,
    automated_action INTEGER NOT NULL,
    human_reviewed INTEGER NOT NULL,
    appeal_available INTEGER NOT NULL,
    public_interest_exception_considered INTEGER DEFAULT 0,
    action_time TEXT NOT NULL,
    FOREIGN KEY (content_id) REFERENCES content_records(content_id)
);

CREATE TABLE amplification_monitoring (
    monitoring_id INTEGER PRIMARY KEY,
    content_id INTEGER NOT NULL,
    baseline_views REAL,
    observed_views REAL,
    amplification_ratio REAL,
    low_integrity_signal REAL,
    coordinated_behavior_signal REAL,
    measured_at TEXT NOT NULL,
    review_required INTEGER DEFAULT 0,
    FOREIGN KEY (content_id) REFERENCES content_records(content_id)
);

CREATE TABLE synthetic_media_reviews (
    review_id INTEGER PRIMARY KEY,
    content_id INTEGER NOT NULL,
    synthetic_media_type TEXT NOT NULL,
    impersonation_risk INTEGER NOT NULL,
    public_figure_or_official_context INTEGER DEFAULT 0,
    nonconsensual_or_harassment_risk INTEGER DEFAULT 0,
    provenance_required INTEGER NOT NULL,
    disclosure_required INTEGER NOT NULL,
    review_status TEXT NOT NULL,
    reviewed_at TEXT,
    FOREIGN KEY (content_id) REFERENCES content_records(content_id)
);

CREATE TABLE media_integrity_reports (
    report_id INTEGER PRIMARY KEY,
    system_id INTEGER NOT NULL,
    reporting_period TEXT NOT NULL,
    provenance_coverage REAL,
    ai_provenance_coverage REAL,
    source_diversity REAL,
    correction_effectiveness REAL,
    low_integrity_amplification REAL,
    synthetic_media_review_rate REAL,
    public_summary_url TEXT,
    published_at TEXT,
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

-- Governance query: high-amplification content with low-integrity signals.
SELECT
    m.system_name,
    c.content_identifier,
    c.content_type,
    a.amplification_ratio,
    a.low_integrity_signal,
    a.coordinated_behavior_signal,
    a.review_required
FROM amplification_monitoring a
JOIN content_records c ON a.content_id = c.content_id
JOIN media_systems m ON c.system_id = m.system_id
WHERE a.amplification_ratio >= 3.0
  AND a.low_integrity_signal >= 0.60;

-- Governance query: synthetic media requiring disclosure or provenance review.
SELECT
    m.system_name,
    c.content_identifier,
    s.synthetic_media_type,
    s.impersonation_risk,
    s.provenance_required,
    s.disclosure_required,
    s.review_status
FROM synthetic_media_reviews s
JOIN content_records c ON s.content_id = c.content_id
JOIN media_systems m ON c.system_id = m.system_id
WHERE s.provenance_required = 1
   OR s.disclosure_required = 1;
