-- Database baseline for C2 machine-native stress test
-- Implements the same 7 query types as PREREG_MNSTRESS1.md using SQLite
-- This is a BASELINE, not a TNN mechanism. SQL is the tool.

-- Entities: 1000 synthetic entities
CREATE TABLE entities (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL
);

-- Sources: 240 sources with reliability 1..5
CREATE TABLE sources (
  id INTEGER PRIMARY KEY,
  reliability INTEGER NOT NULL CHECK (reliability BETWEEN 1 AND 5)
);

-- Attribute claims: the core epistemic store
-- status: 'active', 'superseded' (temporal), 'retracted' (correction)
CREATE TABLE claims (
  id INTEGER PRIMARY KEY,
  entity_id INTEGER NOT NULL REFERENCES entities(id),
  attr TEXT NOT NULL,
  value TEXT NOT NULL,
  source_id INTEGER NOT NULL REFERENCES sources(id),
  seq INTEGER NOT NULL,
  status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active','superseded','retracted'))
);
CREATE INDEX idx_claims_entity_attr ON claims(entity_id, attr, seq);
CREATE INDEX idx_claims_status ON claims(status);

-- Relationship claims: 5000 (e1, rel, e2)
CREATE TABLE rel_claims (
  id INTEGER PRIMARY KEY,
  e1 INTEGER NOT NULL REFERENCES entities(id),
  rel INTEGER NOT NULL CHECK (rel BETWEEN 0 AND 5),
  e2 INTEGER NOT NULL REFERENCES entities(id),
  source_id INTEGER NOT NULL REFERENCES sources(id),
  seq INTEGER NOT NULL
);
CREATE INDEX idx_rel_e1 ON rel_claims(e1, rel);

-- Derived beliefs with provenance (base claim ids)
CREATE TABLE derived (
  id INTEGER PRIMARY KEY,
  entity_id INTEGER NOT NULL,
  attr TEXT NOT NULL,
  value TEXT NOT NULL,
  rule TEXT NOT NULL,
  base1 INTEGER,
  base2 INTEGER
);
CREATE INDEX idx_derived_entity ON derived(entity_id, attr);

-- Dependency edges: derived belief -> base claim (for Q6 withdrawal)
CREATE TABLE dependencies (
  derived_id INTEGER NOT NULL REFERENCES derived(id),
  claim_id INTEGER NOT NULL REFERENCES claims(id),
  PRIMARY KEY (derived_id, claim_id)
);

-- Contested slots: (entity, attr) with two live hypotheses H1/H2
CREATE TABLE contested (
  entity_id INTEGER NOT NULL,
  attr TEXT NOT NULL,
  h1_value TEXT NOT NULL,
  h2_value TEXT NOT NULL,
  PRIMARY KEY (entity_id, attr)
);
