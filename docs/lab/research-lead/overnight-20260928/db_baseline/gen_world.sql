-- Generate synthetic world matching PREREG_MNSTRESS1.md scale
-- Deterministic via fixed patterns (no random needed for structural test)

-- 1000 entities with syllable-table names
WITH RECURSIVE cnt(n) AS (
  SELECT 0 UNION ALL SELECT n+1 FROM cnt WHERE n < 999
)
INSERT INTO entities (id, name)
SELECT n, 'ent_' || (n / 100) || '_' || (n % 100) FROM cnt;

-- 240 sources, reliability 1..5 cycling
WITH RECURSIVE cnt(n) AS (
  SELECT 0 UNION ALL SELECT n+1 FROM cnt WHERE n < 239
)
INSERT INTO sources (id, reliability)
SELECT n, 1 + (n % 5) FROM cnt;

-- 6000 attribute claims: 1000 entities x 6 attrs, values from small vocab
-- Use deterministic pattern: value = 'v' || ((entity_id + attr_idx) % 4)
WITH RECURSIVE
ents(e) AS (SELECT 0 UNION ALL SELECT e+1 FROM ents WHERE e < 999),
attrs(a) AS (SELECT 0 UNION ALL SELECT a+1 FROM attrs WHERE a < 5)
INSERT INTO claims (id, entity_id, attr, value, source_id, seq, status)
SELECT
  (e * 6 + a) AS id,
  e AS entity_id,
  'attr' || a AS attr,
  'v' || ((e + a) % 4) AS value,
  (e * 6 + a) % 240 AS source_id,
  (e * 6 + a) AS seq,
  'active' AS status
FROM ents, attrs;

-- 500 DELIBERATE contradictions: same (entity, attr), different value, different source
-- Take first 500 claims, add contradicting claim with different value
INSERT INTO claims (id, entity_id, attr, value, source_id, seq, status)
SELECT
  6000 + c.id AS id,
  c.entity_id,
  c.attr,
  'v' || ((CAST(SUBSTR(c.value, 2) AS INTEGER) + 1) % 4) AS value,
  (c.source_id + 120) % 240 AS source_id,
  6000 + c.seq AS seq,
  'active' AS status
FROM claims c
WHERE c.id < 500;

-- Mark these 500 slots as contested (H1 = original value, H2 = contradicting value)
INSERT INTO contested (entity_id, attr, h1_value, h2_value)
SELECT DISTINCT c.entity_id, c.attr, c.value,
  'v' || ((CAST(SUBSTR(c.value, 2) AS INTEGER) + 1) % 4)
FROM claims c
WHERE c.id < 500;

-- 60 temporal supersessions: v1 at t1, v2 at later t2; old retained as SUPERSEDED
-- Take claims 500..559, add newer version, mark old as superseded
INSERT INTO claims (id, entity_id, attr, value, source_id, seq, status)
SELECT
  6500 + (c.id - 500) AS id,
  c.entity_id,
  c.attr,
  'v' || ((CAST(SUBSTR(c.value, 2) AS INTEGER) + 2) % 4) AS value,
  c.source_id,
  6500 + c.seq AS seq,
  'active' AS status
FROM claims c
WHERE c.id BETWEEN 500 AND 559;

UPDATE claims SET status = 'superseded'
WHERE id BETWEEN 500 AND 559;

-- 40 delayed corrections: earlier claim retracted by later high-reliability correction
-- Take claims 560..599, add correction from a reliability-5 source, mark old retracted
INSERT INTO claims (id, entity_id, attr, value, source_id, seq, status)
SELECT
  6560 + (c.id - 560) AS id,
  c.entity_id,
  c.attr,
  'v' || ((CAST(SUBSTR(c.value, 2) AS INTEGER) + 3) % 4) AS value,
  4 AS source_id,
  6560 + c.seq AS seq,
  'active' AS status
FROM claims c
WHERE c.id BETWEEN 560 AND 599;

UPDATE claims SET status = 'retracted'
WHERE id BETWEEN 560 AND 599;

-- 5000 relationship claims (e1, rel, e2)
WITH RECURSIVE cnt(n) AS (
  SELECT 0 UNION ALL SELECT n+1 FROM cnt WHERE n < 4999
)
INSERT INTO rel_claims (id, e1, rel, e2, source_id, seq)
SELECT
  n AS id,
  n % 1000 AS e1,
  n % 6 AS rel,
  (n * 7 + 13) % 1000 AS e2,
  n % 240 AS source_id,
  n AS seq
FROM cnt;

-- Derived beliefs via R1: (X located-in Y) + (Y habitat H) => (X habitat H)
-- Simulate with rel=0 as 'located-in', rel=1 as 'habitat'
-- For simplicity, derive 100 sample derived beliefs
WITH RECURSIVE cnt(n) AS (
  SELECT 0 UNION ALL SELECT n+1 FROM cnt WHERE n < 99
)
INSERT INTO derived (id, entity_id, attr, value, rule, base1, base2)
SELECT
  n AS id,
  (n * 11) % 1000 AS entity_id,
  'habitat' AS attr,
  'h' || (n % 5) AS value,
  'R1' AS rule,
  n * 2 AS base1,
  n * 2 + 1 AS base2
FROM cnt;

-- Dependencies: each derived depends on its two base claims
INSERT INTO dependencies (derived_id, claim_id)
SELECT id, base1 FROM derived
UNION
SELECT id, base2 FROM derived;

-- 2000 junk claims as interference (separate attr namespace)
WITH RECURSIVE cnt(n) AS (
  SELECT 0 UNION ALL SELECT n+1 FROM cnt WHERE n < 1999
)
INSERT INTO claims (id, entity_id, attr, value, source_id, seq, status)
SELECT
  10000 + n AS id,
  n % 1000 AS entity_id,
  'junk' AS attr,
  'j' || (n % 10) AS value,
  n % 240 AS source_id,
  10000 + n AS seq,
  'active' AS status
FROM cnt;
