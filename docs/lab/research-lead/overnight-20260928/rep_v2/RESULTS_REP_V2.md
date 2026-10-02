# Rep v2 FDCR: Result Report (2026-09-29)

## Implementation

File: `fdcr_learn.zag` (~1,300 lines, pure Zag, no Python).
Binary: `fdcr_learn` (compiled with znc, not committed).

Operators implemented:
- FORM: shared-subset parent recruitment + subset/superset linking.
- MERGE: identical-intent concept merging.
- SPLIT: contradiction-driven child recruitment (parent preserved).
- GRADE: graded membership, most-specific retrieval.
- CONTEXTUALIZE: context-conditioned children (reason=5).
- COMPOSE: defined in prereg, not yet implemented (exploratory).

## Frozen Bar Verdicts

### K5 (hierarchy): PASS (4/4)
- Parent C2: intent exactly `{flies=yes}`, 8 members, reason=1 (FORM).
- Sparrow C0 and eagle C1 both have parent=2.
- Bar met: `{flies=yes}` parent exists, contains all eight, clusters descend.

### K2 (delayed split): PASS (5/5)
- Phase 1: E1a/E1b merged in C0 `{r1=o1,r2=o2}`.
- Phase 2: SPLIT fired. C1 `{r1o1,r2o2,r3o3a}` (E1a), C2 `{r1o1,r2o2,r3o3b}` (E1b), both parent=0, reason=2.
- Probes: `(E1a,r3)->o3a` ✓, `(E1b,r3)->o3b` ✓.
- Bar met: both phase-two r3 probes correct.

### K4 (overlap): PASS (2/2)
- Shared C2: intent exactly `{r1o1,r2o2}`, members {B1,B2}, reason=1 (FORM).
- Children C0 (B1 full), C1 (B2 full), both parent=2.
- Bar met: shared concept with exactly 2 shared features, B1/B2 members, distinct children.

### K3 (delayed merge, sanity): PASS (5/5)
- M1a (phase 0) and M1b (phase 1, identical) merged into single C0 with both members.
- All probes correct.

### mini_world regression: PASS (8/8)
- Original SEM 8/8 probes all correct.
- Includes sibling-based inference (marked "sib" in output).
- WITHHOLD probes correctly withhold.

## Exploratory

### Context (ctx_test.txt): 3/3
- Base C0 `{r1=o1,r1=o2,r2=o3}` (contradictory).
- C1 (work): `{r1=o1,r2=o3}`, parent=0, reason=5. C2 (home): `{r1=o2,r2=o3}`, parent=0, reason=5.
- Context-conditioned queries retrieve correct values.
- Mechanism works; not a verdict bar.

## Determinism

All fixtures run 3x, byte-identical outputs:
- k5.txt, k2.txt, k4.txt, k3_merge.txt, mini_world.txt, ctx_test.txt: DETERMINISTIC.

## Hardcoding Check

No test vocabulary (`flies`, `sparrow`, `eagle`, `o3a`, `squeezer`, etc.) appears in source.
Implementation is generic.

## Bugs Fixed During Development

1. WITHHOLD parsing: length check used 9 instead of 8 ("WITHHOLD" is 8 chars).
2. FORM did not link subset/superset concepts (e.g., vellum/sheet). Added proper-subset linking.
3. Query retrieval stopped at ambiguous parent; added direct taught-fact lookup (Step 0) before concept inference.
4. Sibling inference did not consider children members; extended to include child concept members.

## Limitations and Open Questions

1. COMPOSE operator not implemented (prereg exploratory).
2. Sibling inference is heuristic; may not generalize.
3. Graded membership (GRADE) is structural but not quantitatively evaluated.
4. K5 produced extra SPLIT children (C3-C6: size/eats distinctions). These are valid but were not required by the bar. Not marketed as successes.
5. Claim scope is representational adequacy only. NOT L3. L3 requires transfer, ablation, reuse, red team per Micah's nine criteria.

## Raw Outputs

See `raw_outputs/` for authoritative execution logs.

## Commit

Implementation and fixtures committed separately from this report.
Binary `fdcr_learn` not committed (generated artifact).
