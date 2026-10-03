-- The 7 query types from PREREG_MNSTRESS1.md, implemented in SQL
-- Each query is demonstrated with a sample invocation

-- Q1: current belief about (entity, attr)
-- Returns the latest active claim's value
-- Sample: entity 42, attr0
.headers on
.mode column
.print '=== Q1: current belief about (42, attr0) ==='
SELECT value AS belief
FROM claims
WHERE entity_id = 42 AND attr = 'attr0' AND status = 'active'
ORDER BY seq DESC LIMIT 1;

-- Q2: why (exact provenance: supporting claim ids + sources)
-- Returns all active claims supporting the current belief, with source ids
.print '=== Q2: provenance for (42, attr0) ==='
SELECT c.id AS claim_id, c.source_id, s.reliability
FROM claims c JOIN sources s ON c.source_id = s.id
WHERE c.entity_id = 42 AND c.attr = 'attr0'
  AND c.value = (SELECT value FROM claims
                 WHERE entity_id = 42 AND attr = 'attr0' AND status = 'active'
                 ORDER BY seq DESC LIMIT 1)
  AND c.status = 'active'
ORDER BY c.seq;

-- Q3: which evidence disagrees (contradicting claim ids + sources)
-- Returns active claims with a different value for the same slot
.print '=== Q3: contradicting evidence for (42, attr0) ==='
SELECT c.id AS claim_id, c.value, c.source_id, s.reliability
FROM claims c JOIN sources s ON c.source_id = s.id
WHERE c.entity_id = 42 AND c.attr = 'attr0'
  AND c.value != (SELECT value FROM claims
                  WHERE entity_id = 42 AND attr = 'attr0' AND status = 'active'
                  ORDER BY seq DESC LIMIT 1)
  AND c.status = 'active'
ORDER BY c.seq;

-- Q4: consequences under context C (derived beliefs with context applied)
-- Returns derived beliefs for an entity; context filters rule applicability
-- Sample: entity 0, all derived beliefs
.print '=== Q4: derived beliefs for entity 0 ==='
SELECT d.id, d.attr, d.value, d.rule, d.base1, d.base2
FROM derived d
WHERE d.entity_id = 0;

-- Q5: what observation would distinguish H1 from H2
-- For a contested slot, names the slot and the differing predictions
-- Sample: first contested slot
.print '=== Q5: discriminating observation for first contested slot ==='
SELECT entity_id, attr,
       h1_value AS predicts_under_H1,
       h2_value AS predicts_under_H2
FROM contested
LIMIT 1;

-- Q6: if evidence E withdrawn, which beliefs lose support (dependency closure)
-- Recursive closure over dependencies starting from claim E
-- Sample: withdraw claim 0, find affected derived beliefs
.print '=== Q6: beliefs affected by withdrawing claim 0 ==='
WITH RECURSIVE affected(derived_id) AS (
  SELECT derived_id FROM dependencies WHERE claim_id = 0
  UNION
  SELECT d.derived_id FROM dependencies d
  JOIN affected a ON d.claim_id = a.derived_id
)
SELECT DISTINCT derived_id FROM affected;

-- Q7: which memories are load-bearing
-- Claims that are the SOLE support of at least one current belief
-- A claim is sole support if it is the only active claim for its (entity, attr, value)
.print '=== Q7: load-bearing claims (sample: first 5) ==='
SELECT c.id AS claim_id, c.entity_id, c.attr, c.value
FROM claims c
WHERE c.status = 'active'
  AND (SELECT COUNT(*) FROM claims c2
       WHERE c2.entity_id = c.entity_id
         AND c2.attr = c.attr
         AND c2.value = c.value
         AND c2.status = 'active') = 1
LIMIT 5;
