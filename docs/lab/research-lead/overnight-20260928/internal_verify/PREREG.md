# PREREG.md -- IVWC: Internal Verification via World Consequences

Frozen: 2026-10-02. This document fixes the experimental design and
the kill bars K1..K6. It must be committed ALONE (with NAMECHECK.md,
no implementation) before any implementation work. Amending a bar
after results invalidates the verdict.

## 1. Research question

Can a learner commit to a composition output plus its own confidence
score BEFORE any correctness signal, then receive pure environmental
consequences (not a score, not an answer comparison), update its own
evaluation of its usefulness from those consequences, and thereby
predict its future performance better? This tests learner-owned
internal verification as a replacement for harness-supplied expected
answers in composition research.

## 2. Frozen design

World: a 1D corridor of 20 cells (0..19). Each case is defined by
ground truth: a wall map (20 bytes, 0/1), an item map (20 bytes,
0/1), a start cell, and an energy budget E=36. All generation is
deterministic: LCG `s = (s*25173 + 13849) % 65536` (no i32 overflow),
world seed `7919*cid + 13`, belief seed `104729*cid + 7`.

- world_gen: cells 0 and 19 forced open. Other cells wall with
  probability 15%. Open cells hold an item with probability 25%.
  Start = first open cell at or after `2 + lcg % 16` (wraps).
- belief_gen (the learner's prior observation, produced ONCE in setup
  from truth; the learner never sees truth afterward): copy truth,
  then apply frozen noise. Wall belief flips with probability 12%
  (never the start cell). True items are dropped from belief with
  probability 15%. Empty true-open cells gain a phantom item belief
  with probability 18%. Start is believed exactly.

Learner composition (learner_compose, sees ONLY beliefs): a
NAV+GATHER composition. Visit believed-item cells in increasing cell
order. For each, check the believed-open interval between the current
believed position and the cell; if any believed wall lies inside,
skip it. Otherwise append unit moves toward it, then one GATHER.
Truncate the plan to E=36 actions (the learner knows its budget).
Outputs: the plan (bytes; 0=LEFT, 1=RIGHT, 2=GATHER; at most 64),
raw_conf = 100*G/max(1,L) where G = planned gathers and L = plan
length (the learner's honest belief-based estimate of items per unit
energy), and bucket b: 0 if G=0, 1 if G=1, 2 if G=2..3, 3 if G>=4.

World consequences (world_execute, sees truth + plan only): step the
plan through corridor physics. LEFT/RIGHT moves to an adjacent cell
if in bounds and open, else records a bump. GATHER collects an item
if the cell truly holds an uncollected one, else records a wasted
gather. Each action costs 1 energy. Consequences buffer: collected,
energy_used, bumps, wasted_gathers, final_pos, plan_len. There is NO
key, NO expected plan, NO reference output anywhere in the program;
consequences are physics outputs, and a "wrong" plan still produces
perfectly well-defined consequences.

Learner update (learner_update, sees ONLY bucket, raw_conf, and the
consequence buffer): actual_eff = 100*collected/max(1,energy_used);
err = raw_conf - actual_eff. Maintain per-bucket (n, sum_err) plus
global (n, sum_err). Calibrated prediction for a future case:
raw - sum_err[n]/n for its bucket (global fallback if the bucket is
empty), clamped to 0..100.

Phases in main (batched, in this order):
1. SETUP: generate truth+beliefs for N_TRAIN=24 cases (cid 0..23).
2. COMMIT (train): learner_compose on train beliefs. In-program
   counter asserts no world_execute call has happened yet (K1).
3. CONSEQUENCE (train): world_execute on committed train plans.
4. UPDATE (train): learner_update from train consequences. In-program
   check that at least one train case now calibrates differently
   from raw (K3).
5. SEALED SETUP: generate truth+beliefs for N_SEALED=12 fresh cases
   (cid 100..111).
6. SEALED COMMIT: learner_compose on sealed beliefs; record raw_conf
   and calibrated_conf (via the trained table).
7. SEALED CONSEQUENCE: world_execute on sealed plans; accumulate
   sum|raw-actual|, sum|calibrated-actual|, sum|ablation-actual|
   over the 12 sealed cases, where the ablation arm uses
   learner_calibrated with a zeroed (never updated) table, i.e. its
   confidence falls back to raw_conf on the identical sealed plans.

Secondary (reported, NOT a frozen bar): a shuffled-feedback arm that
runs the update phase with each train case paired to another case's
consequences (deterministic rotation by 7), to show the content of
the consequences matters, not just the act of updating.

## 3. Frozen kill bars

- K1 (commit before signal): PASS iff the in-program world-call
  counter equals 0 immediately after the train COMMIT phase AND the
  section-5 audit confirms code ordering (all learner_compose calls
  precede all world_execute calls) and the learner code section
  contains no world-truth tokens.
- K2 (consequence is not a disguised answer check): PASS iff the
  section-5 audits hold: no `expected|answer|key|target` tokens in
  src/ivwc.zag; world_execute performs no plan-to-key comparison
  (its only comparisons are physics: bounds, wall presence, item
  presence); learner_update's inputs are (table, bucket, raw_conf,
  consequences) only.
- K3 (confidence updates from consequences): PASS iff the in-program
  check finds at least one train case whose calibrated confidence
  differs from its raw confidence after the UPDATE phase.
- K4 (self-evaluation predicts future performance): PASS iff sealed
  sum|calibrated-actual| < sealed sum|raw-actual| (strict, integer).
- K5 (determinism): PASS iff 3 runs produce byte-identical stdout
  (equal sha256).
- K6 (ablation): PASS iff sealed sum|ablation-actual| >
  sealed sum|calibrated-actual| (strict, integer).
  Declared openly here (not discovered post-hoc): the no-feedback
  ablation's predictions equal raw_conf by construction (its table is
  never updated), so K6 tests the same integer inequality as K4
  through the necessity-of-feedback framing.

Verdict: BUILD-PASS iff K1..K6 all PASS. Any FAIL yields BUILD-FAIL
naming the failed bar. VOID conditions: any forbidden-interpreter
invocation during the wave (PROCESS-FAIL per governance), or any
amendment to this prereg after implementation begins.

## 4. What is NOT claimed

This is a mechanism test of internal verification, not a
composition-novelty claim and not an L3 claim. The NAV+GATHER
composition is deliberately simple; the target of the experiment is
the commit -> consequence -> self-evaluation loop. No claim is made
about cross-domain transfer or representational invention.

## 5. Frozen audit commands (run at report time, shell only)

A1 (K1 ordering): the first `world_execute(` call site in main must
have a greater line number than the last `learner_compose(` call
site in the train COMMIT phase; `grep -n "world_execute("
src/ivwc.zag` and `grep -n "learner_compose(" src/ivwc.zag`.

A2 (K1/K2 info hiding): extract the LEARNER section (between the
`// ===== LEARNER =====` and `// ===== MAIN =====` markers) and
confirm zero occurrences of `world_buf` / `world_off`:
`sed -n '/===== LEARNER =====/,/===== MAIN =====/p' src/ivwc.zag |
grep -c "world_buf\|world_off"` must print 0.

A3 (K2 no answer tokens): `grep -c -i -E "expected|answer|key|target"
src/ivwc.zag` must print 0. (The words appear in this PREREG.md and
in REPORT.md discussion only, never in the program.)

A4 (K2 no key comparison in world): `sed -n '/^fn world_execute/,/^}/p'
src/ivwc.zag | grep -c "plan\["` is informational; the audit is that
every `==` in world_execute/w_step compares against a physics
constant (0/1/19/bounds) or a map cell value, never against a stored
correct plan. There is no correct-plan buffer in the program; `grep -n
"correct\|reference_plan\|gold" src/ivwc.zag` must print 0.

A5 (K5): three runs, `sha256sum` equality.
