# PREREG_TRIG: Windowed Failure-Density Trigger for Interleaved-Error Learning

Lane F1, wave wave-20261001-2321pdt. This prereg is frozen alone before any
implementation exists. It addresses the primary killing bar from
wave-20261001-2021pdt (K-C0C TRIP on W1, 15/30): the K1=2
consecutive-failure trigger never fires on interleaved errors.

## 0. Step 0 (toolchain guard)

Safebin activated and verified before any other work; recorded in
NAMECHECK.md Step 0 of this lane. PATH is safebin only. `which python3`
prints nothing. All work is pure Zag compiled by the pinned znc, or shell
invoking znc, running binaries, git ops, cmp/sha256sum, grep, and file
moves/copies. Any forbidden executable invocation is automatic PROCESS-FAIL.

## 1. The defect (from the prior wave, re-derived)

The prior candidate (impl/f1_learn.zag, wave-20261001-2021pdt) monitored its
own prediction failures with a consecutive counter: `consec` incremented on
err > 0, reset to 0 on err = 0, firing a construction burst at consec >= 2.
On sealed family W1 (y = 2 iff x0==x1 else 0, train episodes alternating
equal/unequal), every correct prediction reset the counter, so the trigger
never fired, the constructor never ran, and hidden accuracy was 15/30.
A non-sealed diagnostic (reordered W1, consecutive errors) confirmed the
constructor discovers EQ when the trigger fires, isolating the defect to
the trigger, not to EQ indiscoverability.

## 2. The candidate: windowed failure-density trigger

Replace the consecutive counter with a sliding window over the learner's
own binary error stream:

- WIN = 8: window over the last 8 truth-episodes (each recorded as
  1 = prediction failure with err > 0, else 0). WIN matches the BUFN = 8
  trial-buffer horizon: the trigger fires on the same episode horizon the
  trial evaluates. This is the principled constant choice, not a tuned one.
- FMIN = 2: fire when failures in the window >= 2. FMIN = 2 is the minimal
  evidence distinguishing a failure pattern from a single fluke; it
  preserves the old K1 = 2 conservatism (a lone error never triggers)
  while generalizing from consecutive to interleaved.
- On fire: log TRIGGER with the window failure count, run the construction
  burst unchanged (up to KB = 4 single-element trial events), then clear
  the window so the same failures cannot retrigger.

Superset property (frozen, verifiable from source): the old fire condition
(2 consecutive failures) implies the new one (2 failures in the window).
Therefore on any stream where the old trigger fired, the new trigger fires
at the same episode; on interleaved streams the new trigger additionally
fires. All previously passing behaviors (W2 composition, W3 revision,
C0-D transfer, K-REV) are preserved by construction.

Generic-machinery argument (frozen): the trigger monitors only the
learner's own error stream. It contains no domain content, no task
knowledge, no semantic cases, no candidate families. It is a failure
monitor, not a solution enumerator. Adding researcher-authored semantic
cases (SUB, DIV, PARITY, threshold COND, or equivalents) in response to
this prereg is forbidden and voids it.

## 3. Sealed interleaving patterns (frozen)

The trigger must fire on all four preregistered interleaving patterns,
instantiated as fresh sealed worlds (new seeds, law y = 2 iff x0==x1 else
0, 2 inputs). The law is held constant across patterns to isolate the
trigger variable; only the input arrangement interleaves errors.

- Pattern A (alternating): train episodes E,U,E,U,... (E: x0==x1; U:
  x0!=x1). Error density 50%, never 2 consecutive.
- Pattern B (1-in-3): every 3rd train episode is E. Density 33%.
- Pattern C (1-in-4): every 4th train episode is E. Density 25%.
- Pattern D (bursty): repeating E,E,U,U,U,U,U,U. Density 25%, bursty.

Seed predicts constant 0, so errors occur exactly on E episodes. Train: 24
episodes, x in 0..7. Hidden: 30 masked probes, x in 8..23, E/U by
unpatterned rng bit, disjoint from train. Fixture seeds and SHA-256 in
section 8.

## 4. Frozen kill bars

### K-TRIG-FIRE (positive: fires on interleaved errors)

On each sealed train run T-A, T-B, T-C, T-D (from the seed state), the
trace contains at least one TRIGGER line with episode index < 12.
A missing trigger on any pattern trips the bar.

### K-TRACE (construction follows the trigger)

On each T-* train run, the trace shows at least 2 CONSTRUCT events with
episode indices at or after the first TRIGGER, and no structure isomorphic
to the final one in learner state before the first construction event.
Fewer than 2 events trips the bar.

### K-LEARN-INTERLEAVED (the trigger enables learning, not just firing)

On each T-* hidden set (30 masked probes, trained state in), accuracy is
at least 80 percent (24/30). Below 80 percent on any pattern trips the
bar. Firing without learning is a hollow fix and fails here.

### K-TRIG-CLEAN (no false positives; frozen rate 0)

Three clean worlds, zero prediction failures in the stream:
- C-A: seed state on y = 0 constant (30 episodes).
- C-B: sum2-trained state (y = 2*(x0+x1)) on fresh same-law episodes
  (30, x in 5..14).
- C-C: quad-trained state (y = 4x) on fresh same-law episodes
  (30, x in 12..41).
The trace of each clean run contains 0 TRIGGER lines. Any trigger on a
clean world trips the bar. The frozen false-positive rate is 0.

### K-C0C-REG (no regression; the C0-C battery still discriminates)

Fresh-seed equivalents of the prior wave's passing families, same laws:
- R-W2: y = 2*(x0+x1), 24 train (x in 0..4), 30 hidden (x in 5..14).
  Bars: hidden at least 80 percent; final main-graph op sequence
  non-isomorphic to the [4 2] training reference (material composition
  difference preserved).
- R-W3: law change 2x (12 episodes, x 0..11) to 4x (12 episodes, x 0..11);
  30 hidden on the new law (x 12..41). Bars: hidden at least 80 percent;
  at least 2 CONSTRUCT events across the run (K-TRACE).
Any regression trips the bar. If the new trigger broke previously passing
behavior, this battery catches it: the C0-C family still trips correctly.

### K-ABL-TA (the learned structure is load-bearing)

On T-A hidden: trained-state accuracy minus seed-state (ablated) accuracy
is at least 40 percentage points. Below 40pp trips the bar.

### K-BASE-TA (beats the trivial baseline by a margin)

Exact-match memorizer (same 24-episode example budget) on T-A hidden:
learner accuracy minus memorizer accuracy is at least 40 percentage
points. (The memorizer scores about 50 percent by predicting 0 on the
U episodes; the bar is the margin, not an absolute memorizer ceiling,
because the sparse positive class makes 50 percent the trivial floor.)

### K-C0A (source audit still clean)

grep over the frozen implementation sources for forbidden protected
semantics (FIND_POLYNOMIAL_ORDER, DETECT_NEGATION, BUILD_CAUSAL_RULE,
LEARN_PROCEDURE, FIND_THRESHOLD, MAKE_CONDITIONAL), downgrade kill-pattern
markers (COUPLED, COND(, SPECIALIZE, REIFY, SPLIT_SCAN), and
researcher-named node type tags / semantic branches / menu / kit /
candidate-family markers: zero hits outside comments denying them. The
only tag dispatch is the frozen ISA op dispatch (generic execution
machinery). Any hit trips the bar.

### NC-TRIG (negative control: the battery has teeth)

The prior wave's frozen binary (dev/bin/f1_learn, sha256
0c571abca5a3c16695115228114c327bb3370081304c9c3a1ea1354840aa2727)
run on sealed T-A train produces 0 TRIGGER lines, reproducing the W1
defect. If the old binary triggers on T-A, the battery is miscalibrated
and the prereg is void (not a pass).

## 5. Sealed evaluation protocol (ordering is load-bearing)

1. This prereg is committed alone. Its SHA-256 and commit are recorded
   before any implementation file exists.
2. The implementation (impl/f1_learn.zag with the windowed trigger;
   impl/f1_isa.zag unchanged from the prior wave) is written only after
   that commit. The implementation-freeze commit records source SHA-256.
3. Sealed runs use the frozen binary only. The builder lane never saw the
   sealed fixture contents before the sealed run (fixtures were generated
   by the generator with fresh seeds; only hashes were recorded in this
   prereg).
4. Each sealed invocation is executed 3 times; outputs are cmp-verified
   byte-identical and hashed.
5. Verdicts are computed against the frozen bars above. No bar may be
   altered after the sealed run begins.

Run matrix (frozen binary `f1_learn <episodes> <state_in|-> <state_out>
<trace> <pred>`):
- T-*: train (seed in) -> state/trace/pred; hidden (masked, trained state
  in) -> pred; hidden ablation (masked, seed in) -> pred. Score with the
  pure-Zag scorer against truth; memorizer from scorer.
- C-A: clean (seed in). C-B: train (seed in) -> state; clean (trained
  state in). C-C: train (seed in) -> state; clean (trained state in).
  Count TRIGGER lines in clean traces.
- R-W2, R-W3: train (seed in) -> state/trace/pred; hidden (masked, trained
  state in) -> pred. Score; op-sequence isomorphism vs [4 2].
- NC-TRIG: old binary on T-A train; count TRIGGER lines.

## 6. Determinism standard

3/3 byte-identical reruns (cmp-verified); SHA-256 of each raw output
recorded. Zero randomness in decision paths. Any nondeterminism voids
the run.

## 7. Toolchain purity and architecture accounting

Pure Zag for implementation, harnesses, verifiers, scorers, fixture
provisioning, and analysis, compiled by the pinned znc. Shell invokes
only znc, runs compiled binaries, performs git ops, cmp/sha256sum, grep,
and file moves/copies. No Python anywhere.

Architecture accounting: 0 cognition-substrate source lines added (no
file outside this lane is touched); new hardcoded semantic cases 0;
new modes 0; new bridges 0; new routers 0; new task-specific handlers 0.
The change is confined to the lane's standalone experiment
(impl/f1_learn.zag trigger section). Capability-source delta approaches
zero: the new capability (learning from interleaved errors) comes from
the generic monitor, not from new researcher-written machinery.

## 8. Sealed fixture manifests (recorded BEFORE any sealed run)

Generator: dev/f1_wgen.zag (pure Zag), seeds below are fresh (dev used
9000-series; sealed uses the series below). hide/truth pairs share
(kind, seed, n) and differ only in masking.

```
01c633c1cbe2db73511d8dd36ef20e70d06af8a9966c5fcc0b7bff67a999180d  tC_train.ep
0e7ed0a4397d450b0b46a5b2d6226cbd24288953c95a174fe0a7bf498653eeee  tB_hidden.ep
1862569e645f7ac47a7619ed2d800eaecec09bec9257c9003bbd2f32920f1954  rW2_train.ep
2136ec910581debbf785c3060d2937d2ce0ad8e6152f3fbb035336519a303279  tC_hidden.ep
272a7fed9db129fc0e7d0067b311e86305af80cf4f7ccaf410d20925261f2a0f  tB_hidden.truth
3633539fe11e7e591bf0f8d870ee795407e423ccfc6fc491ece80eb058b6e344  tA_hidden.ep
3c25415a40cace4122ce15ac9f20cd6a3c1f68c0825a8f4523cedcb793b9fed9  tA_hidden.truth
3f0af82c5014f8f55f95f95ac1008c707d26906eea3423660debd197e5af8640  rW2_hidden.truth
73e24306d530e2b1c39a46d7c51a12fda99c34c68d3d9f9a4907b3570f87b10c  cB_train.ep
76ddbc984c6b9a69f804697b6d5af3249a830de9901a6efd714ce69531417500  tC_hidden.truth
80525da2961c51954ec7fb91c35df7c2cac0c62577326e53f90bf4f256c61458  cB_clean.ep
8b6ac312335bcdfcc83d76d94a0fbd3dc3c5652da4f3915a76ee200d63d23d31  cA_clean.ep
990fe8e07393edd0ba10f91fc99c658bbb4ee4c5af802cc44c4843af8007a381  tA_train.ep
a69d66fc1139d4d0cf0875f464d6448a147dc9ea87a59746fd14ca675bbe09e6  tD_train.ep
abc076155e7661c1e09ee48aa2ba37c4bd49e82df102d4381511730299638302  cC_clean.ep
abc076155e7661c1e09ee48aa2ba37c4bd49e82df102d4381511730299638302  rW3_hidden.truth
c244255ba36a041c784caa76fa5add5353d38e96fde24850613bf866e86ac325  tD_hidden.ep
cedde4d86fb856640bbd1de487c48636b60a477f3de0c7cc5b9afa955b29d4d6  tB_train.ep
d110c10f6e54d8d2f27fc48a7ef4369df6ef6767ce2888556b6fcf513433635f  rW3_train.ep
d1414d1c97f90ad5c36602ea2e688262ecbb270cd0ff786532fb86953c26f8b6  rW3_hidden.ep
de74c3a0d301888a021819714c16f71ee85ba9ff01065957e3b503b874204fc3  cC_train.ep
e46eeed138754eb1c0e46498c3d2a25366115eb03f1e5c3d95b77bb032e63b45  tD_hidden.truth
eafd36ea28d91786a37159fffdb399aef57b33d6597b8520448f80338c90e970  rW2_hidden.ep
```

Seed map: T-A eqA 1101/1102; T-B eqB 1201/1202; T-C eqC 1301/1302;
T-D eqD 1401/1402; C-A zero 3101; C-B sum2 2101/2102; C-C quad 2201/2202;
R-W2 sum2 2301/2302; R-W3 chg24 2401/2402. (cC_clean.ep and
rW3_hidden.truth share content: both are x=12..41, y=4x, deterministic;
used in different roles with different trained states.)

## 9. Verdict rule and void conditions

- BUILD-PASS: every frozen bar passes. This is not a promotion and not an
  L3 claim. The bounded L2+ ceiling stands. The trigger is generic
  infrastructure; it enables learning but invents nothing itself.
- BUILD-FAIL: any kill bar trips. The failed bar and the evidence are
  named.
- VOID: ordering violation, contamination, toolchain violation, seal leak,
  or any forbidden researcher response (adding SUB, DIV, PARITY,
  2-threshold COND, or other researcher-authored semantic cases). A VOID
  verdict is terminal for this prereg.

A frozen kill bar is never weakened to force a pass. Verdicts name the
exact frozen bars that governed them. No em-dashes are used in this
document.
