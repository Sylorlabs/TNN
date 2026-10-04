# PREREG H-DEVINT1: Developmental Integration Worker 1, Trajectory A

**Experiment ID:** H-DEVINT1
**Worker:** Developmental Integration Worker 1 (independent trajectory; Worker 2 runs a separate trajectory for comparison)
**Date (UTC):** 2026-09-30
**Status:** FROZEN. Committed alone before any implementation, build, or run.

## 1. Mission

Build ONE persistent continuing learner combining surviving TNN mechanisms and discover
whether their learned structures actually help each other. This is Trajectory A, run
independently; Developmental Integration Worker 2 runs an independent trajectory with the
same stage skeleton and synergy metric definitions so results can be compared.

This prereg defines the developmental sequence, the synergy metrics, and the BUILD-PASS /
BUILD-FAIL criteria. Per the 2026-09-29 cadence ruling, the builder reports BUILD-PASS or
BUILD-FAIL only; no SURVIVES claim and no L3 claim is made here.

## 2. The persistent learner

**Artifact:** a single Zag program `devint1.zag`, compiled exactly ONCE. One process runs
all eleven developmental stages in order. No reset of learner state between stages. No
recompilation between stages. If a reset or recompile between stages occurs, the
experiment is VOID.

**Staging interpretation (frozen):** the eleven stages are the experimenter's feed
schedule, i.e. the order in which the world presents experiences (a developmental
curriculum). The learner receives NO task-ID input and NO per-stage mode flag. Its
mechanisms (segment, form concepts, relate, hypothesize, proceduralize, detect
contradiction, inquire, revise, manage memory, reuse) run continuously on all input.
Stage boundaries exist only in the experiment log, verified by state-continuity checks.

**State continuity check (frozen):** at each stage boundary the program emits
`STATE-CONT <stage> <nconcepts> <nrules> <nsegs> <checksum>`, where checksum is a
deterministic hash over the concept table and rule table contents. Persistence holds iff
for every consecutive boundary pair, nconcepts and nrules are non-decreasing except where
the frozen revision/eviction semantics explicitly remove entries, and no boundary shows
both tables empty after having been non-empty. Any unexplained emptying is a reset and
voids the run.

## 3. Domain (hidden from the learner)

True morphemes (length 3, lowercase letters), unknown to the learner:

- M0 = "bik", M1 = "gup", M2 = "zol", M3 = "tav"

Raw episodes are concatenations of morphemes with no boundaries and no labels, e.g.
"bikgupzol". A small amount of character noise is injected in later stages (frozen below).

## 4. Integrated mechanisms (simplified faithful cores; simplifications disclosed)

1. **Segmentation (SEG-inspired core).** Lexicon induction: count substrings of length 2..4
   over the observed corpus; segment new strings by dynamic programming maximizing the sum
   of log(count+1) over segments (frequent substrings preferred; unseen bigrams fall back
   to single characters). SIMPLIFICATION vs SEG8: counts are small integers (no big-int
   adaptive digit budget); greedy lexicon rather than exact T_n counting. The core
   idea retained: segmentation from induced substring statistics, no supplied boundaries.
2. **Concepts.** A segment recurring at least twice becomes a concept with a numeric ID.
   Concept table: bounded (cap 24), entries (pattern bytes, count, id).
3. **Relations.** Concept bigrams (C_i followed by C_j) with counts, bounded table.
4. **Causal hypotheses.** Rules "C_i predicts C_j next" with support and refute counts and
   states PROVISIONAL / ACTIVE / ROLLED_BACK (REVISE-inspired core). Rule becomes ACTIVE
   at support >= 3 with zero refutes. SIMPLIFICATION vs H-REVISE9: no peeling protocol;
   contradiction demotes ACTIVE to PROVISIONAL, a second contradiction rolls back;
   rolled-back rules are retained as evidence (non-destructive).
5. **Procedures.** Concept-level substitution procedure. Frozen DSL ops: MAP (apply the
   learned concept pairing table) and COPY. Learning = inducing the pairing table from
   examples. The procedure task: given a concept sequence, output the paired sequence.
6. **Contradiction.** An observation contradicting an ACTIVE rule's prediction, or a
   concept appearing split across a boundary it previously owned, is logged as a
   contradiction event.
7. **Inquiry.** When two ACTIVE rules predict different next-concepts for one context,
   the learner emits an INQUIRY requesting the discriminating episode; the world provides
   it next.
8. **Revision.** Contradiction protocol from (4); plus representational refinement: if a
   concept is contradicted in a sub-context, the learner attempts a SPLIT (replace one
   concept by two whose concatenation equals it, both recurring afterward).
9. **Memory management.** Bounded store. Two eviction policies run on twin learner states
   (see section 6): importance-weighted (importance = causal support + reuse count +
   concept count) vs recency-only (LRU).
10. **Reuse.** Delayed episodes after memory pressure test reuse of invented concepts and
    the learned procedure.

## 5. Frozen developmental sequence

- **S1 raw exposure:** 12 raw episodes (morpheme concatenations, lengths 2..4 morphemes),
  no labels.
- **S2 segmentation:** lexicon built from S1 corpus; segment 6 new episodes; emit
  segments.
- **S3 concepts:** concepts formed from recurring segments; emit inventory.
- **S4 relations:** concept bigrams counted over S1+S2 concept sequences.
- **S5 causal hypotheses:** induce "C_i -> C_j" rules; confirm to ACTIVE at support >= 3.
- **S6 procedures:** substitution procedure learning. Pairing (frozen, hidden): M0<->M2,
  M1<->M3 (i.e. bik<->zol, gup<->tav). Examples: input concept sequence -> paired output
  sequence. Criterion: 5/5 correct on held-out examples. Record examples-to-criterion.
- **S7 contradiction:** 4 episodes contradicting one ACTIVE causal rule; 2 episodes where
  a concept's boundary is violated (refinement trigger).
- **S8 inquiry:** the two competing rules from S7 trigger an INQUIRY; the world supplies
  the discriminating episode; log which rule survives.
- **S9 revision:** apply the contradiction protocol; attempt concept SPLIT on the
  boundary-violated concept; measure accuracy on the contradictory contexts before/after.
- **S10 memory management:** inject 20 distractor episodes (random morpheme orders plus
  4 novel distractor morphemes "wex", "qiv") to exceed capacity; evict under both
  policies on twin states; then measure next-concept prediction accuracy on 10 held-out
  episodes using surviving knowledge.
- **S11 later reuse:** 6 delayed episodes reusing original morphemes in novel orders;
  test (a) concept recognition (fraction of segments mapping to pre-S10 concepts),
  (b) procedure reuse (apply the S6 pairing to a novel sequence, 3/3 correct).

## 6. Frozen synergy metrics

Each metric compares a treatment learner state against a control twin state. Both twins
are persistent across their stages inside the same single process; the control differs
only by the named disabled channel. This is measurement apparatus, not a second
deliverable; the deliverable is the single integrated learner.

- **S1 concepts -> procedure learning.** Treatment: procedure induction may reference the
  invented concept vocabulary (concept IDs). Control: procedure induction over raw
  segment strings with concept IDs disabled (same examples, same DSL otherwise).
  Metric: examples-to-criterion n_treat, n_ctrl. Synergy iff n_treat < n_ctrl.
  Report the delta.
- **S2 causal knowledge -> memory decisions.** Treatment: eviction by importance
  (causal support + reuse count + concept count). Control: eviction by recency (LRU).
  Metric: next-concept prediction accuracy on the 10 held-out episodes after eviction,
  acc_treat vs acc_ctrl. Synergy iff acc_treat > acc_ctrl.
- **S3 contradiction -> representational refinement.** After S7/S9, count refinement
  events: a concept replaced by a SPLIT (two concepts whose concatenation equals the
  old pattern, each recurring at least twice afterward) counts as refinement; plain
  deletion does not. Control twin: delete-only (no SPLIT attempted). Metric:
  refinement event count, and accuracy on the contradictory contexts before vs after
  S9, for treatment vs control. Report both; synergy is descriptive here.
- **S4 segmentation -> concept induction.** Treatment: concepts induced from the
  SEG-core segmentation. Control: concepts induced from fixed-width-3 chunking of the
  same episodes. Metric: episodes until the true 4-morpheme inventory is fully covered,
  and spurious concept count (concepts not equal to a true morpheme) at that point.
  Synergy iff treatment reaches full coverage with fewer spurious concepts.

## 7. Frozen BUILD-PASS / BUILD-FAIL criteria

- **B1 persistence:** one compilation; all 11 stages in one process; STATE-CONT checks
  satisfy section 2 (no unexplained emptying). Determinism: 3/3 runs byte-identical.
- **B2 stage function:** every stage's functional check passes: S2 emits segments; S3
  concept inventory non-empty; S5 at least one rule reaches ACTIVE; S6 procedure reaches
  5/5 criterion in both treatment and control; S7 contradiction events logged (>= 1);
  S8 INQUIRY emitted and answered; S9 revision applied (>= 1 demotion or rollback);
  S10 eviction occurs under both policies; S11 reuse measured.
- **B3 synergy measured:** all four metrics computed with valid treatment/control twins;
  deltas reported with exact integers.
- **B4 governance:** pure Zag (implementation, builds, runs, analysis via shell tools
  only; zero Python at any stage); no em dashes in documentation (byte-verified).

**BUILD-PASS iff B1 and B2 and B3 and B4.** Otherwise BUILD-FAIL. Negative synergy
deltas do NOT fail the build; they are reported honestly as data.

## 8. Coordination note

Worker 2 runs an independent trajectory. Recommended divergence to maximize comparison
value: different surface alphabet/morpheme set and/or a different procedure family
(e.g. repetition/deletion rather than substitution), keeping the same 11-stage skeleton
and the same four synergy metric definitions. Comparison point: whether synergy deltas
replicate across trajectories.

## 9. Deliverables and paths

All work under `docs/lab/research-lead/overnight-20260928/devint_worker1/` (owned paths
only):

- `PREREG_DEVINT1.md` (this file; committed alone)
- `devint1.zag` (implementation; committed after the prereg)
- `DEVINT1_RESULT.md` (results; BUILD-PASS or BUILD-FAIL on the frozen criteria)
- `DEVINT1_RAW.txt` (raw program output; md5 recorded)

No binaries committed. No paths outside `devint_worker1/` staged.
