# REPORT.md - L3 Transfer: reuse of an invented intermediate across domains

Date: 2026-10-02. Worker: L3 Transfer Worker.
Frozen prereg: PREREG.md (committed alone as `abcb1e53d`, with transparent
amendments AMEND-1 and AMEND-2 recorded before the frozen runs).

## Verdict: L3-TRANSFER-COMPLETE

All eight frozen kill bars T1-T8 passed, 3/3 deterministic byte-identical.

## Result vs each frozen bar

- T1 determinism: PASS. run1/run2/run3 sha256
  `4158f39e6a8a903b4dbc3afe0374d2c356baa8f56d3119d67a9ef2e698a8bdc8`,
  byte-identical, exit 0, ALL PASS each run.
- T2 invention in A (FORAGE): PASS. Greedy construct: round 1 base=5,
  80 evals, winner (1,0,2) gain 3 score 8 t=10; round 2 no improvement,
  stop. Library entry 0: prog bytes (1,0,2) = ADD R0,R2, gen 0,
  origin=FORAGE, n_reuse=0. FORAGE test 4/4.
- T3 decoy rejection and invention in C (RELAY): PASS. M_A probed on
  RELAY train: 5/8 at t=12, rejected. Fresh construct: round 1 base=6,
  80 evals, winner (2,0,1) gain 2 score 8 t=3; round 2 stop. Library
  entry 1: (2,0,1) = SUB R0,R1, gen 1, origin=RELAY. RELAY test 4/4.
- T4 reuse in B (SENTRY): PASS. Probe: entry 0 (FORAGE) 8/8 t=16,
  entry 1 (RELAY) 6/8 t=2; exactly one perfect. lib_adapt code 0
  (reuse). B-phase construct evals delta = 0. M slot program bytes
  (1,0,2), identical to entry 0. Provenance line: prog=1,0,2
  origin=FORAGE gen=0 n_reuse=1. SENTRY test 4/4.
- T5 fresh baseline (ARM-FRESH): PASS. Library empty, adapt code 1
  (construct), 160 evals, invented (1,0,2) origin=SENTRY t=16, test 4/4.
- T6 cost: PASS. Transfer arm B-phase evals 0 < fresh arm 160.
- T7 no-lib ablation: PASS. Library wiped (libn=0); phase B reinvented
  from scratch, B-phase evals delta = 160. The library is causally
  responsible for the zero cost.
- T8 hygiene: PASS. Frozen audit grep on learner.zag: `e0+e2`, `ADD R0,R2`,
  `7,1,5,2`, `5,0,9,9`, `9,5,7,5` all 0; `_MODE`, `bridge`, `handler`
  all 0; `_zag_print` 0; pure Zag under safebin (which python3: nothing);
  explicit pathspecs; zero em/en dashes.

## What this establishes

The intermediate M=[ADD R0,R2] invented by greedy construction in the
FORAGE domain (rule: rich iff e0+e2 >= 10) was stored in a learner-owned
library with its provenance (origin=FORAGE). A decoy domain (RELAY, rule
open iff e0-e1 >= 4) correctly rejected M_A (5/8) and invented its own
M=[SUB R0,R1]. In the new SENTRY domain (rule alert iff e0+e2 >= 16,
e1=e3=5 constant), the learner's adapt policy probed the library on
SENTRY training episodes, found exactly one entry reaching perfect
(8/8 at refit t=16), and reused it with zero new construction
evaluations instead of reinventing it (160 evals in the fresh arm).
Provenance is learner-visible: origin=FORAGE, n_reuse=1. The causal
ablation (wipe library, cost returns to 160) shows the reuse depends on
the stored intermediate.

## Honest limits

- This is exact reuse of an invented intermediate across domains with
  matching structure, not adaptation: the adapt policy requires exactly
  one perfect probe hit and otherwise constructs fresh. Partial-match
  adaptation (truncate, specialize, substitute) is the L2 frontier and
  was not tested here.
- Invention itself uses the frozen greedy construct over the same finite
  op menu as the composition_l3 lineage; the transfer claim concerns
  reuse, not open-ended form invention.
- The SENTRY domain was designed by the builder (hand-verified tables),
  not by an independent adversary.

## Reproducibility

- `build.sh` concatenates learner.zag + driver.zag and compiles with
  the pinned `$HOME/safebin/znc`.
- Binary `l3t_bin` run 3x: exit 0, ALL PASS, byte-identical outputs.
- Falsifiers F1-F4 (in-binary assertions) all passed; no assertion
  fired.
