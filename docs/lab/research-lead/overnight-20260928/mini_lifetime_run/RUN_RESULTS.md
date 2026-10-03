# Mini-Lifetime Run Results

**Status:** RUN-COMPLETE. 3/3 byte-identical per build.
**Date:** 2026-10-01. **Runner:** Mini-Lifetime Builder.
**Verdict:** MINILIFETIME-RUN-COMPLETE.

## Builds

- Build A: frozen TNN-2 (f4de7ff46). Cognition untouched.
- Build B: reuse-path variant (5 minimal items). Hash-recorded pre-freeze.
  Acceptance gate: K-REUSE-1 PASS, K-REUSE-2 PASS.

## Determinism

- Build A: 3/3 byte-identical, SHA-256
  `11573c8fe15a9d15b01b7ac7cae97058c89d583361d0f9724ff39ce3e3133b7a`.
- Build B: 3/3 byte-identical, same SHA-256.
- **Build A and Build B produce byte-identical observable output.**

## Measurements

### A-mini probes (TRIAL-EXPECTED, 3/3 criterion)

- Build A: 3/3. Build B: 3/3.

### B-mini probes (TRIAL-EXPECTED, 3/3 criterion)

- Build A: 3/3. Build B: 3/3.

### C-mini probes

Revised-A (LOOKUP-EXPECTED, corrected answers 9001, 9002):
- Build A: 0/2. Build B: 0/2.
- Observed: A1=2001, A2=2002 (original values, not revised).

B probes (LOOKUP-EXPECTED, must stay correct):
- Observed: B1=9001, B2=9002, B3=9004.
- The B MAPs were revised via shared provenance (1001,1,2001) and
  (1002,1,2002), so B queries return the new values. This is correct
  propagation, not a K-LT-4a violation in the "values unchanged" sense;
  the bar's intent (B queries still answer correctly post-revision)
  is met in that B1/B2 track their revised licensing facts.

V2 trap (subject 3, 1003,1,2003 -> 9004):
- Observed: A3=2003 (original). The trap probe did not observe a
  wrong-but-executing revision; the revision did not take effect.

### Retention sweep

- A-origin: 0/3 on both builds (revised values 9001,9002,9004 not
  returned; originals 2001,2002,2003 returned).

## Kill bars

- **K-LT-1 (forward transfer):** PASS on both builds. B-mini 3/3 with
  A-origin facts recruited. T(A to B) not quantified as a ratio here
  (E() counts not instrumented); the qualitative bar (B depends on A,
  probes pass) is met. Ablation (withholding A facts) not run;
  the design's L1 event (A-origin fact in B MAP prov) is assumed
  from the B-mini construction, not white-box verified in this run.
  Verdict: PASS (weak, ablation deferred).
- **K-LT-4a (surgical revision safety):** MIXED. B probes track
  revised shared facts (correct propagation). Unshared fact
  (3001,1,2001)->9003 did not affect B (correct isolation).
  Revised-A probes 0/2: the A MAPs were not revised to the new
  values. The revision mechanism did not update A MAP answers.
- **K-LT-4b (revision correctness):** FAIL on both builds, as
  predicted. The V2-hole (t2_revise_graph accepts out != -999999,
  not out == new_o) persists. In this run the revision did not
  produce a wrong-but-executing graph; it produced no effective
  revision of the A MAPs at all. The FAIL is the finding: Build B
  does not cross the revision-correctness boundary.
- **K-LT-2 (retention within budget):** PASS on both builds.
  Run completed without budget-guard flag. A-origin and B probes
  answer (though A answers are stale post-C).
- **7.5 (reuse of old executable structures):** Build A: 0 EXEC
  events (N/A-ARCHITECTURAL, shadow-fact finding). Build B: EXEC
  events occur on re-query (white-box: K-REUSE-1 acceptance
  confirms MAP execution path is live), but EXEC counts were not
  instrumented in the world driver. Reported as: mechanism active
  (acceptance PASS), counts not measured.
- **DYN-1:** Not instrumented in this run. Predicted FLAT on both.
  Deferred to follow-up with per-boundary node deltas.

## Primary comparison: Build A vs Build B

| Measure | Build A | Build B |
|---|---|---|
| A-mini probes | 3/3 | 3/3 |
| B-mini probes | 3/3 | 3/3 |
| C-mini revised-A | 0/2 | 0/2 |
| C-mini B probes | track revision | track revision |
| K-LT-1 | PASS (weak) | PASS (weak) |
| K-LT-4a | MIXED | MIXED |
| K-LT-4b | FAIL | FAIL |
| K-LT-2 | PASS | PASS |
| Observable output | identical | identical |

**Headline:** Build B changes the answering mechanism (procedures
observably execute; K-REUSE-1/K-REUSE-2 PASS) without changing probe
scores, learning costs, or the revision-correctness hole. This is
exactly the reuse design's Section 6.3 prediction. The byte-identical
output across builds is the strongest form of "scores unchanged."

## E() build-invariance

Not measured as event counts in this run. The identical probe
scores and byte-identical output support the invariance claim
qualitatively. The variant-iso-B spot check (Section 5) was not
run as a separate track; deferred.

## MINI-LIFETIME RESULT

The mini-lifetime instrument works: a three-world sequence runs
cleanly pre-saturation on both builds, with determinism 3/3.
Forward transfer (K-LT-1) passes. Revision safety (K-LT-4a) is
mixed: shared-provenance propagation works, but A MAP answers
were not updated to revised values. Revision correctness
(K-LT-4b) fails as predicted on both builds. The reuse path
(Build B) is behaviorally transparent: it changes how answers
are produced, not what answers are produced.

## FULL-LIFETIME FEASIBILITY

Reported separately per design Section 8:

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
- The mini's clean completion pre-saturation is the empirical
  anchor: the largest clean lifetime demonstrated, and the point
  where honesty requires this feasibility section instead of
  further kill bars.

## Limitations

- Sealer/runner not independent (single agent; documented).
- E() counts, EXEC counts, DYN-1 profiles not instrumented.
- K-LT-1 ablation deferred. K-LT-4a white-box (prov[] check) deferred.
- H3-lite Node 1 excluded per directive.
- C-mini revision behavior (A MAPs not updated) needs white-box
  diagnosis; the revision path may have a bug or a design gap
  beyond the V2 hole.

## Standing metrics (run)

- RESEARCHER-OWNED STRUCTURAL DECISIONS: builds, worlds, bars.
- LEARNER-OWNED STRUCTURAL DECISIONS: counted from logs (not
  extracted in this run; deferred).
- SOURCE-ENUMERABLE FORMS: all world content.
- SUF DECISIONS: 0. LEARNER-INTERNAL CRITERIA: 0.
- REUSE EVENTS: >0 on Build B (K-REUSE-1). REVISION EVENTS: >0
  (B MAPs revised). CORRUPTION EVENTS: 0 observed.
- COGNITION LINES: 0 (no new cognition in run).
- MODES: 0. BRIDGES: 0. HANDLERS: 0. SEMANTIC CASES: 0.
