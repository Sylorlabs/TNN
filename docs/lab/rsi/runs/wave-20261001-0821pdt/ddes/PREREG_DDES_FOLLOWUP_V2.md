# PREREG: DDES schema-persistence follow-up, V2 re-freeze

Frozen before any implementation. Wave 20261001-0821pdt, lane
ddes-refreeze. This prereg is written fresh and supersedes the
wave-20260930-2021pdt prereg
(docs/lab/rsi/runs/wave-20260930-2021pdt/ddes_followup/PREREG_DDES_FOLLOWUP.md),
which is retired without adoption: its implementation ddesp.zag does
not compile under the pinned znc (ddes_world takes 15 params, all six
call sites pass 14; phase B was never wired), and the prereg and the
implementation shared commit 904e9b6f6, so ordering is unverifiable.
Judged BUILD-FAIL + UNVERIFIABLE ORDERING in LOOP_STATE.md (wave
wave-20261001-0221pdt). Nothing from the broken implementation is
adopted; only validated design ideas are carried forward, re-frozen
here. Any amendment must be committed transparently and re-frozen
before implementation; no bar may be altered after seeing results.
Builders report BUILD-PASS/BUILD-FAIL only.

## Provenance

NEW prereg, written by worker ddes-refreeze for wave 20261001-0821pdt,
phase 1. Design inherits the DDES R2 lineage
(docs/lab/rsi/runs/wave-20260930-1121pdt/ddes/PREREG_DDESREPAIR2.md;
REPAIR-PASS, independently verified; the t*=0 soundness hole is closed)
and the 2021pdt follow-up design (schema persistence across scaffold
disconnect). A /tmp diagnostic in the 0221pdt wave suggested the
design's bars would hold under mechanical completion, but that
diagnostic is not evidence and is not adopted.

## The question (one mechanism, one question)

Do DDES-generated experiment schemas persist and stay usable across a
scaffold disconnect? This is a standing metrics priority (genuine
learning persists after scaffold disconnect), and this lane gives it
its first instrumented measurement for DDES, now with the t*=0
soundness repair demonstrated in the persisted application. One
mechanism (DDES), one question (persistence plus post-disconnect
usability of the persisted schema on a sealed world).

## The repaired design

A single pure-Zag binary (phase 2 implementation file: ddesp2.zag;
the broken ddesp.zag name is retired) runs two phases.

### Phase A: scaffold CONNECTED

Repaired DDES derivation (the R2 repair is frozen in) on World F, both
truth configs, plus a World A regression anchor, both configs.

- World F (t*=0 soundness regression world): X=0, Z=1, Y=2.
  H0_F = [(X,Y,0)]. H1_F = [(X,Z,7)]. Both truth configs.
- World A regression anchor: H0 = [(X,Z,2),(Z,Y,0)];
  H1 = [(X,Y,1)]. Both truth configs.
- Derivation includes the R2 repair: eff_waits(t*) = max(t*,1);
  synthesize_plan waits while cur_t < eff_waits(t*); predict uses
  arrival[V*] <= eff_waits(t*); when the derived target satisfies
  t* == 0, the derivation emits the exact trace line
  `FLAG TSTAR-ZERO-BOUNDARY floor=1` between the TARGET line and the
  PLAN line. The clamp and the flag are generic boundary conditions on
  the derived target, of the same class as the existing null-schema
  fallback, not semantic cases.
- Expected World A trace per config (frozen, from the R2 evidence):
  `TARGET V*=2 t*=1 schema=1`; `PLAN [S,W,OY]`; no FLAG;
  `EXEC real=0` (cfg0) / `EXEC real=1` (cfg1);
  `PRED h0=0 h1=1`; correct SURVIVE/ELIM; `CONVERGE-OK`.
  (The candidates_built counter is not frozen; only A and F run here,
  so its values differ from R2.)
- Expected World F trace per config:
  `TARGET V*=2 t*=0 schema=1`;
  `FLAG TSTAR-ZERO-BOUNDARY floor=1`;
  `PLAN [S,W,OY]`;
  `EXEC real=1` (cfg0) / `EXEC real=0` (cfg1);
  `PRED h0=1 h1=0`; correct SURVIVE/ELIM; `CONVERGE-OK`.
- After both F configs converge, the schema record R is written into a
  dedicated learner-owned state buffer (learner_state), separate from
  all derivation temporaries: [0]=schema=1, [4]=V*=2, [8]=t*=0,
  [12]=tstar_zero=1, [16]=pred_h0=1, [20]=pred_h1=0. The trace emits
  the exact line:
  `SCHEMA-RECORD schema=1 V*=2 t*=0 tstar_zero=1 pred_h0=1 pred_h1=0`
- Phase A must converge on both F configs; otherwise the persisted
  record is meaningless.

### Scaffold disconnect

A global phase flag moves to 2. Every derivation-path function
(compute_arrivals, compute_frontier, synthesize_plan, predict,
ddes_world) checks the phase on entry and, if invoked during phase 2,
increments a violation counter and emits `SCAFFOLD-VIOLATION`. The
trace emits `SCAFFOLD-CALLS n` at the end of phase 2. The disconnect
is therefore instrumented, not merely a code path that happens to
avoid derivation.

### Phase B: scaffold DISCONNECTED

Sealed World G, both truth configs. Phase B reads ONLY the persisted
record R from learner_state. It emits the exact line
`RECORD-LOAD schema=1 V*=2 t*=0 tstar_zero=1 pred_h0=1 pred_h1=0`
(fields must match the SCHEMA-RECORD line exactly). It reconstructs
the experiment directly from record fields: [S] then W repeated
eff_waits(t*) times (t*=0 floors to 1 via the generic clamp;
tstar_zero records that the boundary was hit at derivation) then
observe(V*), with obs action = 4 - V* (the same generic mapping, no
derivation). It emits the reconstruction marker `REPLAN [S,W,OY]`
(deliberately distinct from the derivation PLAN marker). It executes
the plan once on the true world, emits `PRED-RECORD h0=1 h1=0`
(predictions from the record, not recomputed), compares the real
observation against the persisted predictions, and eliminates the
mismatch. No arrival computation, no frontier computation, no plan
synthesis, no predictor call. The trace emits CONVERGE-OK or
CONVERGE-FAIL per config.

### World G (sealed, frozen here; derivation never sees it)

Variables: X=0, Z=1, Y=2. H0_G = [(X,Y,0)]. H1_G = [(X,Y,7)]. Both
truth configs. Surface differs from World F: F's H1 is [(X,Z,7)],
G's H1 is [(X,Y,7)]. The discriminating signature (V*=2, t*=0,
pred_h0=1, pred_h1=0, schema=1) is identical, so the persisted record
R applies to G exactly.

Expected phase B trace per config (truth cfg0 = H0_G):
`WORLD G`; `RECORD-LOAD schema=1 V*=2 t*=0 tstar_zero=1 pred_h0=1 pred_h1=0`;
`REPLAN [S,W,OY]`; `EXEC real=1`; `PRED-RECORD h0=1 h1=0`;
`SURVIVE h0`; `ELIM h1`; `CONVERGE-OK`.
Truth cfg1 = H1_G: `EXEC real=0`; `ELIM h0`; `SURVIVE h1`;
`CONVERGE-OK`.

### Why World G demonstrates the soundness repair

G cfg0 is exactly the boundary case that silently wrongly converged
under the unrepaired code. Unrepaired, the schema would reconstruct
[S,OY] with zero waits: rules fire only on W ticks, so OY reads
pre-propagation state (real=0), while the naive predictor
(arrival[V*] <= t* = 0) claims pred_h0=1, eliminating the TRUE h0 and
printing CONVERGE-OK. Repaired, the reconstruction floors to [S,W,OY]
via eff_waits(t*): EXEC real=1 agrees with pred_h0=1, and convergence
is correct. K-G4 forbids any zero-wait plan and requires correct
convergence on both G configs.

## What exactly changes vs the broken ddesp.zag (2021pdt)

1. Compile repair: ddes_world takes 15 params (including the guard
   buffer g) but all six call sites in ddesp.zag passed 14, so it does
   not compile under the pinned znc. The new implementation passes g
   at every call site.
2. Phase B wiring: in ddesp.zag apply_persisted existed but main()
   never called it and the phase flag never advanced to 2. The new
   main() advances the phase flag to 2 after Phase A, calls the
   phase-B applier on both World G truth configs, then emits
   SCAFFOLD-CALLS.
3. t*=0 repair frozen in the derivation: eff_waits clamp in
   synthesize_plan and predict, plus the FLAG TSTAR-ZERO-BOUNDARY
   floor=1 marker on t*==0 (inherited from R2, re-frozen here as an
   explicit requirement; ddesp.zag never compiled, so its derivation
   was never validated).
4. Scope reduction: ddesp.zag ran Worlds A through E in phase A; the
   V2 design runs World A only as a regression anchor plus World F.
   The full A-E regression of the repaired derivation is already
   established and independently verified by R2 (K-R2.3); re-running
   the full suite adds no information for this lane's question.
5. Record carries the boundary fact: the 2021pdt record was
   (schema=1, V*=2, t*=0, pred_h0=1, pred_h1=0); the V2 record adds
   tstar_zero=1, and the SCHEMA-RECORD line includes it.
6. Trace vocabulary: phase B emits REPLAN and PRED-RECORD markers
   distinct from the derivation PLAN and PRED markers, so the no-leak
   audit (K-G7) can forbid derivation markers in phase 2 mechanically.
7. Implementation file renamed ddesp2.zag; the broken ddesp.zag name
   is retired.

## Metric moved

Standing priority "genuine learning persists after scaffold
disconnect": first instrumented measurement for DDES (schema record
persistence plus post-disconnect usability on a structurally novel
world, with the boundary soundness repair demonstrated in the
persisted application). Pass means the derived schema is a storable,
reusable artifact, not scaffold-bound ephemera. This is storage plus
functional reuse; it is not representational invention and is not
evidence toward L3.

## Frozen kill bars (all must pass for BUILD-PASS; builders report BUILD-PASS/BUILD-FAIL only)

- K-G1 (compiles under the pinned znc): the pinned znc compiles
  ddesp2.zag with exit 0, zero stderr bytes, and produces an
  executable. Kill: any compile error, any stderr byte, or no
  executable.
- K-G2 (repaired derivation anchor and persisted record): World A
  anchor converges on both configs with `TARGET V*=2 t*=1 schema=1`,
  plan line starting `PLAN [S,W,OY]`, no FLAG line, correct
  SURVIVE/ELIM and CONVERGE-OK; both World F configs print the exact
  line `FLAG TSTAR-ZERO-BOUNDARY floor=1` between the TARGET line and
  the PLAN line, the plan line starts `PLAN [S,W,OY]`, and both print
  CONVERGE-OK; phase A trace contains the exact line
  `SCHEMA-RECORD schema=1 V*=2 t*=0 tstar_zero=1 pred_h0=1 pred_h1=0`.
  Kill: any absent or mismatched line, a FLAG on World A, a plan
  other than [S,W,OY], or a failed convergence.
- K-G3 (disconnect genuine): the trace contains no SCAFFOLD-VIOLATION
  line and the final `SCAFFOLD-CALLS n` reads 0. Kill: any
  derivation-path invocation during phase 2.
- K-G4 (soundness repair demonstrated on the persisted application):
  phase B on World G, both configs: CONVERGE-OK; surviving hypothesis
  matches truth (cfg0: SURVIVE h0 and ELIM h1; cfg1: ELIM h0 and
  SURVIVE h1); the reconstructed plan is exactly [S,W,OY] (a
  zero-wait plan is forbidden); EXEC real agrees with the persisted
  prediction on the surviving hypothesis (cfg0: real=1 with
  pred_h0=1; cfg1: real=0 with pred_h1=0). Kill: wrong convergence,
  failure to converge, a zero-wait plan, or EXEC/prediction
  disagreement.
- K-G5 (novelty of the usability world): World G rule tables differ
  from World F (static check: H1_G=[(X,Y,7)] vs H1_F=[(X,Z,7)]); the
  derivation path is invoked on F and A only. Kill: any
  derivation-path invocation on G (already covered by K-G3; this bar
  documents the prereg-level check).
- K-G6 (determinism): 3/3 runs byte-identical (sha256 match), exit 0,
  zero stderr bytes on every run. Kill: any divergence, nonzero exit,
  or any stderr byte.
- K-G7 (no leak): phase-2 trace contains no derivation markers
  (TARGET, FLAG, derivation PLAN, derivation PRED); it contains the
  RECORD-LOAD line with fields byte-identical to the SCHEMA-RECORD
  line and the REPLAN marker; static grep of the phase-B applier
  confirms it calls none of compute_arrivals, compute_frontier,
  synthesize_plan, predict, ddes_world and reads no world-law tables
  (it reads only the learner_state record plus the true-world
  execution tables). Kill: any derivation marker in phase 2, any
  RECORD-LOAD/SCHEMA-RECORD field mismatch, or any static-audit
  finding.
- K-G8 (honest cost accounting): the lane RESULT doc contains
  machine-greppable fields binary_bytes, wall_ms (per run),
  plans_built (final counter), source_delta_lines (vs ddesr2.zag),
  new_semantic_cases, new_modes, new_bridges. Kill: any missing
  field; any nonzero new_semantic_cases, new_modes, or new_bridges
  fails the bar as an architecture violation (the eff_waits clamp is
  a generic boundary condition, not a semantic case).
- K-G9 (purity and docs): pure Zag only; zero Python at any stage
  (implementation, build, run, analysis); zero em-dash and zero
  en-dash bytes in all lane files (byte-checked with
  check_no_dash.sh from the repo root). Kill: any Python use or any
  forbidden byte.

## Honest boundaries: bounded L2 ceiling, NOT L3

Ceiling: strong L2 guided generation with persistence. This experiment
measures whether a derived schema is a storable, reusable artifact
(storage plus functional reuse); it does not invent representations.

Criterion 0 status (all four clauses conjunctive; the claim fails
unless all hold):

- C0-A (runtime-defined semantics): FAILS. The record carries only
  values (schema id, V*, t*, predictions, boundary flag) filled into a
  researcher-authored reconstruction template. The experiment
  semantics ([S], then W repeated eff_waits(t*) times, then
  observe(V*) with obs = 4 - V*) reside in source, not in
  learner-created persistent state. The schema=1 reconstruction case
  is researcher-authored machinery, not learner-created semantics.
- C0-B (open structural form): FAILS. The reconstructed experiment is
  a fixed template with filled parameters; the learner does not
  incrementally construct a novel topology.
- C0-C (multiple unforeseen forms): FAILS. Single mechanism; two
  researcher-frozen worlds (F, G); no post-freeze adversary-designed
  evaluation family.
- C0-D (cognitive reuse): FAILS. The schema is applied once on World
  G, which is reuse of a stored artifact, not cognitive reuse
  improving transfer, prediction, procedure learning, causal
  inference, memory, planning, or sample efficiency. Existence plus
  one application is insufficient.

Out of scope (documented, not tested): a persisted schema applied
outside its validity class can misfire; misapplication is not tested.
No protected-core changes. No new dedicated semantic cases. No
CAUSALV7. No frozen bar is weakened.

## Sealing protocol

- Holder of the World G law: the experiment harness (main()'s phase-2
  loop) holds the G rule tables. The derivation learner never receives
  them. Static seal: the derivation-path functions are invoked on F
  and A tables only; the phase-B applier receives only the
  learner_state record and the true-world execution tables for the
  current config.
- Prevention of reads: the phase guard (phase flag = 2) forbids every
  derivation-path call in phase 2, instrumented with the violation
  counter and SCAFFOLD-VIOLATION emission (K-G3). The phase-B applier
  reconstructs from record fields only; predictions come from the
  record (PRED-RECORD), never recomputed from world tables (K-G7).
  Executing the plan on the true G world is environment interaction,
  not a leak: the executor reads only the config's true rules.
- Truth handling: the harness runs each truth config as a separate
  pass; the learner never selects the truth config.
- Audit: the sealed-execution check is the static grep audit plus the
  trace-marker audit in K-G7, run before results are adopted. The G
  table loader may appear only in main()'s phase-2 loop, never in any
  derivation function.

## Commit order

This prereg is written before any implementation and is committed
alone by the coordinator; the implementation commit must be a strict
descendant (verified via git merge-base --is-ancestor before results
are reported). This lane does not commit or push. Phase 2
(implementation ddesp2.zag plus sealed execution) begins only on the
follow-up authorization message, which keeps commit ordering clean.

Phase 2 result doc:
docs/lab/rsi/runs/wave-20261001-0821pdt/ddes/RESULT_DDES_FOLLOWUP_V2.md
