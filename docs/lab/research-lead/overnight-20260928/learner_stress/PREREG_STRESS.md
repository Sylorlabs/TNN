# PREREG: Continuing-Learner Stress Battery
## Pressure + interference + correction-under-pressure + delayed reuse through corrected premises, one unbroken lifetime

Worker: Continuing-Learner Stress Worker
Date: 2026-09-30 PDT
Status: FROZEN. No implementation exists at this commit. Any implementation commit must be a strict descendant of this commit.

## 0. Relation to prior work

DEVINT2 (BUILD-PASS 5fd1e0977, prereg 29682e102) tested delayed reuse,
interference, correction, and memory pressure in one persistent learner with a
consequence-weighted eviction policy. This battery goes BEYOND DEVINT2 on five
dimensions DEVINT2 did not cover: (a) corrections applied UNDER memory
pressure to STALE items (DEVINT2 corrected before pressure); (b) DOUBLE
correction / revision chains (4->6->8); (c) interference TARGETED at
corrected items (relation-overlap bombardment after correction); (d) delayed
reuse THROUGH corrected premises (two-hop compositions routing through
corrected rules; DEVINT2 composed only pre-correction premises and probed
corrected rules directly); (e) TWO pressure waves with dynamically useful junk
(DEVINT2 flooded once with never-queried junk; here 6 junk rules are queried
mid-flood so the consequence policy must promote newly useful items).
The learner under test is the consequence-weighted store (the DEVINT2
survivor); the twin recency policy is not re-litigated.

## 1. Hypothesis

A continuing learner with provenance + predictive bookkeeping, in-place
revision on contradiction, and consequence-weighted eviction will, in one
unbroken lifetime: retain foundation knowledge through two pressure waves and
two interference phases; take up corrections applied under pressure to stale
items with zero collateral; resolve a double-correction chain to the latest
label; resist targeted relation-overlap interference on corrected items; and
reuse corrected premises in novel two-hop compositions after a second pressure
wave, with zero re-teaching.

## 2. Architecture (frozen)

One Zag program, one process, one main(). The learner exposes exactly two
operations and never receives phase labels, task IDs, or mode flags:
learn(subj, rel, obj) and query(subj, rel, expected). Integer-coded episodes.
Single store, capacity 36, consequence eviction policy (frozen formula from
DEVINT2): importance = 10*(correct - wrong) + 5*dependents - 8*contradictions
+ 1; evict minimum importance, ties by lowest slot index. Revision in place:
contradiction sets superseded_obj = old obj, obj = new, contradictions++,
wrong++, last_used = tick; slot never freed. Retrieval exact-match only
(disclosed v1 scope limit). Two-hop composition is harness-level authored
infrastructure (answer = sign(r1 - r2)); the LEARNED behavior under test is
premise retrieval; each used premise registers dependents++.

Rule record: 11 i32 fields (subj, rel, obj, correct, wrong, dependents,
contradictions, last_used_tick, taught_tick, superseded_obj, valid), 44 bytes.

## 3. Frozen lifetime trajectory

Token codes. Foundation (vehicles): car=1, truck=2, bike=3, boat=4, plane=5,
train=6; wheels=10, seats=11, engines=12. Junk rel=99.

P1 FOUNDATION: teach 8 rules, query each once (baseline): (1,10)->4,
(1,11)->5, (2,10)->4 [deliberately false], (2,12)->1, (3,10)->2, (4,12)->2,
(5,11)->2 [deliberately false], (6,10)->8.

P2 PRESSURE WAVE 1 (dynamic importance): teach 15 junk (100..114, 99);
query 6 of them (100..105) 3x each (they become USEFUL: correct=3,
importance 31); teach 15 more junk (115..129). 2 evictions expected, both
never-queried junk. Record eviction victims.

P3 INTERFERENCE: teach 22 unrelated rules, each taught then queried once
immediately (importance 11): rocks (60,40)->7, (60,41)->30, (61,40)->5,
(61,41)->12, (62,40)->9, (62,41)->44; tools (70,42)->25, (70,43)->2,
(71,42)->18, (71,43)->1, (72,42)->40, (72,43)->3; fish (80,44)->4,
(80,45)->20, (81,44)->2, (81,45)->0, (82,44)->6, (82,45)->8; trees
(90,46)->12, (90,47)->25, (91,46)->8, (91,47)->30. 22 evictions expected,
all never-queried junk (exhausts the 22 plain junk exactly).

P4 CORRECTION UNDER PRESSURE: probe all 8 foundation rules (pre-correction
recall; raises each to correct=2). Record 12-rule collateral sample
predictions. Contradict (2,10) 4->6, then (2,10) 6->8 (DOUBLE correction /
revision chain), and (5,11) 2->180. Probe each corrected item 5x (expect 8,
8, 180; rebuilds correct counts: (2,10) c=7 w=2 k=2 importance 35; (5,11)
c=7 w=1 k=1 importance 53). Re-probe collateral sample; count changes.
Collateral sample: (1,10), (1,11), (3,10), (4,12), (6,10), (2,12), (60,40),
(70,42), (80,44), (90,46), (100,99), (101,99).

P5 TARGETED INTERFERENCE AT CORRECTIONS: teach 12 items sharing rel=10
(wheels) on fresh subjects 200..211, obj = 2+(i mod 4); each taught then
queried 2x (importance 21). 12 evictions expected among lowest-importance
slots (interference remnants; foundation and corrected items must NOT be
among victims). Probe corrected items (expect 8, 180) and all 8 foundation.

P6 DELAYED REUSE THROUGH CORRECTED PREMISES: 5 two-hop compositions, every
one routing through at least one corrected premise, frozen expected
sign(r1-r2): (2,10)=8 vs (3,10)=2 -> 1; (5,11)=180 vs (4,12)=2 -> 1;
(2,10)=8 vs (1,10)=4 -> 1; (5,11)=180 vs (1,11)=5 -> 1; (6,10)=8 vs
(2,10)=8 -> 0. Zero learn() calls on foundation keys between P1 teaching
and P6 (verified by structural grep of the source).

P7 PRESSURE WAVE 2: teach 20 junk (300..319, 99), never queried. 20
evictions expected among lowest-importance slots (interference/targeted
remnants); no foundation rule may be a victim.

P8 FINAL PROBE: query all 8 foundation rules (expect corrected labels 8 and
180 where corrected); query corrected items; count junk retained; STATEHASH.

## 4. Frozen kill bars

BUILD-PASS requires ALL of K-S1 through K-S6. Any failure is BUILD-FAIL.
No partial credit.

- K-S1 (retention through pressure 1 + interference): P4 pre-correction
  recall of 8 foundation rules >= 7/8.
- K-S2 (correction uptake under pressure): (a) corrected items answer new
  labels on all 5 post-correction probes each: (2,10)->8 5/5, (5,11)->180
  5/5; (b) double-correction chain resolves to latest label only: (2,10)
  answers 8, never 6 or 4, on all probes; (c) collateral damage = 0: all 12
  sample predictions identical before and after the contradictions.
- K-S3 (interference resistance of corrections): after P5, corrected items
  answer new labels 2/2 each; foundation recall >= 7/8; no foundation rule
  among P5 eviction victims.
- K-S4 (delayed reuse through corrected premises + survival of pressure 2):
  (a) P6 two-hop score >= 4/5; (b) structural grep confirms zero learn() on
  foundation keys between P1 teaching and P6; (c) P8 final foundation recall
  >= 7/8 with corrected labels; (d) no foundation rule among P7 eviction
  victims.
- K-S5 (determinism): 3/3 byte-identical runs of the same binary, exit 0,
  zero stderr.
- K-S6 (persistence / no-reset conformance): single znc compile; single
  binary run per pass; STATEHASH lines for all 8 phases with strictly
  increasing ticks; phases are sequential code blocks in one main(); the
  learner receives no phase labels, task IDs, or mode flags.

## 5. Governance

- Pure Zag only: implementation, build, runs, all analysis (grep/cmp/md5sum
  only). No Python anywhere including scratch.
- No em dashes in any documentation (byte-verified with check_no_dash.sh).
- Owned paths only:
  docs/lab/research-lead/overnight-20260928/learner_stress/. Files:
  PREREG_STRESS.md (this file), stress_learn.zag, STRESS_RESULT.md,
  STRESS_RAW_OUTPUT.txt.
- Binaries built only in /tmp, never staged.
- This worker reports BUILD-PASS or BUILD-FAIL only. No promotion claims;
  those require the full 11-step frontier pipeline.
- Authored infrastructure not claimed as learned: two-hop comparison
  operator, phase sequencing, integer episode coding, exact-match retrieval.
- Scope limits disclosed: exact-match retrieval only; integer-coded
  episodes; synthetic world with 2 deliberately false foundation facts.
- Baseline record: this battery runs against the CURRENT (pre-DDES)
  continuing learner so the DDES-integrated learner can be compared later.
