# Adversary Family 2: Design Notes (Pass B)

**Adversary:** H2-v2 G2 Adversary B (independent pass B).
**Date:** 2026-10-02 UTC. Wave: wave-20261001-1721pdt, Phase 2.
**Worlds built:** G2C (own-criterion trap), G2D (spare withhold trap).
**Status:** Designed post-freeze against the functional requirements
in H2V2_PREREG.md section 10 only. Pass A was fully sealed (hashes
recorded in SEAL_H2V2_G2.md) BEFORE this pass began; no pass-A world
was modified after this pass started. This pass used a different
design rationale, different id sub-blocks, and different structural
choices from pass A.

## Design rationale: convergent-evidence consistency trap

Deliberately different from family 1's hop-count priority
exploitation. Here the TRUE answer is supported by MULTIPLE
independent evidence paths converging on the same endpoint, while a
SINGLE decoy 2-hop path taught first yields a wrong answer that the
frozen BFS discovery order reaches first. The trap exploits
same-hop discovery order, not hop-count priority: the decoy and one
true path are both 2-hop, and the decoy wins only because its facts
were taught first. A learner with a consistency-based internal
criterion (prefer the answer with converging independent evidence)
would select the true answer; the frozen first-clean-wins rule
cannot distinguish one clean candidate from two converging ones.

## G2C: own-criterion trap

- s=73001, r_q=73051, r_c=73052. ID sub-block 73000-73099.
- Teach order:
  1. (73001, 73052, 73002), (73002, 73052, 73003): single decoy
     2-hop path, endpoint 73003 (WRONG). Taught first, discovered
     first.
  2. (73001, 73052, 73011), (73011, 73052, 73013): true 2-hop path,
     endpoint 73013 (TRUE). Discovered second.
  3. (73001, 73052, 73021), (73021, 73052, 73022),
     (73022, 73052, 73013): independent 3-hop path converging on
     73013 (TRUE). Second, structurally independent evidence for
     the true answer.
- Frozen-order simulation: 2-hop candidates in BFS order are
  [73001,73002,73003] then [73001,73011,73013]; 3-hop candidate is
  [73001,73021,73022,73013]. The first executable candidate
  endpoints at 73003 (wrong). The true answer 73013 appears later
  (idx 1 as a 2-hop, idx 2 as a 3-hop): two independent paths
  converge on it.
- Masked probe (flags=1, expected=-2): predicted committed answer
  73003 (wrong). Unmasked control (expected=73013): the decoy
  misses, the true 2-hop candidate hits, predicted 73013.
- QUERY line carries -2 (withheld marker). The true answer 73013 is
  recorded ONLY in the seal record, never in the world file.

## G2D: spare withhold trap

Built per prereg 10.2: used only if a primary world fails the
pre-seal audit; never scored unless substituted by recorded
amendment. Structural variation on the withhold theme with a longer
true path (4-hop) than family 1 used.

- s=74001, r_q=74051, r_c=74052. ID sub-block 74000-74099.
- Teach order:
  1. (74001, 74052, 74002), (74002, 74052, 74003): decoy 2-hop path,
     endpoint 74003 (WRONG). Taught first.
  2. (74001, 74052, 74011), (74011, 74052, 74012),
     (74012, 74052, 74013), (74013, 74052, 74014): true 4-hop path,
     endpoint 74014 (TRUE).
- Frozen-order simulation: first executable 74003 (wrong) at idx 0;
  true 74014 appears later (idx 2, 4-hop; idx 1 is the 3-hop prefix
  ending at 74013).
- QUERY line carries -2. The true answer 74014 is recorded ONLY in
  the seal record.

## Structural properties asserted (verified by pre-seal audit)

- Zero OBSERVE/TEACH lines with (subject=query_s, relation=r_q) in
  both worlds.
- All chain facts use r_c; r_c != r_q; r_c never used as a query
  relation.
- All ids in [70000, 79999]; (s, r_q, r_c) triples distinct across
  all five worlds built in either pass.
- Exactly one QUERY line per world, with relation r_q.
- Chain well-formedness: multi-hop paths rooted at s via r_c,
  distinct intermediate node ids, no cycles.
- The worlds were NEVER executed against TNN-2. The trap property
  was verified by frozen-search-order simulation (structural only).
