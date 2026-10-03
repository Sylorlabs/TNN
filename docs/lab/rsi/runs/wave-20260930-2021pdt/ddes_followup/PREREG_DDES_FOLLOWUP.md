# PREREG: DDES schema-persistence follow-up (ddes_followup)

Frozen before any implementation. Wave 20260930-2021pdt, lane ddes_followup.
This prereg commits the design and the kill bars. Any amendment must be
committed transparently and re-frozen before implementation; no bar may be
altered after seeing results. Builders report BUILD-PASS/BUILD-FAIL only.
No L3 claims: Criterion 0 (all four clauses conjunctive) is the mandatory
L3 gate and this experiment does not attempt it. DDES stays L2+ bounded
(strong L2 guided generation) unless a full 11-step pipeline says otherwise.

## Provenance

NEW prereg, written by worker ddes_followup for wave 20260930-2021pdt.
Design inherits the DDES R2 lineage at the 11:21 lane
(docs/lab/rsi/runs/wave-20260930-1121pdt/ddes/, PREREG_DDESREPAIR2.md,
implementation ddesr2.zag, BUILD-PASS with World F t*=0 soundness repair).
World F tables restated from that prereg. World G is new, designed and
frozen here, never seen by the DDES derivation path in any prior run.

## The question (one mechanism, one question)

Do DDES-generated experiment schemas persist and stay usable across a
scaffold disconnect? This is a standing metrics priority (genuine learning
persists after scaffold disconnect), and this lane gives it its first
instrumented measurement for DDES. One mechanism (DDES), one question
(persistence plus usability of the persisted schema after the derivation
scaffold is removed).

## Design

A single pure-Zag binary runs two phases.

Phase A: scaffold CONNECTED. Run the full DDES derivation on World F
(frozen regression world: H0=[(X,Y,0)], H1=[(X,Z,7)]), both truth configs.
Derivation yields the schema record R = (schema=1, V*=2, t*=0,
pred_h0=1, pred_h1=0). R is written into a dedicated learner-owned state
buffer (learner_state), separate from all derivation temporaries. The
trace emits the exact line:
`SCHEMA-RECORD schema=1 V*=2 t*=0 pred_h0=1 pred_h1=0`
Phase A must itself converge on both F configs (otherwise the persisted
record is meaningless).

Scaffold disconnect: a global phase flag moves to 2. Every
derivation-path function (compute_arrivals, compute_frontier,
synthesize_plan, predict, ddes_world) checks the phase on entry and
increments a violation counter if invoked during phase 2. The disconnect
is therefore instrumented, not merely a code path that happens to avoid
derivation. The trace emits `SCAFFOLD-CALLS n` at the end of phase 2.

Phase B: scaffold DISCONNECTED. Sealed World G (frozen below), both
truth configs. Phase B reads ONLY the persisted record R from
learner_state. It reconstructs the experiment directly from record
fields: [S] then W repeated eff_waits(t*) times then observe(V*), with
obs action = 4 - V* (the same generic mapping, no derivation). It
executes the plan once on the true world, compares the real observation
against the persisted predictions (pred_h0, pred_h1), and eliminates the
mismatch. No arrival computation, no frontier computation, no plan
synthesis, no predictor call. The trace emits CONVERGE-OK or
CONVERGE-FAIL per config.

## World G (sealed, frozen here; derivation never sees it)

Variables: X=0, Z=1, Y=2. H0_G = [(X,Y,0)]. H1_G = [(X,Y,7)].
Both truth configs. Surface differs from World F: F's H1 is [(X,Z,7)],
G's H1 is [(X,Y,7)]. Under the set-X schema the arrivals at Y are (0,7)
for G versus (0, INF-with-Z-detour...) for F; the discriminating
signature (V*=2, t*=0, pred_h0=1, pred_h1=0, schema=1) is identical, so
the persisted record R applies to G exactly.

Expected phase B trace per config (truth cfg0 = H0_G):
PLAN [S,W,OY] (reconstructed from R); EXEC real=1; PRED h0=1 h1=0
(from R, not recomputed); SURVIVE h0; ELIM h1; CONVERGE-OK.
Truth cfg1 = H1_G: EXEC real=0; ELIM h0; SURVIVE h1; CONVERGE-OK.

## Metric moved

Standing priority "genuine learning persists after scaffold disconnect":
first instrumented measurement for DDES (schema record persistence plus
post-disconnect usability on a structurally novel world). Pass means the
derived schema is a storable, reusable artifact, not scaffold-bound
ephemera. This is storage plus functional reuse; it is not representational
invention and is not evidence toward L3.

## Frozen kill bars (all must pass for BUILD-PASS)

- K-F1 (record persisted from a working derivation): phase A trace
  contains the exact line
  `SCHEMA-RECORD schema=1 V*=2 t*=0 pred_h0=1 pred_h1=0`, and phase A
  prints CONVERGE-OK on both World F configs. Kill: line absent or
  mismatched, or either F config fails to converge.
- K-F2 (disconnect genuine): the trace contains no SCAFFOLD-VIOLATION
  line and the final `SCAFFOLD-CALLS n` reads 0. Kill: any
  derivation-path invocation during phase 2.
- K-F3 (usable after disconnect): phase B on World G, both configs:
  CONVERGE-OK, surviving hypothesis matches truth
  (cfg0: SURVIVE h0 and ELIM h1; cfg1: ELIM h0 and SURVIVE h1), and the
  executed plan is exactly [S,W,OY] reconstructed from record fields.
  Kill: wrong convergence, failure to converge, or a plan other than
  [S,W,OY].
- K-F4 (novelty of the usability world): World G rule tables differ
  from World F (static check; H1_G=[(X,Y,7)] vs H1_F=[(X,Z,7)]), and
  phase A runs derivation on F only. Kill: derivation ever ran on G
  (already covered by K-F2; this bar documents the prereg-level check).
- K-F5 (determinism): 3/3 runs byte-identical (sha256 match), exit 0,
  zero stderr bytes on every run. Kill: any divergence, nonzero exit,
  or any stderr byte.
- K-F6 (purity and docs): pure Zag only; zero Python at any stage
  (implementation, build, run, analysis); zero em-dash and zero en-dash
  bytes in all lane files (byte-checked with check_no_dash.sh from the
  repo root). Kill: any Python use or any forbidden byte.

## Out of scope (documented, not tested)

Schema validity scope: a persisted schema applied outside its validity
class can misfire; this experiment does not test misapplication. No
protected-core changes. No new dedicated semantic cases. No CAUSALV7.
No frozen bar is weakened.

## Commit order

This prereg is written before any implementation. The implementation is
a strict descendant. The wave coordinator commits at wave end; this lane
does not commit or push.
