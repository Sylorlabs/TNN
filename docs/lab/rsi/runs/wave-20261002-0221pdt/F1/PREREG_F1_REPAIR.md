# PREREG_F1_REPAIR: Cumulative failure-evidence repair trigger (POLICY-C)

Lane F1, wave wave-20261002-0221pdt. This prereg is frozen alone before
any implementation file exists, before any fresh fixture is generated,
before any probe is built, and before any fresh learner run executes.
It is a fresh preregistration, not a salvage: the F1 v4 BUILD-FAIL
(wave-20261001-2021pdt, RT-EXEC EVIDENCE-HOLDS) and the 2321pdt
windowed-trigger BUILD-FAIL both stand on their frozen rules.

No em-dashes are used in this document.

## 0. Step 0 (toolchain guard)

Safebin activated and verified before any other work; recorded in
NAMECHECK.md Step 0 of this lane. PATH is safebin only. `which
python3` prints nothing. All work is pure Zag compiled by the pinned
znc, or shell invoking znc, running binaries, git ops, cmp/sha256sum,
grep, and file moves/copies. Any forbidden executable invocation is
automatic PROCESS-FAIL.

Pre-prereg work only (not implementation): read-only inspection of
committed traces from prior waves with grep (no probe built), and
read-only reading of committed sources. No fresh fixture generated, no
fresh learner run executed, no new code written to produce this
prereg.

## 1. Background and the remaining gap

F1 v4 (2021pdt) BUILD-FAILed with K-C0C TRIP on W1 (15/30): the K1=2
consecutive-failure trigger never fires on interleaved errors, so the
constructor never attempts learning. The 2321pdt trigger wave replaced
the consecutive counter with a windowed failure-density trigger
(WIN=8, FMIN=2): fire when at least 2 of the last 8 truth-episodes
were prediction failures. All trigger-specific bars passed
(K-TRIG-FIRE on 4 interleaving patterns, K-LEARN-INTERLEAVED 100%
hidden on all four, K-TRIG-CLEAN 0 false positives, K-ABL-TA,
K-BASE-TA, K-C0A, NC-TRIG discriminating old from new). The wave
BUILD-FAILed only on K-C0C-REG (fresh-seed R-W2 0/30), proven to be a
pre-existing constructor limitation: the old consecutive-trigger
binary fails identically on the same fixtures (8 triggers, same 4
overfit constructs, 0/30), and zero trigger regression was proven on
the prior wave's W2 fixtures (identical trigger episode, constructs,
30/30, structure).

Remaining gap (frozen premise of this prereg): the windowed trigger
forgets. Any failure stream with density below FMIN/WIN provably never
fires it: with failures spaced more than WIN episodes apart, no
8-episode window ever contains 2 failures. Sparse interleaved errors,
the normal case for a mostly-competent learner meeting occasional
counterexamples, therefore never trigger a repair attempt. This is the
remaining interleaved-error trigger gap.

This lane does not re-freeze the windowed trigger (that would repeat
a BUILD-FAILed wave without structural difference) and does not touch
the constructor (the R-W2 overfit is out of scope, proven
pre-existing).

## 2. The candidate: POLICY-C (cumulative failure-evidence repair trigger)

Replace the sliding window with a non-forgetting cumulative counter
over the learner's own binary error stream:

- Maintain `cumfail`, the count of truth-episodes with err > 0 since
  the last repair burst. Initialized 0.
- On each truth-episode: if err > 0, cumfail++. If cumfail >= FMIN,
  log TRIGGER, run the construction burst unchanged (up to KB=4
  single-element trial events, identical trial_move), then reset
  cumfail=0 so the same failures cannot retrigger.
- Disclosed constants (frozen here): FMIN=2 (unchanged minimal-evidence
  conservatism: a lone error never triggers). WIN is removed; there is
  no window and no forgetting.

Structural difference from the windowed trigger (frozen, verifiable
from source): the trigger condition is cumulative since the last burst
rather than windowed over the last 8 episodes. This is a
single-variable change: binary failure flags and FMIN=2 are unchanged;
only the memory horizon changes (infinite until reset vs 8). On dense
failure streams the two policies fire at identical episodes (the 2nd
failure); on sparse streams (failures spaced more than 8 apart) only
POLICY-C fires.

Superset property (frozen): any stream on which the windowed trigger
fires also fires POLICY-C at the same or an earlier episode, because 2
failures within 8 episodes are 2 cumulative failures since the last
reset, and resets coincide whenever both policies fired at the same
prior episode. POLICY-C additionally fires on sparse streams the
windowed trigger provably misses.

Generic-machinery argument (frozen): POLICY-C monitors only the
learner's own binary error stream with one counter and one threshold
comparison. It contains no domain content, no task knowledge, no
semantic cases, no candidate families, no modes, no bridges. It is a
failure monitor, not a solution enumerator. Adding researcher-authored
semantic cases (SUB, DIV, PARITY, 2-threshold COND, or equivalents) in
response to this prereg is forbidden and voids it.

Trace grammar (frozen): `TRIGGER <ep> cumfail=<c> buf=<b>` where <c>
is the cumulative failure count at firing (>= 2) and <b> is the trial
buffer fill. CONSTRUCT, STALL, EP, EXEC, SUMMARY lines are unchanged
from the base implementation.

## 3. Base mechanism

Base: the 2321pdt windowed-trigger implementation
`docs/lab/rsi/runs/wave-20261001-2321pdt/F1/impl/f1_learn.zag` (binary
sha256 6f2b155b233a95ad1a8323e8565b9a798dc822db6eff57e065b71b5be8882847),
copied into this lane as `impl/f1_learn_c.zag`. The only source change
is the trigger section (window win/wnn replaced by the cumulative
counter; TRIGGER log line updated). `impl/f1_isa.zag` is copied
unchanged. The constructor (trial_move, burst, supersede) is
byte-identical logic.

## 4. Fresh sealed fixture design (frozen)

World family: y = 2 iff x0==x1 else 0, 2 inputs, seed predicts
constant 0 so errors occur exactly on E episodes (x0==x1). The law is
held constant; only the E interleaving density varies. Train: 24
episodes, x in 0..7. Hidden: 30 masked probes, x in 8..23, E/U by
unpatterned rng bit, disjoint from train.

Sparse patterns (fresh kinds, defined here):
- eqF: train E iff (i % 9) == 0. E at train episodes 0, 9, 18.
  Failure gaps of 9 exceed WIN=8, so the windowed trigger provably
  never fires (no 8-window contains 2 failures); POLICY-C fires at
  episode 9.
- eqG: train E iff (i % 12) == 0. E at train episodes 0, 12.
  POLICY-C fires at episode 12; windowed provably never fires.

Generator: lane `dev/f1_wgen2.zag` (pure Zag, written after this
prereg commits), deterministic in (kind, seed, n); hide/truth pairs
share (kind, seed, n) and differ only in masking; x-generation follows
the prior wave's wgen discipline (LCG, same ranges).

Frozen seed map (fresh series, never used by any prior wave):
- sF_train: eqF, seed 9501, n=24, train
- sF_hidden: eqF, seed 9502, n=30, hide; sF_truth: eqF, seed 9502,
  n=30, truth
- sG_train: eqG, seed 9503, n=24, train
- sG_hidden: eqG, seed 9504, n=30, hide; sG_truth: eqG, seed 9504,
  n=30, truth
- c0_clean: zero (1 input, y=0 always, x0=i), seed 9505, n=30, train

The fixture SHA-256 manifest (`sealed6/FIXTURE_SHA256.txt`) is
committed before any sealed run begins. A spec-conformance check
(E-positions in the train fixtures match the preregistered patterns)
runs at generation time; x values are not inspected before runs.

## 5. Regression suite (existing sealed fixtures, read-only)

The new binary is run on prior waves' sealed fixtures to prove no
regression. All are used read-only; their hashes were recorded in
their own preregs.

- T-A, T-B, T-C, T-D trains + hidden/truth (2321pdt sealed/):
  dense interleaving controls.
- R-W3 train + hidden/truth (2321pdt sealed/): law-change control.
- R-W2 train + hidden/truth (2321pdt sealed/): constructor-overfit
  control (report-only bar, see section 6).
- W2, W3 trains + hidden/truth (2021pdt sealed/): original passing
  families.
- C-A clean, C-B train+clean, C-C train+clean (2321pdt sealed/):
  false-positive controls (0 TRIGGER lines expected).
- 7300-series: 24 sum2 worlds, train + hidden/truth
  (F1-REPAIR2 sealed5/): the largest labeled corpus; per-seed
  CORRECT/OVERFIT labels frozen in SEALED_EVAL_REPAIR2.md section 3.

## 6. Run protocol per fixture (frozen binaries, read-only controls)

New binary `impl/f1_learn_c` (compiled from the frozen lane source
with the pinned znc; sha256 recorded before runs):
- sF/sG: train (seed in) -> state/trace/pred; hidden (masked, trained
  state in) -> pred; hidden ablation (masked, seed state in) -> pred.
- c0_clean, cA_clean: (seed in) -> trace.
- cB/cC: train (seed in) -> state; clean (trained state in) -> trace.
- T-*/R-W2/R-W3/W2/W3: train (seed in) -> state/trace/pred; hidden
  (trained state in) -> pred.
- 7300-series x24: train (seed in) -> state/trace/pred; hidden
  (trained state in) -> pred.

Control binary (windowed, sha256
6f2b155b233a95ad1a8323e8565b9a798dc822db6eff57e065b71b5be8882847,
read-only, never modified): sF_train and sG_train (seed in) ->
trace, to verify the gap premise (0 TRIGGER lines expected).

3/3 byte-identical reruns per invocation (cmp-verified), all
invocations.

Scoring: pure-Zag scorer (`f1_score acc`, `f1_score mem`) copied
read-only into this lane. Signature extraction: lane pure-Zag probe
(implements exactly the section 2 grammar), written after this prereg
commits.

## 7. Frozen kill bars

### K-CUM-FIRE (primary: fires on sparse interleaved errors)

On sF_train and sG_train (new binary, seed state in): the trace
contains at least one TRIGGER line with episode index < 24.
Expected: sF fires at episode 9, sG at episode 12. A missing trigger
on either pattern trips the bar.

### K-CUM-GAP (the gap premise; control discriminates)

Windowed control binary on sF_train and sG_train: 0 TRIGGER lines on
both. If the control fires on either, the sparse-gap premise is false
and this prereg is VOID (battery miscalibrated), not BUILD-PASS.

### K-CUM-LEARN (the trigger enables learning, not just firing)

Hidden accuracy on sF_hidden and sG_hidden (30 probes, trained state
in): at least 80 percent (24/30) on each. Below 80 percent on either
trips the bar. Firing without learning is a hollow fix and fails
here.

### K-CUM-TRACE (construction follows the trigger)

On sF_train and sG_train: at least 2 CONSTRUCT events with episode
indices at or after the first TRIGGER episode, and no structure
isomorphic to the final main graph in learner state before the first
construction event (seed holds [WRITE r0] only). Fewer than 2 events
trips the bar.

### K-CUM-CLEAN (no false positives; frozen rate 0)

0 TRIGGER lines on each of: c0_clean (new binary, seed state),
cA_clean.ep (new binary, seed state), cB_clean.ep (new binary,
cB-trained state), cC_clean.ep (new binary, cC-trained state). Any
trigger on any clean run trips the bar.

### K-REG-IDENTITY (dense streams: identical firing, no regression)

On T-A, T-B, T-C, T-D trains: new binary first-TRIGGER episode equals
the old binary's (2, 3, 4, 1 respectively); TRIGGER-episode-normalized
traces (TRIGGER lines reduced to their episode index) are identical
between old and new binaries; hidden accuracy equals the old 30/30 on
all four. Any deviation trips the bar.

### K-REG-RW3 (law-change control)

New binary on rW3: hidden 30/30 and at least 2 CONSTRUCT events
across the run. Below on either trips the bar.

### K-REG-W2W3 (original passing families)

New binary on 2021pdt w2 and w3: hidden equals the old 30/30 on both.
Any decrease trips the bar.

### K-REG-7300 (largest labeled corpus; no flips)

New binary on the 24 7300-series sum2 worlds: zero
CORRECT-to-OVERFIT flips relative to the windowed binary's frozen
labels (18 CORRECT seeds must stay CORRECT; seed 19 non-degenerate
OVERFIT and seeds 18, 20, 21 D-seed OVERFITs may stay OVERFIT or flip
to CORRECT). One flip trips the bar. Classification: CORRECT iff
hidden accuracy >= 80 percent via `f1_score acc`, identical to
REPAIR2.

### K-REG-RW2 (report-only, non-decisive)

New binary on rW2: hidden accuracy reported; PASS iff new hidden >=
old hidden (0/30). Rationale (frozen): rW2's 0/30 is a proven
pre-existing constructor limitation (old binary identical), and this
lane does not change the constructor; demanding >= 80 percent would
re-freeze a failed bar without structural difference on the
constructor side. This bar cannot decide BUILD-PASS alone.

### K-ABL-SPARSE (the learned structure is load-bearing)

On sF_hidden (30 probes): trained-state accuracy minus seed-state
(ablated) accuracy >= 40 percentage points. Below 40pp trips the bar.

### K-BASE-SPARSE (beats the trivial baseline by a margin)

Exact-match memorizer (same 24-episode example budget, `f1_score
mem`) on sF_hidden: learner accuracy minus memorizer accuracy >= 40
percentage points. Below 40pp trips the bar.

### K-C0A (source audit still clean)

grep over the frozen lane sources (`impl/f1_learn_c.zag`,
`impl/f1_isa.zag`, `dev/*.zag`) for (i) forbidden protected-semantic
markers (FIND_POLYNOMIAL_ORDER, DETECT_NEGATION, BUILD_CAUSAL_RULE,
LEARN_PROCEDURE, FIND_THRESHOLD, MAKE_CONDITIONAL and
benchmark/domain equivalents), (ii) downgrade kill-pattern markers
(COUPLED, SPECIALIZE, REIFY, SPLIT_SCAN, COND(, SUB, DIV, PARITY
researcher-addition markers), (iii) menu/kit/candidate-family markers
(menu, kit_, candidate_list, template): zero hits required. Any hit
trips the bar. The frozen ISA op dispatch is permitted machinery.

## 8. Determinism standard and void conditions

3/3 byte-identical reruns per invocation (cmp-verified); SHA-256 of
each raw output recorded. Zero randomness in decision paths. Any
nondeterminism voids that invocation's results.

VOID (terminal for this prereg): ordering violation (this prereg's
commit not strictly before the implementation commit; any fresh
fixture generated, any probe built, or any fresh learner run executed
before this prereg's commit), contamination, toolchain violation,
seal leak (builder inspection of fresh fixture x values before runs;
choosing seeds, kinds, or definitions after seeing fresh results),
more than 2 trace-parse failures, any nondeterminism, or any
forbidden researcher response (adding SUB, DIV, PARITY, 2-threshold
COND, or other researcher-authored semantic cases).

## 9. Verdict rule

- BUILD-PASS: every decisive frozen bar passes. This is not a
  promotion and not an L3 claim. The bounded L2+ ceiling stands. The
  trigger is generic infrastructure; it enables learning but invents
  nothing itself.
- BUILD-FAIL: any decisive kill bar trips. The failed bar and the
  evidence are named.
- K-REG-RW2 is report-only and non-decisive by frozen design.

A frozen kill bar is never weakened to force a pass. Verdicts name
the exact frozen bars that governed them. No frozen bar from
PREREG_F1.md (wave-20261001-2021pdt) or PREREG_TRIG.md
(wave-20261001-2321pdt) is weakened, reinterpreted, or re-frozen by
this prereg.

## 10. Architecture accounting

No file outside this lane is touched: 0 cognition-substrate source
lines added. The change is confined to the lane's standalone
experiment copy (`impl/f1_learn_c.zag` trigger section; `impl/f1_isa.zag`
unchanged). The sealed eval records the exact added/removed line
count from the source diff. New hardcoded semantic cases: 0. New
modes: 0. New bridges: 0. New routers: 0. New task-specific handlers:
0. Capability-source delta approaches zero: the new capability
(learning from sparsely interleaved errors) comes from the generic
monitor's memory horizon, not from new researcher-written machinery.

No em-dashes are used in this document.
