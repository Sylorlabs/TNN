# PREREG: DDES t*=0 Soundness Repair, Wave 3 (R3)

Frozen before any implementation. This prereg commits the repair
specification and the repair kill bars for wave 20260930-1421pdt.
Any amendment must be committed transparently and re-frozen before
implementation; no bar may be altered after seeing results.

## Provenance

NEW prereg, written by worker DDES for wave 20260930-1421pdt.
Repair design inherited from PREREG_DDESREPAIR2.md
(wave-20260930-1121pdt, committed alone at d31e901b0) and the
white-box diagnosis in this lane's DIAGNOSIS.md. Wave-2 repair
implementation ddesr2.zag was validated by this worker (A-E block
byte-identical to DDES_RAW.txt; 3/3 runs byte-identical) but its
implementation commit never landed, so this wave re-freezes,
re-implements from the frozen BUILD-PASS source, and re-runs.
World F is the adversary's sealed soundness world (e40bdfc9b).
World F2 is a NEW sealed boundary world designed fresh in this
prereg (two-hop 0-delay cascade), frozen before any implementation
exists. Nothing in this prereg is copied from a tool result; world
tables are restated from PREREG_DDES.md, PREREG_DDESREPAIR2.md, and
the hand-derived expectations below.

## Provenance header (machine-checkable, standing rule 2026-09-23)

- RENDER_SHA: N/A (no render; pure Zag experiment).
- FIRST_RENDERED_WAVE: N/A.
- COMPONENT_LINEAGE: prereg text new this wave (R3; World F2 new);
  implementation to be written fresh from ddes.zag @ 56db8d606
  (BUILD-PASS source) plus this spec; World F inherited from the
  adversary e40bdfc9b; Worlds A-E inherited from PREREG_DDES.md.
- NEW_KNOWLEDGE_CLAIM: whether the eff_waits repair closes the t*=0
  hole on World F and the new sealed World F2 with zero A-E
  regression.

## Target

DDES lineage at 56db8d606 (BUILD-PASS, strong L2 guided generation,
NOT L3). Adversary finding e40bdfc9b: ATTACK-SUCCEEDS via K2
(sealed soundness world). The frozen K-NX1 through K-NX8 verdicts
stand; none of the frozen K-NX worlds has t*=0.

## The bug (restated from DIAGNOSIS.md)

Sealed World F: H0 = [(X,Y,0)] (0-delay rule). H1 = [(X,Z,7)].
The disagreement frontier selects (Y, t*=0). The unrepaired
synthesize_plan emits [S,OY] with zero waits. The execution model
fires rules only on W ticks; the S action sets X but fires no rules.
With zero waits, OY reads pre-propagation state (0). The analytic
predictor (observation of V at end of plan is 1 iff arrival[V] <= t*)
claims H0 predicts 1. When truth is h0, the unrepaired mechanism
eliminates the TRUE hypothesis and converges to h1: silent wrong
convergence (CONVERGE-OK printed, false hypothesis surviving).

## Repair specification (frozen)

The execution model and the analytic predictor must agree on the
effective wait count. Rules fire only on W ticks, so an observation
must follow at least one W tick to reflect any propagation.

- Add a generic helper eff_waits(t_star) = max(t_star, 1).
- synthesize_plan: wait while cur_t < eff_waits(t_star)
  (was: cur_t < t_star).
- predict: observation is 1 iff arrival[V*] <= eff_waits(t_star)
  (was: arrival[V*] <= t_star).
- Boundary detection and flag: when the derived target satisfies
  t_star == 0, the derivation path must emit the exact trace line
  `FLAG TSTAR-ZERO-BOUNDARY floor=1` immediately after the TARGET
  line and before the PLAN line. This is the mechanism detecting and
  flagging the unsound boundary condition instead of passing through
  it silently. The flag is a detection marker, not a branch on any
  delay value, variable id, or world id.
- No other logic changes. The clamp and the flag are generic boundary
  conditions on the derived target t*, of the same kind as the
  existing null-schema fallback and the n<1 guard in z_alloc.
- ISA ruling respected: no new core operation, no domain regularity
  detector, no new modes, bridges, handlers, or semantic cases.
- One-System Rule: the repair adds learner-external machinery only as
  a boundary clamp; capability comes from the same guided derivation,
  not a new subsystem. Accounting fields are reported in the result.

For all frozen K-NX worlds (t* >= 1), eff_waits(t*) = t* and the flag
never fires, so the repaired binary must behave identically to
56db8d606 on Worlds A through E.

## Test worlds (frozen)

Worlds A, B, C, D, E exactly as in PREREG_DDES.md (same rule tables,
same configs, same expected plans and convergence).

World F (adversary sealed soundness world, regression world):
H0 = [(X,Y,0)]. H1 = [(X,Z,7)]. Both truth configs.
Expected after repair:
- truth h0: TARGET V*=2 t*=0 schema=1; FLAG TSTAR-ZERO-BOUNDARY
  floor=1; PLAN [S,W,OY]; EXEC real=1; PRED h0=1 h1=0;
  SURVIVE h0; ELIM h1; CONVERGE-OK.
- truth h1: TARGET V*=2 t*=0 schema=1; FLAG TSTAR-ZERO-BOUNDARY
  floor=1; PLAN [S,W,OY]; EXEC real=0; PRED h0=1 h1=0;
  ELIM h0; SURVIVE h1; CONVERGE-OK.

World F2 (new sealed boundary world, designed in this prereg):
H0 = [(X,Z,0),(Z,Y,0)] (two-hop 0-delay cascade). H1 = [(X,Y,3)].
Hand derivation (frozen): set-X arrivals H0 = [X=0,Z=0,Y=0];
H1 = [X=0,Z=INF,Y=3]. Frontier: Z disagrees (0 vs INF), t=0;
Y disagrees (0 vs 3), t=0; tie broken to lowest variable id, so
V*=1 (Z), t*=0, schema=1. Repaired plan [S,W,OY] is wrong here:
the observed variable is Z, so the plan is [S,W,OZ].
Expected after repair:
- truth h0: TARGET V*=1 t*=0 schema=1; FLAG TSTAR-ZERO-BOUNDARY
  floor=1; PLAN [S,W,OZ]; EXEC real=1 (first W tick fires the
  0-delay cascade X->Z->Y); PRED h0=1 h1=0; SURVIVE h0; ELIM h1;
  CONVERGE-OK.
- truth h1: TARGET V*=1 t*=0 schema=1; FLAG TSTAR-ZERO-BOUNDARY
  floor=1; PLAN [S,W,OZ]; EXEC real=0 (3-delay rule not yet fired);
  PRED h0=1 h1=0; ELIM h0; SURVIVE h1; CONVERGE-OK.
Unrepaired baseline would emit [S,OZ] with zero waits and, on
truth h0, eliminate the true hypothesis (same silent-wrong class).

## Repair kill bars (all must pass for REPAIR-PASS; builders report BUILD-PASS/BUILD-FAIL only)

- K-R3.1 (t*=0 condition detected and flagged): all four boundary
  configs (F cfg0/cfg1, F2 cfg0/cfg1) contain the exact line
  `FLAG TSTAR-ZERO-BOUNDARY floor=1` between the TARGET line and
  the PLAN line. Kill: the flag is absent on any boundary config,
  or appears on any of Worlds A through E.
- K-R3.2 (no silent wrong convergence): on all four boundary
  configs the run prints CONVERGE-OK and the surviving hypothesis
  matches truth (cfg0: SURVIVE h0 and ELIM h1; cfg1: ELIM h0 and
  SURVIVE h1). The emitted plan is exactly [S,W,OY] on World F and
  exactly [S,W,OZ] on World F2; zero-wait plans are forbidden at
  the boundary. Kill: any config eliminates the true hypothesis,
  fails to converge, or emits a plan with zero W ticks before the
  observation.
- K-R3.3 (zero regression): the Worlds A through E output block
  (first 67 lines) is byte-identical to the frozen reference
  docs/lab/research-lead/overnight-20260928/ddes/DDES_RAW.txt
  (diff empty). The plans_built counter reads 8 after the E
  section; the full run (A-E plus F plus F2) reads
  plans_built=12 and SUMMARY ok=13/13. Kill: any byte difference
  in the A-E block, or a counter mismatch.
- K-R3.4 (determinism): 3/3 runs byte-identical (md5 match),
  exit 0, zero stderr bytes on every run. Kill: any divergence,
  nonzero exit, or any stderr byte.
- K-R3.5 (purity): pure Zag only. Zero Python at any stage
  (implementation, build, run, analysis). Zero em-dash and zero
  en-dash bytes in all committed files (byte-checked).
  Kill: any Python use or any forbidden byte.
- K-R3.6 (no new enumeration): static audit of the repaired
  synthesis path. The repair must not introduce any
  candidate-generating loop, length constant, or comparison
  between assembled plans. Kill: any such construct.

## One-System Rule accounting (frozen fields to report)

Cognition source lines added, new hardcoded semantic cases
(frozen expectation: 0), new modes (0), new bridges (0), new
task-specific handlers (0), learner-state structures created
(expected: none; the flag is a trace marker and eff_waits is
stateless).

## Commit order

This prereg is written before any implementation. ORDER.txt in this
lane records the creation order. The implementation commit must be
a strict descendant of the prereg commit; verified via
git merge-base --is-ancestor before the result is adopted.

No em-dashes in this documentation.
