# TRIAL_RESULTS.md — NSR-1 structural revision loop (native)

Date: 2026-09-19. All runs native on this Linux VM via
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
Runner: `./run_sr.sh` (compile + 2 runs, byte-identical stdout required,
every `CL_CHECK` validated, static RNG grep, core-isolation grep,
receipts + SHA-256 per evidence dir).

Verdict: **POSITIVE** (attempt 3; attempts 1–2 are honest negatives that
drove amendments A1–A3 — reported below, not hidden).

## Final run (attempt 3) — TRIAL PASSED

`SR_FAILURES,0` · `checks_total=94 checks_bad=0` · determinism byte-identical
· `system_rng_symbols=none` · `core_isolation=ok` · run1_exit=0 run2_exit=0.

Per-arm statistics (`SR_STAT,run,arm,seed,diagnoses,promotes,rollbacks,exhausted`):

| arm | seed 11 | seed 22 | seed 33 |
|---|---|---|---|
| SHIFT (designed) | 6 diag, 2 prom, 1 rb, 0 exh | same | same |
| SHIFT-LCG (scaffold) | 4 diag, 2 prom, 0 rb, 0 exh | same | same |
| NO-SHIFT | 2 diag, 0 prom, 1 rb, 0 exh | same | same |
| FROZEN | 0 diag, 0 prom, 0 rb, 0 exh | same | same |
| SCALE (560 eps, 9 inversions) | 20 diag, 9 prom, 1 rb, 0 exh | same | same |

Endpoints (`r1ep/16`, `finalep/32`, final trace):

- SHIFT: r1ep=13/16, finalep=26/32, final trace `(0,500,0)` — flipped to
  `(0,500,1)` for R1, flipped back after returning to R0. All gates pass
  on all 3 seeds.
- SHIFT-LCG: r1ep=13/16, finalep=26/32. All gates pass on all 3 seeds.
- NO-SHIFT: 0 promotes (gate), finalep=26/32 (≥20 gate). The single
  rollback is the designed dip curriculum at eps 10–11 being correctly
  refused: 2 sustained failing batches → propose edit 0 → paired 32
  (normal flips): base 26 vs candidate 6 → NOTBETTER → rollback.
- FROZEN: r1ep=3/16 — the mechanism is off, so this is the raw
  base-trace score on R1. SHIFT−FROZEN r1ep = 13−3 = 10 ≥ 5 on all seeds.
- SCALE: 9 promotes (exactly the 9 inversions), 1 rollback (the dip
  curriculum), 0 exhausted; r1ep=13/16, finalep=26/32; ends with the
  R1-adapted trace `(0,500,1)` (run ends in R1). Ledger ~612 entries;
  wall-clock ~160 ms/run total.

White-box gates (all arms × all seeds, 0 errors):

- `wb_replay` = 0: replaying the append-only audit ledger reconstructs
  the exact live state (accepted slot, candidate liveness, streaks,
  tried masks, all five audit counters).
- `wb_attr` = 0: accepted symbolic structure changes only via
  SR_SEED/SR_PROMOTE.
- `wb_clean` = 0: refused operations never mutate state.
- `wb_just` = 0: every promotion in the ledger was justified —
  candidate-majority-positive, base-majority-negative, strict
  candidate > base improvement.

Units: `units_err=0` (13 native unit tests, including negative cases:
propose-without-diagnosis, promote-worse-candidate,
rollback-without-candidate, double-seed, 5-rollbacks-then-exhausted,
derivation-advance-after-rollback, and the A3 rejection-expiry test).

Evaluator separation held: R1-phase endpoints and final endpoints are
read-only fresh batches never fed back into `SR_RECORD`.

Program-law compliance:

- No RNG in the AI: `sr_core.zag` + the trial's learner policy path
  contain no RNG, no random tie-breaks, no stochastic policy (static
  grep verified each run). The system is deterministic from state.
- Test adversarial: all adversity is designed — the exact R0, the
  3/16 flip sequence, the dip episodes, the regime inversions; the
  SHIFT-LCG arm's seeded LCG is explicitly labeled harness scaffolding.
- Verdict distinguishes system-deterministic (byte-identical double
  runs, exact replay) from test-adversarial (designed curricula +
  scaffold arm).
- 10× scale addressed in-trial: SCALE arm, 560 episodes, 9 inversions,
  9/9 adapted, invariants held, ~2.4 ms/episode.

## Attempt 1 (negative — drove amendment A1)

- 35 `SR_FAILURES`; SCALE churned: 279 diagnoses, 6 rollbacks,
  272 exhausted proposals, 1 noise promotion.
- Causes: (a) replay-check implementation bug (PROMOTE/ROLLBACK zeroed
  candidate fields live but replay only cleared candidate liveness);
  (b) single 16-probe diagnosis batches fired on noise dips — one batch
  cannot distinguish a dip from a shift.
- Fixes (A1): replay zeroes all candidate fields exactly; proposal
  requires SUSTAINED diagnosis (≥2 consecutive majority-negative
  batches); promotion measures on two paired fresh 32-probe batches.

## Attempt 2 (negative — drove amendments A2, A3)

- Units and white-box gates passed, but science gates failed and the
  behavior was wrong in an instructive way.
- The sum-inverse R1 (`label = (v0+v1 ≤ 1000)`) was outside the 5-edit
  hypothesis neighborhood: the polarity flip recovers only ~50% because
  the base trace was a 75% approximation, never the exact rule. The loop
  behaved *correctly* — diagnosed, tried all 5 edits, rolled each back,
  declared EXHAUSTED — but the trial couldn't show learning when the
  fix wasn't in the hypothesis space. (Documented as a finding: the
  refusal/exhaustion machinery working as designed.)
- Real mechanism flaw found: R0 dips burned all 5 edits before the R1
  shift arrived (seed 22: 0 promotes, 14 exhausted) — rejections
  measured against dip noise permanently disqualified edits for a
  later genuine shift. Fix (A3.1): `tried` mask scoped to the failure
  episode; a healthy accepted batch expires old rejections.
- Test flaw found: the designed cue formula's dip frequency varied
  10–37% by seed — adversity wasn't controlled. Fix (A3.2): exact R0
  (`label = (v0 > 500)`, every batch exactly 13/16) + explicit designed
  dip episodes (10–11) for the rollback path; paired/endpoint
  measurements always use standard flips.
- Harness bug found: R1 endpoint measured at end-of-run with the
  flipped-back R0 trace; fixed to capture at end of an R1 phase
  (ep39; ep559 = ne-1 for SCALE, whose last phase is R1).

## Scope boundary (what this does NOT claim)

- One symbolic trace, one 5-edit neighborhood, a synthetic cue family,
  a harness-fixed invocation policy.
- The approximation regime (base trace as inexact rule) is untested —
  the sum-rule world is the named next curriculum.
- A passing result establishes a native, audited, deterministic
  structural revision loop surviving a 10× horizon — not general
  self-programming or general intelligence.

## Evidence

Latest passing evidence bundle:
`EVIDENCE_20260920T002523Z/` (receipt, SHA-256 sums, compile/run
transcripts for both byte-identical runs, sources). Earlier attempts'
bundles: `EVIDENCE_20260920T002045Z`, `...T002155Z`, `...T002251Z`,
`...T002401Z`, `...T002407Z`, `...T002513Z`, `...T002519Z` (kept —
negatives are deliverables).
