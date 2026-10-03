# IMPLEMENTATION: F2 v6 (wave-20261002-0521pdt)

Source: `f2v6_learner.zag` (this lane). Frozen prereg: PREREG_F2V6.md
(commit 8f99040b3). Pure Zag; safebin toolchain (Step 0 in NAMECHECK.md).

## Provenance

Adapted from the uncommitted v5 working-copy implementation
(`docs/lab/rsi/runs/wave-20261002-0221pdt/F2/f2v5_learner.zag`), which was
never executed against any sealed world and never committed. The v6 delta
was applied after the prereg freeze commit (commit-order self-check:
prereg 8f99040b3 strictly precedes the implementation commit).

## The v6 delta (exact)

1. `L_run` replaced: fixed one-revision cap -> evidence-driven revision
   loop (contradiction -> revise; stop on goal-met, fixed-point law-set
   repetition, or no-contradiction; wave-safety cap 6 as hygiene).
2. `L_wave` result buffer extended 64 -> 128 bytes: +52 nalive (i32),
   +56 ne (i32), +60 ne*5 survivor rule bytes (canonical).
3. Return encoding: bits 0-5 final mask; bits 8-10 revision count;
   bit 11 fixed-point stop. Single-wave runs return the v4-style mask.
4. Header and L_wave doc comments updated. Nothing else changed.

Diff line count (v5 base -> v6): 206 changed lines (measured via `diff`;
v5 base is the uncommitted 0221pdt working-copy file).

## K6-R2 source audit (construction, not enumeration)

- No complete experiment, distinguishing sequence, or goal plan appears
  as a literal in source. `grep` for literal action sequences (`[SX`)
  returns nothing; all executed sequences are produced by
  iterative-deepening composition over the 7-symbol primitive alphabet
  (L_find standard scan to depth 6; L_dpds_pair pair-restricted search
  to D2=9; L_plan / L_plan_c2 to w_plan_maxd).
- The SUFFIX verification protocol is constructed programmatically by
  L_build_suffix ([OBS goalvar, WAIT] x 3); it is the preregistered
  measurement protocol, not a goal plan.
- The random-action control uses a frozen fixed-seed LCG; its outputs
  never feed back into decisions.
- The learner never reads sealed laws; it calls only the w_* interface
  (verified: no reference to S2_*/C2_* law constants in the learner).

## Architecture accounting (implementation step)

- Cognition source lines added vs v5 base: 206 changed lines (loop +
  signature export + encoding + comments).
- New hardcoded semantic cases: 0.
- New modes / bridges / routers: 0.
- New task-specific handlers: 0.
- New learner-state structures: 0 (signature is wave-local; the sigs
  buffer in L_run is run-local comparison state, not persistent
  cognitive structure).
- Sealed worlds + NC substrates: authored test substrate, not cognition.

## Build

`bash build.sh [sealed|regression|nc|all]` (run from ~/workspace/tnn-rsi).
Binaries and concatenation intermediates in /tmp (ephemeral); sources
and logs in the lane dir.
