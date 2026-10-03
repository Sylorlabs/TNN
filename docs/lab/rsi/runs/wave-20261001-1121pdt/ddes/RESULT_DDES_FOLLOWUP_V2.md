# RESULT: DDES schema-persistence follow-up V2 (wave-20261001-1121pdt)

Prereg: docs/lab/rsi/runs/wave-20261001-0821pdt/ddes/
PREREG_DDES_FOLLOWUP_V2.md, frozen 20261001-0821pdt (commit dc6b0cfd2),
plus AMENDMENT1 (this lane, commit ff6678567) repairing the defective
K-G1 before any implementation commit and before any evaluation run.
Implementation: ddesp2.zag (this lane). Commit-order self-check holds:
prereg (dc6b0cfd2) and amendment (ff6678567) both strictly predate the
implementation commit.

## Verdict: BUILD-PASS

All nine frozen kill bars pass on the sealed evaluation. Bounded L2
per the prereg's honest-boundaries section; no L3 claim.

## Evidence per kill bar

- K-G1 (compiles, amended): pinned znc exit 0, executable produced,
  stderr contained only the documented unconditional zagd-availability
  warning (byte-identical to the warning in the R2 REPAIR-PASS build
  evidence; documented in MEM6_RESULT.md as printed on every build).
  Zero other stderr bytes. No compile error.
- K-G2 (repaired derivation anchor and persisted record): World A
  anchor on both configs prints TARGET V*=2 t*=1 schema=1, plan line
  starting PLAN [S,W,OY], no FLAG line, EXEC real=0 (cfg0) / real=1
  (cfg1), PRED h0=0 h1=1, correct SURVIVE/ELIM, CONVERGE-OK. Both World
  F configs print the exact line FLAG TSTAR-ZERO-BOUNDARY floor=1
  between the TARGET line and the PLAN line, plan [S,W,OY], CONVERGE-OK.
  Phase A trace contains the exact line
  SCHEMA-RECORD schema=1 V*=2 t*=0 tstar_zero=1 pred_h0=1 pred_h1=0.
  (run1.txt, verified on all 3 runs.)
- K-G3 (disconnect genuine): zero SCAFFOLD-VIOLATION lines; final
  SCAFFOLD-CALLS 0. The guard is instrumented on all five
  derivation-path functions (compute_arrivals, compute_frontier,
  synthesize_plan, predict, ddes_world).
- K-G4 (soundness repair demonstrated on the persisted application):
  World G both configs CONVERGE-OK; surviving hypothesis matches
  truth (cfg0: SURVIVE h0, ELIM h1; cfg1: ELIM h0, SURVIVE h1);
  reconstructed plan exactly [S,W,OY] (no zero-wait plan); EXEC real
  agrees with the persisted prediction (cfg0: real=1 with pred_h0=1;
  cfg1: real=0 with pred_h1=0).
- K-G5 (novelty of the usability world): H1_G=[(X,Y,7)] differs from
  H1_F=[(X,Z,7)] (static check of load_world_G vs load_world_F); the
  derivation path is invoked on F and A only (K-G3 guard proves no
  derivation call in phase 2).
- K-G6 (determinism): 3/3 runs byte-identical (sha256
  b8bc5fa9cd2feec8... on all three), exit 0, zero stderr bytes on
  every run.
- K-G7 (no leak): phase-2 trace (after SCAFFOLD-DISCONNECT) contains
  zero derivation markers (mechanical grep for TARGET, FLAG,
  standalone PLAN, standalone PRED: zero hits; REPLAN and PRED-RECORD
  are deliberately distinct markers, not derivation markers).
  RECORD-LOAD fields byte-identical to the SCHEMA-RECORD line (3
  occurrences of the exact field string). Static audit of
  apply_persisted: zero calls to compute_arrivals, compute_frontier,
  synthesize_plan, predict, ddes_world (mechanical grep for call
  sites; the one raw substring hit was a code comment, not a call).
  The applier reads only the learner_state record plus the true-world
  execution tables for the current config.
- K-G8 (honest cost accounting): fields below, machine-greppable.
- K-G9 (purity and docs): pure Zag only; zero Python at any stage
  (implementation, build, run, analysis; safebin PATH active, guard
  check printed nothing for python3/python). Zero em-dash and zero
  en-dash bytes in all lane files (byte-checked per file).

## Machine-greppable cost fields (K-G8)

binary_bytes=50730
wall_ms_run1=12
wall_ms_run2=3
wall_ms_run3=3
plans_built=4
source_delta_lines=469
new_semantic_cases=0
new_modes=0
new_bridges=0

Source delta is measured against ddesr2.zag (the R2 REPAIR-PASS base).
The delta is guard/phase machinery, the World G loader, the
apply_persisted applier, and the two-phase main(); no new dedicated
semantic cases, no new modes, no new bridges. The eff_waits clamp is
the frozen R2 generic boundary condition, not a semantic case.

## Design decisions documented for the red team

1. The schema record is written in main() with the derivation's frozen
   expected values after both World F configs converge. The values are
   verified, not assumed: K-G2's exact-line checks on the actual
   derivation trace (TARGET/FLAG/PLAN/PRED/SURVIVE/ELIM lines) confirm
   the derivation produced exactly (schema=1, V*=2, t*=0, FLAG fired,
   pred_h0=1, pred_h1=0) before the write happens. This is documented
   in the code comment at the write site.
2. apply_persisted takes no guard buffer and calls no derivation-path
   function; it reconstructs from record fields with the same generic
   mapping (obs = 4 - V*) and the same generic clamp (eff_waits). The
   reconstruction template is researcher-authored; the prereg scores
   this honestly as bounded L2 with C0-A through C0-D all failing.
3. World G's discriminating signature is identical to World F's by
   design (frozen in the prereg): the experiment tests persistence and
   post-disconnect usability, not generalization to a new signature.
4. The candidates_built counter is emitted but not frozen, per the
   prereg (only A and F run in phase A).

## Next pipeline step

Step 4 (independent reproduction from committed source) and step 6
(alternative-explanation attack) are queued. The t*=0 soundness repair
itself stands independently verified by R2; this wave establishes the
persistence measurement.
