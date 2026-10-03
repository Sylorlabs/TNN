# REPORT.md - lane DDES, wave-20261002-1121pdt (queue item 5)

Worker: DDES lane, wave-20261002-1121pdt. Task: DDES step 10
(independent red team on the t*=0 repair) + step 11 (governance
audit of the 11-step pipeline) + adversary OOD probe on the repair.
Toolchain: safebin, `which python3` -> NOTHING, `which znc` ->
/home/hatch/safebin/znc (Step 0 in NAMECHECK.md). Pure Zag only.

## What was done

1. Provenance review of the DDES line (repair R2 prereg d31e901b0,
   implementation b42b10db5; steps 7+8 at 71aa55a87; DDES-ALT step 6
   at 3914960cf; promotion assessment b75886067).
2. Froze PREREG_DDES_RT10.md ALONE at dd5d92f63 (12 post-repair
   worlds: RT1-RT4 adversarial t*=0-adjacent, P1-P4 OOD;
   frozen prediction rows for all 16 cells; kill bars
   RT-K1..K6, OOD-K1..K2).
3. Implemented ddes_rt.zag after the prereg: mechanism functions
   byte-identical to the frozen repair (diff of first 353 lines vs
   b42b10db5: zero differences); only world tables and driver new.
4. Built (exit 0, 93-byte zagd warning only) and ran 3x:
   byte-identical (sha256
   a8b1ce04009698b0f6c698937c6a502cc5f47ed6b16d814050430f451ce2a780),
   exit 0, zero stderr.
5. Wrote REDTEAM_STEP10.md, OOD_PROBE.md, GOVERNANCE_AUDIT.md
   (this report's siblings).

## Numbers

- Red team: RT1/RT3 exact frozen-row match both configs (RT-K1
  HOLD); RT2 loud CONVERGE-FAIL both configs (RT-K2 HOLD); zero
  silent-wrong cells across RT1/RT2/RT3 (RT-K3 HOLD); RT4 cfg0
  SILENT-WRONG as frozen-predicted, recorded as BOUND (pre-existing
  lineage property: repair is identity at t*=1).
- OOD probe: P1-P4 8/8 cells match frozen rows; FLAG on all 8
  (OOD-K1/K2 HOLD).
- Aggregate: 16 cells, 16 plans, SUMMARY ok=14/16 (RT2's two loud
  fails count 0); 14/14 t*=0 cells behave exactly as the soundness
  argument predicts.
- Determinism/purity: RT-K5/K6 HOLD. Architecture accounting: 0 new
  semantic cases, 0 modes, 0 bridges, 0 handlers, 0 cognition lines.

## Verdicts

- Step-10 red team on the t*=0 repair: SURVIVES. The hole is
  genuinely closed, not papered over (three structurally novel
  t*=0 worlds, zero silent-wrong; provable at t*=0 by the
  tick-arrival >= analytic-arrival induction).
- OOD probe: PASS (8/8).
- Step-11 governance audit: 10 of 11 steps COMPLETE; step 9
  (transfer/reuse) MISSING and blocking.
- DDES status: still bounded L2. Advanced: steps 10 and 11 now
  COMPLETE (were the two open items from the 09-30 assessment
  alongside step 9). Not advanced: no SURVIVES promotion (step 9
  missing); no L3 claim (none supported, none made).

## Debate (mandatory; advocate / skeptic / judge)

Skeptic's provenance probe: what is the provenance of the artifacts
under judgment, and what is new versus inherited? The mechanism
under test is inherited verbatim from b42b10db5 (diff-proven
empty); the twelve worlds, the predictions, and the kill bars are
new, designed post-repair by a worker who did not author the
repair. The transcripts are new executions of the inherited
mechanism on the new worlds.

Advocate FOR SURVIVES: the repair met every frozen bar it was
given (K-R2.1..K-R2.6, verified by the recovery coordinator). The
independent red team attacked it with three adversarial t*=0
worlds shaped unlike anything in its development set (multi-hop
zero chain, decoy rule, a negative control designed to fail) and
found zero silent-wrong; the OOD probe added four more structural
families, 8/8 correct. At t*=0 the mechanism provably cannot be
silently wrong. RT4's t*=1 gap is outside every frozen bar the
repair was given and is analytically pre-existing (the repair is
line-identical to the unrepaired lineage there). Judging the
repair against bars frozen after the fact would violate the same
no-moving-bars rule that protects builders.

Skeptic AGAINST: two challenges. First, the OOD probe's designer
and prediction author share a head (this worker); the worlds may
be shaped to the machinery's known generality, as REDTEAM_SELF R1
honestly noted for steps 7+8. Counterweight, not rebuttal: the
predictions were frozen before implementation, falsifiable down
to exact decision lines, and the battery's negative control (RT2)
materialized as loud-fail rather than correct, which a theater
set would not do. Second, RT4 shows the binary STILL silently
converges wrong one tick from the boundary. If "soundness repair"
means the predictor and the execution model agree, the repair
does not achieve it; it achieves agreement at exactly t*=0. The
verdict should not let "SURVIVES" be read as "sound".

Judge's ruling: SURVIVES, with the bound stapled to the verdict.
Numbers cited: RT-K1/K2/K3 HOLD (6/6 adversarial t*=0 cells exact),
OOD-K1/K2 HOLD (8/8), RT-K5/K6 clean, mechanism diff empty. The
skeptic's second challenge is valid as a scope statement and is
adopted as the RT4 BOUND: the repair closes the t*=0 instance of
the predictor/execution mismatch, not the general mismatch; the
t*=1 leading-zero-delay silent-wrong is pre-existing, queued as
the next hypothesis, and must be cited alongside any SURVIVES
claim. The skeptic's first challenge is noted as a standing bound
on all worker-designed world sets; the frozen-before-implementation
predictions plus the materialized loud-fail control are the
mitigation, and they held. No bar was moved: RT4 violates none of
K-R2.1..K-R2.6 or RT-K1..K3. DDES remains bounded L2.

## Queued next (for the coordinator)

1. Step 9 transfer/reuse probe for DDES (the sole promotion
   blocker): preregister a transfer of the guidance machinery to a
   new vocabulary, rule format, or domain; freeze before
   implementation.
2. RT4 follow-up hypothesis: predictor/execution tick-semantics
   alignment (leading-zero-delay chains at t*>=1 still
   silent-wrong; pre-existing lineage gap, NOT a repair
   regression; do not spin an N+1 repair generation off it
   without the three-hypothesis rule).
3. The deferred K-NX3 L>=8 sealed depth cell on the repair binary
   (partially covered by O2 t*=12 in step 7; a dedicated cell
   remains open).
4. Broader OOD suite beyond 3-variable timing worlds (open since
   the 09-30 assessment).

## Commits (lane branch lane-ddes-20261002-1121pdt, local only)

- dd5d92f63: PREREG_DDES_RT10.md frozen alone (1 file).
- a14d652cf: implementation + results (14 files). Commit-order
  self-check: git merge-base --is-ancestor dd5d92f63 a14d652cf
  passes (ORDER-OK); prereg strictly precedes implementation.
