# PREREG: DEVINT2 - Developmental Integration Worker 2
## Delayed reuse, interference, correction, memory pressure in one persistent learner

Worker: Developmental Integration Worker 2 (subagent 79513561-c750-4a6e-aa65-082869c7f178)
Date: 2026-09-29 PDT
Status: FROZEN. No implementation exists at this commit. Any implementation commit must be a strict descendant of this commit.

## 0. Coordination note

No Worker 1 trajectory material was found in the repo at prereg time. To avoid
duplication, Worker 2 uses a DISTINCT developmental sequence from the forward
trajectory Micah sketched (raw sequence -> segmentation -> concepts ->
relations -> prediction -> contradiction -> inquiry -> revision -> delayed
reuse). Worker 2's emphasis, per assignment: delayed reuse AFTER unrelated
interference, correction without catastrophic forgetting, and memory pressure
with a controlled policy comparison. Shared integration design vocabulary used
by both workers: one persistent process, no task IDs/prefixes supplied to the
learner, no resets, no recompilation between stages, staged harness invisible
to cognition.

## 1. Hypothesis

A continuing learner that (a) stores learned associations with provenance and
predictive bookkeeping, (b) revises in place on contradiction, and (c) evicts
under capacity pressure by COGNITIVE CONSEQUENCE (predictive value, dependency,
contradiction cost) rather than recency, will:

- retrieve early knowledge after long unrelated interference without re-teaching,
- compose early knowledge with later knowledge in two-hop queries,
- correct contradicted beliefs with zero collateral damage to unrelated beliefs,
- retain predictively useful but stale knowledge under memory pressure while a
  recency-eviction twin catastrophically forgets it.

This directly tests Micah's key question: memory importance must depend on
cognitive consequences (dependency, uniqueness of evidence, predictive value,
contradiction, reconstructability), not query count, age, or a fixed cache
metric.

## 2. Architecture (frozen)

One Zag program, one process, one main(). The LEARNER exposes exactly two
operations to the world; it never receives stage labels, task IDs, or mode
flags:

- learn(subj, rel, obj): store or revise the association (subj,rel)->obj.
- query(subj, rel, expected): predict obj for (subj,rel); the world scores
  against expected and the learner updates its predictive books.

Episodes are integer-coded (subject, relation) -> object. No string parsing.
This is disclosed: token encoding is not under test; retrieval, revision, and
retention are.

Rule store record (11 i32 fields): subj, rel, obj, correct, wrong, dependents,
contradictions, last_used_tick, taught_tick, superseded_obj, valid.

learn() semantics:
- key exists, same obj: refresh last_used only. No bookkeeping inflation.
- key exists, different obj (contradiction): superseded_obj = old obj;
  obj = new; contradictions++; wrong++ (prior belief scored wrong by world);
  last_used = tick. Revision is in place; the slot is not freed.
- key new, store not full: insert; taught_tick = last_used = tick.
- key new, store full: evict one slot by the store's policy, then insert.

query() semantics: exact key match only (no backoff generalization in v1;
disclosed scope limit). Hit: last_used = tick; correct++ if prediction equals
expected else wrong++. Miss: return UNKNOWN (-2); no bookkeeping.

Two-hop composition (harness-level, authored comparison; the LEARNED part
under test is premise retrieval): r1 = query(a), r2 = query(b),
answer = sign(r1 - r2). Each premise rule used gets dependents++ (dependency
link registration). The comparison operator itself is authored infrastructure,
not claimed as learned.

Twin stores in ONE process: STORE-C (consequence policy) and STORE-R
(recency policy). Stages 1-5 feed both stores IDENTICAL episode sequences
(mirrored learn/query/twohop). Capacity 36 each; 32 rules pre-flood, so no
eviction before Stage 6 and both stores stay identical (verified by
DIVERGENCE_CHECK). Stage 6 floods both with the same 30 junk rules; eviction
diverges by policy. Stage 7 probes both separately. This is a controlled
within-subject comparison, not two experiments.

Frozen importance formulas:
- STORE-C eviction key: importance = 10*(correct - wrong) + 5*dependents
  - 8*contradictions + 1. Evict minimum; ties broken by lowest slot index.
  Age (last_used, taught_tick) does NOT enter except through the above terms.
- STORE-R eviction key: last_used tick. Evict minimum (least recently used);
  ties broken by lowest slot index.

## 3. Frozen developmental trajectory

Token codes. Subjects: dog=1, cat=2, spider=3, bird=4, fish=5, snake=6,
oak=20, rose=21, cactus=22, table=30, chair=31, sofa=32, n3=40, n7=41, n5=42,
eagle=50, owl=51, penguin=52, junk=100..129. Relations: legs=10, eyes=11,
wings=12, petals=20, thorns=21, height=22, drawers=23, double=30, half=31,
junkrel=99.

STAGE 1 (foundation): teach 8 animal rules, then immediate recall query each:
(1,10)->4, (1,11)->2, (2,10)->4, (2,11)->2, (3,10)->8, (4,12)->2, (5,11)->2,
(6,10)->0. Baseline recall recorded (informational).

STAGE 2 (unrelated interference): teach 24 disjoint-key rules, then query each
once: plants (20,20)->0, (20,22)->30, (21,20)->8, (21,21)->12, (22,20)->0,
(22,21)->50; furniture (30,10)->4, (31,10)->4, (32,10)->4, (30,23)->2,
(31,23)->0, (32,23)->0; numbers (40,30)->6, (40,31)->1, (41,30)->14,
(41,31)->3, (42,30)->10, (42,31)->2; birds (50,12)->2, (50,11)->2, (51,12)->2,
(51,11)->2, (52,12)->2, (52,11)->2. Note (30,10),(31,10),(32,10) share
relation legs=10 with animal rules on different subjects: tests relation-level
interference under exact-match (expected: none; honest check).

STAGE 3 (delayed reuse, zero re-teaching of Stage-1 rules since Stage 1):
- recall: query all 8 Stage-1 rules.
- 6 two-hop compositions with frozen expected sign(r1-r2):
  a. (1,10)=4 vs (3,10)=8 -> -1
  b. (4,12)=2 vs (5,11)=2 -> 0
  c. (6,10)=0 vs (1,10)=4 -> -1
  d. (3,10)=8 vs (2,10)=4 -> 1
  e. (5,11)=2 vs (4,12)=2 -> 0
  f. (1,10)=4 vs (30,10)=4 -> 0 (cross-domain: Stage-1 + Stage-2 premise)
  Premise rules get dependents++: dog 3, spider 2, bird 2, fish 2, snake 1,
  cat 1, table 1.

STAGE 4 (interference soak): 2 rounds x query all 24 Stage-2 rules
(informational accuracy; refreshes their recency, making Stage-1 rules stale
by age while retaining predictive value: the exact dissociation under test).

STAGE 5 (correction): record predictions of 12-rule collateral sample; then
contradict (2,10)->3 (cat legs corrected 4->3) and (5,11)->1 (fish eyes
corrected 2->1); probe both corrected (expect 3, expect 1); re-probe the
12-rule sample and count prediction changes.
Collateral sample (12): (1,10), (1,11), (3,10), (4,12), (20,20), (21,21),
(30,10), (31,23), (40,30), (41,31), (50,12), (52,11).

STAGE 6 (memory pressure):
- DIVERGENCE_CHECK: count of differing fields between STORE-C and STORE-R.
  Must be 0 (else the twin comparison is VOID).
- Flood both stores with 30 junk rules: (100..129, 99) -> obj=subj. Taught
  once each, never queried. Each store: 62 rules, capacity 36 -> 26 evictions
  by policy.
- Select the 8-rule pressure probe set BEFORE the flood (deterministic):
  (6,10) snake-legs, (2,11) cat-eyes, plus the 6 non-collateral-sampled
  Stage-2 rules with smallest last_used tick. All have wrong=0, contra=0,
  correct>=2 (predictively useful), and stale last_used (old by age).
- Expected mechanism behavior (informational): STORE-C evicts 26 junk
  (importance 1 < min non-junk importance 18); STORE-R evicts the 26 oldest
  last_used, which includes all 8 probe rules.

STAGE 7 (final probe): query all 8 probe rules on STORE-C and on STORE-R;
count correct. Informational: query the 2 corrected rules on STORE-C;
count junk retained per store (rel=99).

## 4. Frozen kill bars

BUILD-PASS requires ALL of K-D2-1 through K-D2-6. Any failure is BUILD-FAIL.
No partial credit. Bars are absolute counts on the frozen trajectory above.

- K-D2-1 (delayed reuse): Stage-3 two-hop score >= 5/6. Zero learn() calls on
  Stage-1 keys between Stage 1 teaching and Stage 3 (queries only).
- K-D2-2 (interference resistance): Stage-3 recall of Stage-1 rules >= 7/8
  (baseline 8/8 at Stage 1).
- K-D2-3 (correction): (a) both corrected rules predict new labels: 2/2;
  (b) collateral damage = 0: all 12 sample predictions identical before and
  after the contradictions.
- K-D2-4 (memory pressure): on the 8-rule probe set at Stage 7:
  STORE-C correct >= 7/8 AND STORE-R correct <= 2/8 AND STORE-C > STORE-R
  (strict). This is the consequence-vs-recency dissociation.
- K-D2-5 (determinism): 3/3 byte-identical runs of the same binary, exit 0,
  zero stderr.
- K-D2-6 (persistence): single znc compile; single binary run per pass;
  STATEHASH lines present for all 7 stages with strictly increasing tick;
  DIVERGENCE_CHECK = 0 pre-flood; stages are sequential code blocks in one
  main() so no process boundary exists between stages. Exact shell commands
  documented in the result.

## 5. Governance

- Pure Zag only: implementation, build, runs, and all analysis (grep/cmp/md5/
  diff only). No Python anywhere including scratch.
- No em dashes in any documentation (byte-verified before commit).
- Owned paths only: docs/lab/research-lead/overnight-20260928/devint_worker2/.
  Files: PREREG_DEVINT2.md (this file), devint2_learn.zag, DEVINT2_RESULT.md,
  DEVINT2_RAW_OUTPUT.txt.
- This worker reports BUILD-PASS or BUILD-FAIL only. No promotion to
  SURVIVES/BOUNDED/DOWNGRADED/KILLED; per Micah's 2026-09-29 directive those
  require the full 11-step frontier pipeline including independent red team.
- The two-hop comparison operator and the harness stage sequencing are
  authored infrastructure, not claimed as learned. The claims under test are
  retrieval persistence, revision locality, and retention policy only.
- Scope limits disclosed: exact-match retrieval only (no generalization/
  backoff in v1); integer-coded episodes; synthetic world with 2 deliberately
  false Stage-1 facts corrected at Stage 5.
