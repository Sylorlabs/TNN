# PREREG_PART1: Windowed failure-density trigger, corrected regression bar

Lane F1-FOLLOWUP, wave wave-20261001-2321pdt. This prereg is frozen
alone before any sealed run of this lane. It is a narrowed re-test of
the F1 windowed failure-density trigger with ONE corrected bar:
K-C0C-REG runs on the PRIOR WAVE's validated W2 fixtures instead of a
fresh seed, so trigger regression is no longer conflated with
constructor seed-robustness. The trigger is NOT redesigned. No new
implementation exists in this lane: the binary under test is the F1
frozen binary `impl/f1_learn` (sha256
6f2b155b233a95ad1a8323e8565b9a798dc822db6eff57e065b71b5be8882847,
implementation freeze commit ba5ebbf8b on branch tnn-native-lab,
local only). The old-binary reference is wave-20261001-2021pdt F1
`dev/bin/f1_learn` (sha256
0c571abca5a3c16695115228114c327bb3370081304c9c3a1ea1354840aa2727).

## 0. Step 0 (toolchain guard)

Safebin activated and verified before any other work; recorded in
NAMECHECK.md Step 0 of this lane. PATH is safebin only. `which python3`
prints nothing. All work is pure Zag compiled by the pinned znc, or
shell invoking znc, running binaries, git ops, cmp/sha256sum, grep, and
file moves/copies. Any forbidden executable invocation is automatic
PROCESS-FAIL.

## 1. Subject (unchanged from F1)

The windowed failure-density trigger from F1 PREREG_TRIG.md section 2:
WIN = 8 sliding window over the learner's own binary truth-episode
error stream, FMIN = 2 (fire when at least 2 of the last 8
truth-episodes are prediction failures), clear the window on fire, run
the construction burst unchanged. The generic-machinery argument and
the forbidden researcher responses (SUB, DIV, PARITY, 2-threshold COND,
or equivalents) carry over unchanged; adding them voids this prereg.

## 2. Fixtures (copies, hash-verified, read-only from F1)

Interleaved patterns, clean worlds, and R-W3 use the F1 sealed
fixtures, copied into this lane's sealed/ and verified against the
hashes recorded in F1 PREREG_TRIG.md section 8 (F1 sealed/FIXTURE_SHA256.txt
must also verify before copying):

```
01c633c1cbe2db73511d8dd36ef20e70d06af8a9966c5fcc0b7bff67a999180d  tC_train.ep
2136ec910581debbf785c3060d2937d2ce0ad8e6152f3fbb035336519a303279  tC_hidden.ep
272a7fed9db129fc0e7d0067b311e86305af80cf4f7ccaf410d20925261f2a0f  tB_hidden.truth
3633539fe11e7e591bf0f8d870ee795407e423ccfc6fc491ece80eb058b6e344  tA_hidden.ep
3c25415a40cace4122ce15ac9f20cd6a3c1f68c0825a8f4523cedcb793b9fed9  tA_hidden.truth
73e24306d530e2b1c39a46d7c51a12fda99c34c68d3d9f9a4907b3570f87b10c  cB_train.ep
76ddbc984c6b9a69f804697b6d5af3249a830de9901a6efd714ce69531417500  tC_hidden.truth
80525da2961c51954ec7fb91c35df7c2cac0c62577326e53f90bf4f256c61458  cB_clean.ep
8b6ac312335bcdfcc83d76d94a0fbd3dc3c5652da4f3915a76ee200d63d23d31  cA_clean.ep
990fe8e07393edd0ba10f91fc99c658bbb4ee4c5af802cc44c4843af8007a381  tA_train.ep
a69d66fc1139d4d0cf0875f464d6448a147dc9ea87a59746fd14ca675bbe09e6  tD_train.ep
c244255ba36a041c784caa76fa5add5353d38e96fde24850613bf866e86ac325  tD_hidden.ep
cedde4d86fb856640bbd1de487c48636b60a477f3de0c7cc5b9afa955b29d4d6  tB_train.ep
d110c10f6e54d8d2f27fc48a7ef4369df6ef6767ce2888556b6fcf513433635f  rW3_train.ep
d1414d1c97f90ad5c36602ea2e688262ecbb270cd0ff786532fb86953c26f8b6  rW3_hidden.ep
de74c3a0d301888a021819714c16f71ee85ba9ff01065957e3b503b874204fc3  cC_train.ep
e46eeed138754eb1c0e46498c3d2a25366115eb03f1e5c3d95b77bb032e63b45  tD_hidden.truth
abc076155e7661c1e09ee48aa2ba37c4bd49e82df102d4381511730299638302  rW3_hidden.truth
eafd36ea28d91786a37159fffdb399aef57b33d6597b8520448f80338c90e970  rW2_hidden.ep
```

(The F1 R-W2 fixtures on the fresh sealed seed 2301 are deliberately
NOT reused here; that was the calibration mistake. The seed series
1100..3100 is otherwise untouched.)

The corrected regression leg uses the PRIOR WAVE's validated W2
fixtures (wave-20261001-2021pdt F1 sealed/, the exact fixtures on which
the old binary was characterized with TRIGGER ep 1, the same 3
constructs, 30/30 hidden, structure [4 4 4 2]), copied into this lane's
sealed/ and hash-verified:

```
2e27d8a58af8cd259d692235fe5b3d200b176c30d3ee808b180800b26f252012  w2_train.ep
613536078f8227f2bbaf676887c646ae2024647c7588aaa33c8014aeb207f34c  w2_hidden.ep
8cc652da1791226cd23e117dd32ed40bf39f6aeb2dc0a417ef88bd726884f6ff  w2_hidden.truth
```

## 3. Frozen kill bars

### K-TRIG-FIRE (unchanged)

On each sealed train run T-A, T-B, T-C, T-D (from the seed state), the
trace contains at least one TRIGGER line with episode index < 12.
A missing trigger on any pattern trips the bar.

### K-TRACE (unchanged)

On each T-* train run, the trace shows at least 2 CONSTRUCT events
with episode indices at or after the first TRIGGER, and no structure
isomorphic to the final one in learner state before the first
construction event. Fewer than 2 events trips the bar.

### K-LEARN-INTERLEAVED (unchanged)

On each T-* hidden set (30 masked probes, trained state in), accuracy
is at least 80 percent (24/30). Below 80 percent on any pattern trips
the bar.

### K-TRIG-CLEAN (unchanged; frozen rate 0)

Three clean worlds (C-A seed on y = 0 constant, 30 episodes; C-B
sum2-trained on fresh same-law episodes, 30; C-C quad-trained on fresh
same-law episodes, 30): each clean trace contains 0 TRIGGER lines.
Any trigger trips the bar.

### K-C0C-REG (CORRECTED)

Two legs on validated fixtures only.

Leg W2 (the correction): both the new binary and the old binary are
run on the prior wave's validated W2 fixtures above. The new binary
must reproduce the old binary's behavior exactly:
- same TRIGGER episode number(s) in the train trace (line formats
  differ, so the comparison is on episode numbers, not raw bytes);
- same CONSTRUCT event sequence in the same order: same count, same
  (ep, burst index, node id, op, p1, p2, p3, err_before, err_after)
  fields per event;
- identical final main-graph signature (f1_score sig on the final
  trained states);
- hidden accuracy 30/30 for the new binary, and its hidden pred
  outputs byte-identical to the old binary's on the same masked
  fixtures.
Any deviation in trigger episodes, construct sequence, signature,
accuracy, or pred outputs trips the bar. This is a pure no-regression
test: constructor seed-robustness is out of scope (it is Part 2's
subject).

Leg R-W3: on the F1 sealed R-W3 fixtures (validated by F1's passing
run): hidden at least 80 percent and at least 2 CONSTRUCT events
across the run. A regression here trips the bar.

### K-ABL-TA (unchanged)

On T-A hidden: trained-state accuracy minus seed-state (ablated)
accuracy is at least 40 percentage points.

### K-BASE-TA (unchanged)

On T-A hidden: learner accuracy minus exact-match memorizer accuracy
(same 24-episode budget) is at least 40 percentage points.

### K-C0A (unchanged)

grep over the frozen F1 implementation sources for forbidden protected
semantics (FIND_POLYNOMIAL_ORDER, DETECT_NEGATION, BUILD_CAUSAL_RULE,
LEARN_PROCEDURE, FIND_THRESHOLD, MAKE_CONDITIONAL), downgrade
kill-pattern markers (COUPLED, COND(, SPECIALIZE, REIFY, SPLIT_SCAN),
and researcher-named node type tags / semantic branches / menu / kit /
candidate-family markers: zero hits outside comments denying them.
Any hit trips the bar.

### NC-TRIG (unchanged)

The prior wave's frozen binary on sealed T-A train produces 0 TRIGGER
lines, reproducing the W1 defect. If the old binary triggers on T-A,
the battery is miscalibrated and this prereg is void (not a pass).

## 4. Sealed evaluation protocol (ordering is load-bearing)

1. This prereg is committed alone (with NAMECHECK.md only). No sealed
   run of this lane exists before that commit.
2. The binary under test is pre-frozen (F1 impl/f1_learn, sha256
   verified before every run); no implementation work occurs in this
   lane. A small pure-Zag trace comparator implementing the frozen
   W2-leg comparison spec is committed before the sealed runs; it
   encodes only the fields named in section 3 (K-C0C-REG Leg W2).
3. Fixtures are copied and hash-verified against the lists in
   section 2 before any run; the verified list is committed in
   sealed/FIXTURE_SHA256.txt.
4. Each sealed invocation is executed 3 times; outputs are
   cmp-verified byte-identical and hashed.
5. Verdicts are computed against the frozen bars above. No bar may be
   altered after the sealed run begins.

Run matrix (frozen binaries only):
- T-*: train (seed in) -> state/trace/pred; hidden (masked, trained
  state in) -> pred; hidden ablation (masked, seed in) -> pred. Score
  with the pure-Zag scorer against truth; memorizer from scorer.
- C-A: clean (seed in). C-B: train (seed in) -> state; clean (trained
  state in). C-C: train (seed in) -> state; clean (trained state in).
  Count TRIGGER lines in clean traces.
- W2-validated: train (seed in) -> state/trace/pred for BOTH binaries;
  hidden (masked, trained state in) -> pred for BOTH binaries. Compare
  per K-C0C-REG Leg W2.
- R-W3: train (seed in) -> state/trace/pred; hidden (masked, trained
  state in) -> pred. Score.
- NC-TRIG: old binary on T-A train; count TRIGGER lines.

## 5. Determinism standard

3/3 byte-identical reruns (cmp-verified); SHA-256 of each raw output
recorded. Zero randomness in decision paths. Any nondeterminism voids
the run.

## 6. Architecture accounting

0 cognition-substrate source lines added; no file outside this lane is
touched; the F1 lane is read-only. New hardcoded semantic cases 0;
new modes 0; new bridges 0; new routers 0; new task-specific handlers 0.
The only new code in this lane is sealed-evaluation methodology (the
trace comparator and run script), which is not the subject under test.

## 7. Verdict rule and void conditions

- BUILD-PASS: every frozen bar passes. This is not a promotion and not
  an L3 claim. The bounded L2+ ceiling stands. The trigger is generic
  infrastructure; it enables learning but invents nothing itself.
- BUILD-FAIL: any kill bar trips. The failed bar and the evidence are
  named.
- VOID: ordering violation, contamination, toolchain violation, seal
  leak, or any forbidden researcher response (adding SUB, DIV, PARITY,
  2-threshold COND, or other researcher-authored semantic cases). A VOID
  verdict is terminal for this prereg.

A frozen kill bar is never weakened to force a pass. Verdicts name the
exact frozen bars that governed them. No em-dashes are used in this
document.
