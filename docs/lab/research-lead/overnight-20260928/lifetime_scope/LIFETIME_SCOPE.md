# Lifetime Scope: What Fits Under the Scaling Wall

**Status:** analysis only. **Verdict: LIFETIME-SCOPE-COMPLETE.**
Date: 2026-10-01. Parent task: scope what lifetime testing is
feasible given the scaling wall. This document does NOT revise the
lifetime protocol (v2, DRAFT-NOT-FROZEN, commit `dd745851e`); it
reports the feasible envelope and proposes a minimal viable test
for Micah's freeze decision (banked D4).

## 1. Method

All projections are arithmetic on the measured per-operation cost
table from `3eeb0d78e` (COST_ACCOUNTING.md, 3/3 byte-identical),
combined with the scaling analysis (`02804f782` / `bda26cf91`).
No new measurements. The event-mix model is the scaling worker's
stated model; per-world node budgets below are computed from the
protocol v2 world designs (Section 4) under explicit assumptions,
with ranges where world-design details are not yet fixed.

Structural constants (frozen source, read-only):
node table 1,024 slots; edge table 4,096 slots; `decay` scans all
4,096 edge slots on every event; `evict_node` costs 2,528,389 scan
steps per victim and silently corrupts surviving MAP roots
(`986c52fdc`).

Measured per-operation node deltas (from `3eeb0d78e`):
teach +1; query hit +0; query trial+promote +41; query miss +3;
observe contradict +2; revise (chain rewire) +6.

## 2. The feasible envelope

### 2.1 Saturation arithmetic

Busy mix (4.95 nodes/event): the 1,024-node table fills at
~207 events. Quiet mix (1.2 nodes/event): ~850 events. Empirical
anchor: the white-box inventory found 1022/1024 live nodes after
FW9 (nine worlds), consistent with fill-in within the low hundreds
of events at observed promotion rates.

Post-saturation, every new node triggers `evict_node` (2.5M scans)
plus silent MAP-root corruption risk. Per-event cost jumps ~100x
(busy: ~12.5M scans/event; quiet: ~3.1M). The stream then pays
mostly for the privilege of forgetting destructively.

**Envelope: a clean (pre-saturation, corruption-free) lifetime on
frozen TNN-2 is bounded at roughly 200 to 800 events and roughly
1,000 node allocations, depending on mix.** Beyond that, every
measure is confounded by eviction churn and zombie MAPs.

### 2.2 Per-world node budgets under protocol v2

Protocol v2 worlds use 10 subjects each with criterion 10/10 on
held-out probes. Because TNN-2 graphs are subject-bound (literals
baked in; transfer analysis 2026-10-01), each subject needs its
own promoted MAP for its probes to pass. Trial+promote costs 41
nodes per MAP.

WORLD A (10 subjects, 2-hop and 3-hop chains, redundant licensing):
- Teaches: ~50 chain links + ~50 redundant = ~100 nodes.
- MAP promotions: 10 subjects x 41 = 410 nodes.
- Probing overhead: probes every k=5 teaches; early probes miss
  (+3 nodes each) and build uncertainty nodes. Estimated 150 to
  300 nodes depending on E(A).
- **WORLD A alone: roughly 650 to 800 nodes, 60 to 80 percent of
  the entire node budget.**

WORLD B (10 subjects, dependent chains): same order, ~650 to 800
nodes. WORLD D (10 subjects, count/sum rebuild): same order.
WORLD A' (10 subjects): same order. WORLD C (contradictions and
revisions): smaller, roughly 50 to 150 nodes (contradict +2,
revise +6 each, plus probes).

**The five-world protocol v2 sequence needs on the order of
2,500 to 3,500 node allocations.** That is 2.5x to 3.5x the
1,024-node budget. The full sequence cannot complete
pre-saturation on frozen TNN-2. Saturation would arrive during
WORLD B under any plausible mix, and every subsequent measure
(K-LT-2 retention, K-LT-4 revision safety, K-LT-5 learning-rate
transfer, the final retention sweep) would be confounded by
eviction corruption rather than measuring the phenomenon it
names.

This is not a matter of world-design tuning. Ten subjects with
per-subject MAP promotion is ~410 nodes of irreducible procedure
cost per world before any fact or probing overhead. Four such
worlds exceed the budget on MAPs alone.

### 2.3 What fits and what does not

FITS in a clean pre-saturation envelope (under ~500 nodes,
under ~250 events):
- A two-world mini-lifetime A to B (3 subjects each): forward
  transfer K-LT-1 with E() ratios, L1 events with ablation,
  DYN-1 cost-constancy diagnostic. See Section 3.
- A three-world mini-lifetime A to B to C (3 subjects each,
  C small): adds K-LT-4a (surgical revision safety) and K-LT-4b
  (V2-hole trap). See Section 3.

DOES NOT FIT on frozen TNN-2:
- The full five-world v2 sequence (2.5x to 3.5x over budget).
- K-LT-2 (retention under interference) beyond budget: the
  protocol wants to characterize degradation, but degradation
  arrives as silent corruption (zombie MAPs), which invalidates
  the probe scores it would characterize. The CORRUPTION and
  ZOMBIE-STATE event types would fire, but the retention numbers
  would measure corruption artifacts, not interference.
- K-LT-5w/K-LT-5s on frozen TNN-2: predicted FAIL regardless
  (fixed trial order); the A to A' return cannot be reached
  cleanly.
- Any lifetime phenomenon requiring more than ~800 events of
  continuous experience: the architecture enters the destructive
  regime first.

ENLARGING THE TABLES DOES NOT FIX IT (scaling, Section 4):
every scan loop iterates full table size, not occupancy. A
10,240-node build pushes saturation to ~2k to 8k events while
making every query hit cost ~380k to 4.4M scans. Bigger is slower
and still fills. The root cause is linear scans with no indexing,
not the constants.

## 3. Proposed minimal viable lifetime test

Recommendation for Micah (not a protocol revision; the freeze
decision D4 remains his).

**Design: three-world mini-lifetime, A-mini to B-mini to C-mini,
one continuing learner, no resets, no task labels, 3/3
byte-identical runs, with isolation controls per world.**

- A-mini: 3 subjects, 2-hop chains, redundant licensing facts.
  ~30 teaches, 3 MAP promotions, probing to criterion.
  Budget: ~200 to 250 nodes.
- B-mini: 3 fresh subjects, chains whose premises include A-mini
  facts (same cross-subject design as v2 Section 4, scaled down).
  Budget: ~200 to 250 nodes.
- C-mini: contradictions targeting 3 of A-mini's licensing facts
  (2 shared with B-mini MAPs for the surgical test, 1 unshared),
  plus the V2-hole trap contradiction. Budget: ~80 to 120 nodes.

**Total: roughly 500 to 600 nodes, roughly 250 to 350 events.**
Fits pre-saturation with margin under the quiet-to-moderate mix
(2.1 nodes/event implied; saturation at ~488 events).

**Measures exercised:**
- K-LT-1 (forward transfer, fact level): T(A to B) with E()
  ratios and L1 events with single-fact ablation. Honest
  prediction: PASS (tests machinery, not a miracle).
- K-LT-4a (surgical revision safety): post-C B-mini probes
  intact. Honest prediction: PASS.
- K-LT-4b (revision correctness): V2-hole trap probe. Honest
  prediction: FAIL (wrong-but-running repair accepted).
- DYN-1 (per-experience cost constancy): the "write-mostly, not
  living" diagnostic across all three worlds.
- THEATER_GUARD, CORRUPTION detector, ZOMBIE-STATE sweep: all
  v2 instrumentation applies unchanged at this scale.

**What it discriminates:** whether the lifetime track itself
works as a scientific instrument (paired isolation controls,
white-box log signatures, byte-identical determinism) and whether
fact-level transfer plus surgical revision survive the
continuing-learner setting. A clean PASS on K-LT-1/K-LT-4a with a
clean FAIL on K-LT-4b would validate the track and mark the exact
revision-correctness boundary.

**What it does not test:** K-LT-2 beyond budget, K-LT-3
(architecturally blocked, predicted FAIL), K-LT-5w/K-LT-5s
(predicted FAIL on frozen TNN-2), long-horizon retention,
interference at scale. These require either TNN-3 (Section 4) or
are already answered by existing analyses.

**Event mix for the run:** teach-heavy early (A-mini
acquisition), probe-heavy at criterion checks, contradiction
events in C-mini. Probing schedule k=5 per v2 Section 9, with
the trial-must-run validation (v2 Section 4.1) applied to all
TRIAL-EXPECTED probes.

## 4. What TNN-3 needs for true lifetime

The scaling analysis states four requirements (Section 6):
(1) sublinear retrieval; (2) non-destructive, sublinear
reclamation; (3) amortization; (4) a retention policy with a read
path. Which binds first depends on the question asked.

**Binding engineering constraint: (1) and (2) together.**
Without sublinear retrieval, per-operation cost grows with
capacity, so no budget is ever big enough to be cheap. Without
non-destructive reclamation, every saturation event risks silent
corruption, so no long run is trustworthy. These two are the
reason the wall is at hundreds of events and the reason
enlarging the tables moves the wall without removing it. Any
TNN-3 that keeps linear workspace scans and destructive eviction
cannot run a lifetime longer than ~10^3 events no matter what
else it fixes. This is the constraint that must be satisfied for
a lifetime to RUN.

**Binding scientific constraint: (4), the retention policy with
a read path.** Suppose (1) through (3) were fixed and a million
events ran cheaply. The system would still be "write-mostly, not
living" (state dynamics `ee238d8d4`): constant per-experience
cost, duplicated structures on repeated experiences, zero
learner-owned retention decisions (forgetting `2726baf74`: eight
fixed researcher criteria, zero learner input). A cheap infinite
tape that records everything and prioritizes nothing is not a
continuing learner; it is a log file. The retention policy is
the constraint that must be satisfied for a lifetime to MEAN
anything. It is also the prerequisite the consequence-reentry
analysis (`7eab34ff2`) identifies: consequences of the system's
own activity must re-enter future decisions (M2/M3/M4), and
retention is the most load-bearing such decision.

**Amortization (3) is the bridge.** It is the observable that
connects the engineering to the science: if per-experience cost
declines (or at least does not explode) as experience grows, the
system is learning to learn its own maintenance. DYN-1 is the
standing diagnostic for exactly this. Currently DYN-1 is
predicted flat-then-catastrophic; a TNN-3 candidate should show
DYN-1 bending the right way before any capability claim is
entertained.

**Order of attack for TNN-3 design workers:** (4) first in
design priority (it determines what the other three are FOR),
(1) and (2) first in implementation priority (nothing runs
without them), (3) as the acceptance metric (DYN-1 must improve
or the redesign failed its purpose). Designing (1) and (2)
without (4) produces a fast amnesiac; designing (4) without
(1) and (2) produces a thoughtful system that still saturates
at hundreds of events.

## 5. Implications for the banked decisions

- D2 (H3-lite vs lifetime ordering): the mini-lifetime in
  Section 3 can run on frozen TNN-2 NOW and does not depend on
  H3-lite. It tests the track, not the policy machinery. H3-lite
  K-LT-5w needs the A to A' return, which does not fit; that
  bar awaits TNN-3 or a separately scoped two-world A to A'
  mini test (same 3-subject discipline, feasible at ~450 nodes).
- D3 (which builds): for the mini-lifetime, the reuse-path
  variant question matters (measure 7.5 is trivially zero
  without it, per the shadow-fact finding `6fa7dd2ec`). Recommend
  the run matrix include the frozen build as-is for K-LT-1 and
  K-LT-4 (which do not need MAP-first query) and note 7.5 as
  not-applicable on the frozen build rather than zero-as-finding.
- D5 (weak vs strong K-LT-5): neither fits the mini-lifetime;
  both are deferred to TNN-3. The weak K-LT-5 prereg
  (`0cab8938f`) already exists as an isolation-style test and is
  unaffected by this scoping.

## 6. Bottom line

The lifetime protocol v2 as designed is a 2,500 to 3,500 node
experiment on a 1,024 node architecture. It does not fit. The
shortfall is structural (per-subject MAP promotion at 41 nodes
each, linear scans, destructive eviction), not a tuning margin.

What fits: a three-world mini-lifetime (A to B to C, 3 subjects
each, ~500 to 600 nodes) that exercises K-LT-1, K-LT-4a,
K-LT-4b, and DYN-1 with full v2 instrumentation. This validates
the lifetime track as an instrument and marks the
revision-correctness boundary.

What TNN-3 needs, in order: retention policy with a read path
(design first), sublinear retrieval plus non-destructive
reclamation (implementation first), amortization as the
acceptance metric (DYN-1 must bend).

## Standing metrics

- RESEARCHER-OWNED STRUCTURAL DECISIONS: 0 (analysis only;
  the scoped test in Section 3 is a recommendation, not a
  decision; Micah owns D4).
- LEARNER-OWNED STRUCTURAL DECISIONS: 0
- SOURCE-ENUMERABLE FORMS: 0
- SUF DECISIONS: 0
- LEARNER-INTERNAL CRITERIA: 0
- REUSE EVENTS: 0
- REVISION EVENTS: 0
- COGNITION LINES: 0
- MODES: 0, BRIDGES: 0, HANDLERS: 0, SEMANTIC CASES: 0
