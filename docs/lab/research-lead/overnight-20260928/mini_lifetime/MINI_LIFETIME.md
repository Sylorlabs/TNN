# Mini-Lifetime: Causal Experiment Design

**Status:** DESIGN ONLY. DRAFT-NOT-FROZEN. No implementation, no worlds
generated, no runs executed.
**Date:** 2026-10-01. **Verdict:** MINI-LIFETIME-COMPLETE (design).

## 0. What this is

A freezable design for the mini-lifetime causal experiment ordered by
Micah 2026-10-01: one continuing learner, sequential A-mini to B-mini
to C-mini stream, primary comparison of frozen TNN-2 (Build A) against
the reuse-path variant (Build B), with H3-lite Node 1 held separate.
It tests the lifetime track as a scientific instrument and marks exact
boundaries (revision correctness, cost bending, reuse observability)
without shrinking the full-lifetime AGI target to fit TNN-2.

The full five-world protocol v2 sequence needs 2,500 to 3,500 node
allocations on a 1,024-node architecture (lifetime scope, dffbdbbe7).
It does not fit. This design fits a three-world sequence in 500 to 600
nodes and reports FULL-LIFETIME FEASIBILITY separately and honestly.

## 1. Builds

### Build A: frozen TNN-2

The frozen binary identified as f4de7ff46 in protocol v2 Section 19
(D3). Cognition frozen and untouched. Source hash, binary hash, and
protocol hash recorded at the freeze commit. This is the control arm:
procedures are causally inert at query time (shadow-fact finding
6fa7dd2ec), so measure 7.5 is expected trivially zero and reported as
not-applicable-architectural, not as a finding.

### Build B: reuse-path variant (prerequisite, unfrozen)

Implements exactly the MINIMAL reuse path from
`tnn2_reusepath/REUSE_PATH_DESIGN.md` Section 6.1, the five items:

1. MAP-lookup branch in `ev_query` before `activate`: MAP-first
   ordering, fallback to facts on execution failure (-999999).
2. Delete the shadow teach at `promote_graph:541`.
3. Liveness: MAPs included in the `decay` sweep; `is_superseded`
   filter on the MAP lookup; live-MAP-wins rule for mixed states.
4. Contradiction retargeted at the MAP; no shadow fact taught on MAP
   revision; supersede-and-teach-fact on revision failure.
5. MAP selection: most-recent live MAP by `field24`, with the
   selection call site documented as the target-selection seam.

Explicitly OUT of Build B: portable procedures (value traces remain;
literals stay baked in), target-selection scoring, composition via
inlining, general revision. `t2_revise_graph` is UNCHANGED, including
its acceptance criterion (`out != -999999`, never `out == new_o`).
Build B therefore addresses the first C0-D cause (query-path bypass)
and deliberately does not address the revision-correctness hole.

Build acceptance (before the mini-lifetime freeze):

- Exact source diff against the frozen base, committed and hashed.
- 3/3 byte-identical self-check runs.
- Draft K-REUSE-1 (query-time MAP execution with MAP read preceding
  any `activate` hit) and K-REUSE-2 (no shadow facts) from the reuse
  design Section 7, run on a sealed micro-world by an independent
  checker. Both must PASS or Build B is rejected.
- Corruption-detector layout compatibility: tag-20 MAP layout,
  field-20 root, field-24 promotion index, field-28 answer are
  unchanged by Build B. Verified by inspection before any lifetime
  run, or the detector spec (protocol v2 Section 6.2) is updated
  first.

### What "no source edits" means

No source edits after the freeze commit. No per-world recompilation.
No task labels compiled in. Build B is constructed, validated, and
hash-recorded BEFORE freezing; the runs perform zero builds. Any
rebuild after the freeze starts a new freeze cycle.

## 2. Worlds (3 subjects each)

Relation symbols (R_CHAIN) are bound by the world sealer to relation
ids from the frozen TNN-2 vocabulary; the binding is recorded in the
sealed manifest. Subject pools are disjoint across minis except where
cross-mini links are designed (B-mini). No direct fact for any
TRIAL-EXPECTED probe's (s, r) may appear in its teach stream
(protocol v2 Section 4.1).

### A-mini: foundation chains

- Subjects 1, 2, 3. Per subject s, teach stream (fixed order):
  - Chain: (s, R_CHAIN, 1000+s), (1000+s, R_CHAIN, 2000+s).
  - Redundant licensing path: (s, R_CHAIN, 3000+s),
    (3000+s, R_CHAIN, 2000+s). Same endpoint, alternative middle.
    Makes provenance nontrivial and gives C-mini two severable
    paths per subject.
- Sealed probes: 3 held-out chain queries (s, R_CHAIN), s in
  {1,2,3}, never taught. TRIAL-EXPECTED. Criterion 3/3.
- Probing schedule k=5 (protocol v2 Section 9). Records E(A-mini).
- Budget: 200 to 250 nodes (12 teaches + 3 promotions at 41 nodes
  each + probing overhead).

### B-mini: dependent domain (forward transfer probe)

- Subjects 11, 12, 13 (fresh). Per subject t, the chain is 3-hop with
  the middle link recruited from A-mini state:
  - Teach (t, R_CHAIN, 4000+t) and (2000+s_t, R_CHAIN, 5000+t),
    where the middle link (4000+t, R_CHAIN, 2000+s_t) is NOT taught;
    instead the trial must recruit the A-mini fact
    (1000+s_t, R_CHAIN, 2000+s_t) or (s_t, R_CHAIN, 1000+s_t) as the
    licensing premise. Concretely, B-mini chains pass through
    A-mini entities: teach (t, R_CHAIN, 1000+s_t) as the first link
    (novel fact referencing A's entity), then the trial recruits
    A's (1000+s_t, R_CHAIN, 2000+s_t) as the second link.
  - Mapping: t=11 uses s_t=1, t=12 uses s_t=2, t=13 uses s_t=3.
- Isolation-B is taught the A-referenced middle-link facts inside
  its own stream (same bytes the lifetime learner already holds),
  so T(A to B) isolates retention and recruitment, not missing
  information.
- Sealed probes: 3 B-chain queries (t, R_CHAIN), held out.
  TRIAL-EXPECTED. Criterion 3/3. Records E(B-mini).
- Budget: 200 to 250 nodes.

### C-mini: contradiction and revision (revision safety probe)

- Targets 3 of A-mini's licensing facts:
  - 2 facts that ARE in B-mini MAP provenance (shared; revision
    must propagate correctly and B probes must stay correct).
  - 1 fact that is NOT in any B-mini MAP provenance (unshared;
    revision must not touch B).
- V2-hole trap: one additional contradiction whose correct repair
  the trial cannot produce by literal patch alone. The trap probe
  checks the revised MAP's executed output against the true
  corrected answer (`out == new_o`), not merely successful
  execution. `t2_revise_graph` accepts any repair with
  `out != -999999`; if the learner's revision is accepted anyway,
  the probe records a V2-HOLE event.
- Sealed probes: 3 revised-A queries (corrected answers,
  LOOKUP-EXPECTED: they test the answering path after revision),
  3 B queries (must be unchanged, LOOKUP-EXPECTED), 1 V2 trap
  probe (LOOKUP-EXPECTED with white-box answer verification:
  returned value, MAP field-28, and `t2_exec` on the stored root).
- Budget: 80 to 120 nodes.

### Totals

500 to 600 nodes, 250 to 350 events. Pre-saturation with margin
(saturation near 488 events at the implied 2.1 nodes/event mix).

## 3. Procedure (normative)

Per protocol v2 Section 5, scaled to three minis:

1. Freeze commit records: world manifests and hashes, Build A hash,
   Build B source diff and binary hash, instrumentation field order,
   k=5, bar thresholds, evaluator identity. Freeze strictly precedes
   the first teach event.
2. Lifetime track, per build: initialize one blank workspace. Stream
   A-mini, then B-mini, then C-mini as one continuous teach sequence.
   The driver never labels the mini; cognition receives no
   world identifier (verified by inspection: no mini id reaches any
   `ev_*` call). After each teach stream, run that mini's sealed
   probes read-only. At each mini boundary, the driver takes a
   white-box snapshot and runs the corruption detector (protocol v2
   Section 6.2) and the theater guard (Section 6.1); snapshot hashes
   are committed to the run log.
3. Final retention sweep: all probe sets re-run on the same unbroken
   learner state.
4. Repeat steps 2 to 3 two more times: 3/3 byte-identical runs per
   learner. Any measure unstable across runs is reported as
   unstable, not as a result.
5. Isolation track (frozen Build A, canonical): iso-A (blank + A-mini
   stream), iso-B (blank + B-mini stream with embedded A facts),
   iso-C-skip (A-mini then B-mini streams, probes, no C-mini).
   Same determinism rule.
6. Variant spot check: variant-iso-B, 3/3 runs. E() invariance rule
   (Section 5).

No learner reset: one workspace id per lifetime learner, logged on
every event; a second initialization for the same learner voids the
run. No process reset between minis.

## 4. Instrumentation

Protocol v2 Section 6 event vocabulary applies unchanged: TEACH,
PROMOTE (with prov[]), EXEC, QPATH (fact_hit / map_exec / trial /
miss), REVISE, EVICT, POLICY (theater-guarded), FORGET,
CORRUPTION, THEATER_GUARD classifications, boundary snapshots.

Provenance annotation (driver-side log enrichment, no cognition
change; per Micah's provenance directive): every TEACH and OBSERVE
event is tagged with its source class: EXTERNAL (driver `ev_teach`),
OBSERVED (`ev_observe`), INFERRED (bootstrap self-teach),
REVISION (revision-derived). A later analysis must be able to
distinguish externally supplied evidence from the learner's own
inference. Self-generated facts must never silently become
independent evidence for the learner's own later inference in any
claim the run makes.

## 5. Controls

- **Trial-must-run (protocol v2 Section 4.1), per build.** The
  hash-verified validator confirms on the sealed streams that no
  TRIAL-EXPECTED probe's (s, r) has a direct fact `activate` would
  find first. Scaled void rule: if ANY of the 3 TRIAL-EXPECTED
  probes in a set resolves via fact_hit during validation, the
  mini fails design validation and its E() is VOID. (Scales the
  v2 "more than 2 of 10" rule: >20% of 3 rounds to 1.)
- **E() build-invariance.** E() counts teach/probe events, not node
  writes. Build B's changes (query path, promotion shadow) do not
  alter trial dynamics for held-out probes, so E_iso is expected
  build-invariant. The variant-iso-B spot check must equal
  frozen iso-B E() exactly across 3/3 runs. If it differs, the
  invariance claim is VOID and no T() ratio may be reported for
  Build B until a full per-build isolation track is run.
- **No-reset verification.** Workspace id logged per event; exactly
  one initialization per lifetime learner per run.
- **No-label verification.** Driver code inspection: no mini
  identifier reaches cognition.
- **Budget guard.** If node budget fraction reaches 0.9 at any
  boundary, the run is flagged PRESSURE-CONFOUNDED: subsequent
  measures are reported as feasibility data (Section 8), not as
  kill-bar verdicts.

## 6. Kill bars and measures (mini-scoped)

All bars: lifetime track vs isolation controls, 3/3 byte-identical
runs, PASS/FAIL/VOID. Predictions are honest expectations, not
targets.

- **K-LT-1 (forward transfer, fact level).** T(A to B) =
  E_iso(B) / E_life(B) >= 1.25 AND at least one L1 event (A-origin
  fact in a B-mini MAP prov[]) with ablation confirmation (a
  counterfactual re-run withholding that fact increases E(B) or
  breaks B probes). Predicted PASS on both builds: B-mini is
  designed to depend on A's facts; this bar tests the machinery.
- **K-LT-4a (surgical revision safety).** Post-C: B probes 3/3
  unchanged AND revised-A probes 3/3 correct AND the unshared-A
  control probe correct. Predicted PASS on both builds (revision
  is provenance-scoped).
- **K-LT-4b (revision correctness).** V2 trap probe: revised MAP's
  executed output equals the true corrected answer. Predicted FAIL
  on both builds. Build B does not change `t2_revise_graph`'s
  acceptance criterion, so the wrong-but-running hole persists by
  construction. The FAIL is the finding: it marks the exact
  boundary the reuse path does not cross.
- **K-LT-2 (retention within budget).** Final sweep: A-origin
  probes 3/3 and B probes 3/3 with budget fraction < 0.9.
  Predicted PASS on both builds.
- **7.5 (reuse of old executable structures).** EXEC event counts
  with origin_mini earlier than event mini. Build A: expected 0,
  reported N/A-ARCHITECTURAL (shadow-fact finding), not a finding.
  Build B: expected >0 on re-queries of promoted (s, r). Reported
  honestly as same-instance reuse, NOT cross-domain transfer
  (K-LT-3 is out of scope for the mini; no D world).
- **DYN-1 (per-experience cost constancy).** Per v2 Section 7.8:
  per-experience node/edge deltas per mini boundary. Predicted
  FLAT on both builds. The A-vs-B comparison is the test: does
  MAP-first query bend the cost curve? Honest prediction: no
  (Build B removes ~1 shadow-fact node per promotion and adds
  frame allocations per MAP-hit query; the structural write sites
  per event are unchanged).

OUT OF SCOPE for the mini (reported as such, not silently
dropped): K-LT-3 (needs a D world), K-LT-5w/K-LT-5s (needs an A'
return; H3-lite Node 1 stays separate per directive), K-LT-2
beyond budget (needs the pressure regime; characterized instead
by the budget guard in Section 5).

## 7. Primary comparison: Build A vs Build B

The causal question: what changes when promoted procedures become
first-class answerers?

| Measure | Build A (frozen) | Build B (reuse variant) |
|---|---|---|
| EXEC events (7.5) | 0 (N/A architectural) | >0 expected on re-query |
| QPATH on re-query | fact_hit (shadow fact) | map_exec |
| E(A-mini), E(B-mini) | baseline | equal or slightly lower |
| K-LT-1 T(A to B) | PASS expected | PASS expected |
| K-LT-4a | PASS expected | PASS expected |
| K-LT-4b | FAIL expected | FAIL expected (criterion unchanged) |
| DYN-1 | flat | flat expected |
| K-LT-2 retention | 3/3, 3/3 | 3/3, 3/3 |
| Probe scores | baseline | identical answers expected |

The honest headline, if predictions hold: Build B changes the
answering mechanism (procedures observably execute; EXEC becomes a
real log event; contradictions retarget at MAPs) without changing
probe scores, learning costs, or the revision-correctness hole.
That is exactly the reuse design's Section 6.3 prediction: scores
unchanged, architecture gains the observable reuse event. Any
deviation (score change, E() change, DYN-1 bend, K-LT-4b flip) is
a major finding and triggers re-verification before any claim.

Consequence-reentry observation (instrumented, not claimed):
C-mini on Build B exercises the full re-entry loop at the procedure
level: contradiction (experience) to MAP revision (retained
consequence) to later query answering via the revised MAP (changed
decision), with the EXEC/QPATH log as the signature. The mini is
therefore also the instrument on which consequence-driven
adaptation claims can later be tested.

## 8. Reporting (two separate sections)

### MINI-LIFETIME RESULT

Per-build kill-bar verdicts (K-LT-1, K-LT-4a, K-LT-4b, K-LT-2),
the A-vs-B comparison table with measured values, EXEC/QPATH
distributions, DYN-1 profiles per mini boundary, L1 ablation
evidence, boundary snapshot hashes, CORRUPTION counts (expected
zero pre-saturation; any nonzero is reported with the detector's
classification), and the E() invariance check outcome. Every claim
carries its white-box log signature or it is not a finding.

### FULL-LIFETIME FEASIBILITY

Separate section, reported regardless of mini outcome:

- The full five-world protocol needs 2,500 to 3,500 node
  allocations (scope dffbdbbe7); the architecture holds 1,024.
  Saturation arrives during WORLD B under any plausible mix.
- Beyond saturation every new node triggers `evict_node`
  (~2.5M scans) and silent MAP-root corruption risk; per-event
  cost jumps ~100x; measures past that point characterize
  corruption artifacts, not the phenomena they name.
- Enlarging the tables does not fix it: every scan loop iterates
  full table size, so a 10x table pushes saturation out while
  making every query hit cost ~380k to 4.4M scans. The root cause
  is linear scans with no indexing plus destructive eviction.
- The mini's budget-guard flag (Section 5) is the empirical
  anchor: the largest clean pre-saturation lifetime demonstrated
  on TNN-2, and the point where honesty requires the feasibility
  section instead of further kill bars.

## 9. Prerequisites and ordering

1. Build B constructed from the reuse design, acceptance bars
   K-REUSE-1/K-REUSE-2 passed, hashes recorded. (Independent
   builder + checker; builder must not seal worlds.)
2. Worlds designed and sealed by an independent sealer; validator
   confirms the trial-must-run rule per build on hashes only.
3. Freeze commit (Section 3 item 1) strictly precedes the first
   teach event.
4. Runs execute; evaluator (named, no world-content access beyond
   hashes until evaluation) reports Section 8.

H3-lite Node 1 does not enter this run matrix. Its weak K-LT-5
claim is evaluated under its own prereg (currently EXPLORATORY
per the E3 discrepancy); it joins a lifetime run only after its
causal effect is established cleanly.

## 10. Standing metrics (this design)

- RESEARCHER-OWNED STRUCTURAL DECISIONS: builds, worlds, bar
  thresholds, instrumentation spec, validation rules (the
  researcher's legitimate role: designing the test).
- LEARNER-OWNED STRUCTURAL DECISIONS: 0 (design only; every MAP,
  fact, revision, and eviction during runs will be counted from
  logs when run).
- SOURCE-ENUMERABLE FORMS: all world content (researcher
  designed).
- SUF DECISIONS: 0. LEARNER-INTERNAL CRITERIA: 0.
- REUSE EVENTS: 0 (to be counted). REVISION EVENTS: 0 (to be
  counted). CORRUPTION EVENTS: 0 (to be counted).
- COGNITION LINES: 0. MODES: 0. BRIDGES: 0. HANDLERS: 0.
- SEMANTIC CASES: 0.
