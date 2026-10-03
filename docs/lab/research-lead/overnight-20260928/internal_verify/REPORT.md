# REPORT.md -- IVWC: Internal Verification via World Consequences

## Verdict: BUILD-PASS (K1..K6 all PASS)

The learner committed to composition outputs plus its own confidence
before any outcome signal, received pure environmental consequences,
updated its own calibration from those consequences, and its updated
self-evaluation predicted sealed future performance better than its
raw estimate. All six frozen kill bars pass. Deterministic 3/3.

## What was built

`src/ivwc.zag` (pure Zag, single file, pinned znc), `bin/ivwc`
(frozen binary). 1D corridor world (20 cells), NAV+GATHER composition
from noisy beliefs, physics consequence simulator, per-bucket
learner-owned calibration table, sealed evaluation (12 fresh cases),
no-feedback ablation arm, shuffled-feedback secondary arm.

Build: `src/tools/toolchain/znc_linux_x86_64_abed8aa1 src/ivwc.zag
-o bin/ivwc`. Analyzer warnings: none after flag cleanup (one
informational zagd-unavailable notice only).

## Kill-bar results

- K1 (commit before signal): PASS. In-program world-call counter = 0
  immediately after the train COMMIT phase (`K1-STRUCT-PASS`).
  Audit A1: last train-commit `learner_compose(` at line 344, first
  `world_execute(` at line 357; 357 > 344. Audit A2: zero
  `world_buf`/`world_off` tokens in the LEARNER section.
- K2 (consequence not a disguised answer check): PASS. Audit A3:
  zero `expected|answer|key|target` tokens (case-insensitive) in the
  program. Audit A4: zero `correct|reference_plan|gold` tokens; every
  `==` in `world_execute`/`w_step`/`w_*` compares against physics
  (bounds, wall presence, item presence) or action dispatch; no
  reference plan exists anywhere in the program. The consequence
  `collected` is a physical inventory count from executing the plan,
  not a comparison to a key. `learner_update` receives only
  (table, bucket, raw_conf, consequence buffer).
- K3 (confidence updates from consequences): PASS.
  `K3-STRUCT-PASS nmoved=17`: 17 of 24 train cases calibrate
  differently from raw after the update phase.
- K4 (self-evaluation predicts future performance): PASS. Sealed
  sum|calibrated-actual| = 113 < sum|raw-actual| = 116 (strict).
- K5 (determinism): PASS. 3/3 byte-identical stdout, sha256
  `307fdd58bebea712cf25ed64c0fe7c7e22bb42cb9531edfd97bc61da9580507c`.
- K6 (ablation): PASS. Sealed sum|ablation-actual| = 116 >
  sum|calibrated-actual| = 113 (strict). As declared in the prereg,
  the no-feedback ablation's predictions equal raw by construction.

## Calibration numbers

Learner-owned calibration table after 24 train cases (bucket by
planned gathers; mean overconfidence error):

- b=0 (0 gathers): n=7, meanerr=0
- b=1 (1 gather):  n=7, meanerr=4
- b=2 (2-3 gathers): n=7, meanerr=15
- b=3 (4+ gathers): n=3, meanerr=16

The learner discovered systematic overconfidence that grows with
planned gathers, which matches the world structure: more planned
gathers means more exposure to phantom item beliefs (18% false
positive rate). Bucket 0 correctly learned zero bias (empty plans
cannot overcollect). By construction of the physics, err =
raw - actual is always >= 0 (collected can never exceed planned
gathers, energy used equals plan length), so the miscalibration is
structural overconfidence, and the learner's correction is always in
the right direction.

Sealed (12 fresh cases, cid 100..111):
sum|raw-act| = 116, sum|cal-act| = 113, sum|abl-act| = 116,
sum|shuffled-act| = 302.

The shuffled-feedback secondary arm (each train case updated from
another case's consequences) scores 302, far worse than the feedback
arm's 113: the CONTENT of the consequences drives the calibration,
not the mere act of updating.

## Honest caveats

1. The K4 margin is thin: 113 vs 116 (2.6% MAE improvement). The bar
   is strict inequality and it passes deterministically, but the
   effect is modest. Per-case analysis: calibration helps most when
   the learner was badly overconfident (sealed s=0: 40->25 error;
   s=3: 50->46) and hurts slightly when beliefs happened to be
   exactly right (s=2,4,7,9,10: raw was exact, correction adds 4).
   The learned bias structure (0/4/15/16) is clear; the sealed gain
   is the average of these opposing effects.
2. K6 is numerically identical to K4's comparison (declared openly in
   PREREG section 3): the no-feedback ablation falls back to raw
   confidence on identical plans. The independent evidence for
   "feedback matters" is the shuffled arm at 302.
3. This is a mechanism test, not a composition-novelty or L3 claim
   (per PREREG section 4). The NAV+GATHER composition is deliberately
   simple; the result concerns the commit -> consequence ->
   self-evaluation loop.

## Implementation bug fix (documented, not a design change)

During testing, `world_gen`/`belief_gen` panicked for case ids whose
frozen seed exceeded 65535: the LCG's first `seed*25173` overflowed
i32, producing a negative state and a negative cell index. Fixed in
`lcg_next` by reducing the state mod 65536 on entry (the LCG state
space is 0..65535; the frozen seed formulas `7919*cid+13` and
`104729*cid+7` are unchanged). Kill bars and design parameters are
untouched; the prereg's LCG specification is now actually
implementable. Found via case bisection (t=20), verified fixed, then
full 3/3 runs.

## Reproduction

```
cd docs/lab/research-lead/overnight-20260928/internal_verify
~/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1 src/ivwc.zag -o bin/ivwc
./bin/ivwc | sha256sum   # expect 307fdd58bebea712cf25ed64c0fe7c7e22bb42cb9531edfd97bc61da9580507c
```

Frozen audits (PREREG section 5): A1 ordering 344<357; A2 count 0;
A3 count 0; A4 zero tokens, `plan[` count 0 (informational); A5
sha256 equality across runs/ivwc-run{1,2,3}.txt.

## Branch note

Work was committed on `lane-hcontlife5-20261002` (the shared checkout
this worker was spawned on), not `tnn-native-lab`: switching branches
with other workers active and staged changes in the shared index
would move the working tree under them. All commits use explicit
pathspecs confined to `internal_verify/`. Local only, never pushed.
