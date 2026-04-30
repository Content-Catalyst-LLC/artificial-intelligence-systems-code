-- AI History Timeline Metadata Schema
-- Supports article-level documentation for:
-- The History of Artificial Intelligence: From Symbolic Logic to Machine Learning

CREATE TABLE IF NOT EXISTS ai_history_events (
    event_id TEXT PRIMARY KEY,
    event_year INTEGER NOT NULL,
    event_name TEXT NOT NULL,
    paradigm TEXT NOT NULL,
    event_summary TEXT,
    source_id TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ai_history_sources (
    source_id TEXT PRIMARY KEY,
    author TEXT,
    publication_year INTEGER,
    title TEXT NOT NULL,
    source_type TEXT,
    url TEXT,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS ai_history_paradigms (
    paradigm_id TEXT PRIMARY KEY,
    paradigm_name TEXT NOT NULL,
    approximate_start_year INTEGER,
    approximate_peak_year INTEGER,
    core_methods TEXT,
    limitations TEXT,
    continuing_relevance TEXT
);

CREATE TABLE IF NOT EXISTS ai_history_article_links (
    link_id TEXT PRIMARY KEY,
    article_slug TEXT NOT NULL,
    related_article_slug TEXT NOT NULL,
    relation_type TEXT NOT NULL
);
