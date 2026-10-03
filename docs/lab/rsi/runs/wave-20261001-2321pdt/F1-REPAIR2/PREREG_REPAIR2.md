# PREREG_REPAIR2: S-prime confirmation and repair-time policy

Lane F1-REPAIR2, wave wave-20261001-2321pdt. Replacement worker for
the F1-REPAIR lane, which closed GREEDY-CONFIRMED per its frozen
rule while trace evidence showed the buf=8 clause was overfit:
under the relaxed signature S-prime (a later burst driving
trial-buffer error to zero, any buffer size), repair-to-zero iff
CORRECT on 20/20 degenerate-path seeds (11/11 fresh 6100-series +
9/9 5100-series training). This prereg is frozen alone (separate
commit) before any fresh sealed fixture is generated, any probe is
built, or any fresh sealed run executes. It is a fresh
preregistration, not a salvage: the F1-REPAIR verdict
GREEDY-CONFIRMED stands on its frozen rule.

No em-dashes are used in this document.

## 0. Step 0 (toolchain guard)

Safebin activated and verified before any other work; recorded in
NAMECHECK.md Step 0 of this lane. PATH is safebin only. `which
python3` prints nothing. All work is pure Zag compiled by the
pinned znc, or shell invoking znc, running binaries, git ops,
cmp/sha256sum, grep, and file moves/copies. Any forbidden
executable invocation is automatic PROCESS-FAIL.

Pre-prereg work only (not implementation): read-only inspection of
committed 5100/6100 traces with grep/awk (no probe built), and
read-only extraction of committed tool binaries via git show (no
fresh fixture generated, no fresh learner run executed). The
calibration that motivates POLICY-R is frozen in
dev/CALIBRATION_5100_6100_POLICY.md, committed with this prereg.

## 1. Background

F1-REPAIR sealed verdict: GREEDY-CONFIRMED (misc 6/24 on the
frozen signature with the buf=8 clause), with the mechanistic
post-hoc showing the counterexample (6100 seed 10) was repaired
by a partial-buffer (buf=4) to-zero burst the frozen signature
missed. Under S-prime the 6100 D-subset separates 11/11 and the
5100 training D-subset separates 9/9. Two questions remain:

- Part A: does S-prime hold on genuinely fresh sealed worlds?
- Part B: what makes a later burst run to zero vs stall?

## 2. Frozen definitions

The frozen F1 binary is
docs/lab/rsi/runs/wave-20261001-2321pdt/F1/impl/f1_learn, sha256
6f2b155b233a95ad1a8323e8565b9a798dc822db6eff57e065b71b5be8882847
(verified before runs; read-only; never modified).

Trace grammar (frozen; observed identically in all sealed traces
to date):
- `TRIGGER <ep> winfail=<f> win=<w> buf=<b>`
- `CONSTRUCT <ep> <k> NODE id=<id> op=ADD p1=<a> p2=<b> p3=<c> err_before=<e0> err_after=<e1>`
- `STALL <ep> nodes=<n> buf_err=<e>`
Operand codes: 0 = accumulator r0, 8 = feature f0, 9 = feature
f1.

- T1(seed) = episode index on the first TRIGGER line. A trace
  with no TRIGGER line is NOTRIG.
- A burst at episode t = the CONSTRUCT lines with episode t that
  immediately follow the TRIGGER t line (before the next
  TRIGGER/STALL/EXEC/SUMMARY line). A burst with zero CONSTRUCT
  lines is stall-only.
- D-SEED (degenerate-path seed): identical to F1-REPAIR
  PREREG_REPAIR.md section 2: the first-trigger burst has at
  least two CONSTRUCT lines; c0 has op=ADD with p2 == p3 (call
  it f, the doubled feature); c1 has op=ADD with p1 == 0; and
  neither c1.p2 nor c1.p3 equals COMP(f), where COMP swaps 8
  and 9.
- S-PRIME S'(seed) = 1 iff at least one REPAIR-BURST event
  exists in the train trace, else 0. REPAIR-BURST event: a
  TRIGGER line at episode t such that (i) t > T1, (ii) the
  burst at t contains at least one CONSTRUCT line, (iii) the
  last CONSTRUCT line of the burst at t has err_after=0.
  Buffer size is unrestricted (this is the relaxed clause).
- DOUBLING construct: op=ADD with p1 == 0 and p2 == p3 and p2
  in {8, 9}. In trace terms it overwrites the accumulator r0
  with f+f, discarding whatever chain r0 previously held.
- POLICY-R (frozen repair-time policy hypothesis): for every
  TRIGGER at t > T1 whose burst commits at least one
  CONSTRUCT, the burst runs to err_after=0 iff its FIRST
  committed construct is a DOUBLING construct. If the first
  construct is not a doubling (accumulator-preserving add),
  the burst commits exactly one construct and stalls with
  err_after > 0.
- polok(seed) = 1 iff every TRIGGER at t > T1 with at least
  one CONSTRUCT satisfies POLICY-R in both directions, else 0.
  Seeds with no such burst are vacuously polok=1.

Classification (frozen, same as prior lanes): hidden accuracy on
the 30-probe masked set via the frozen pure-Zag f1_score;
CORRECT iff at least 24/30 (80 percent), else OVERFIT.

## 3. Frozen decision rules

Part A (S-prime confirmation, primary, conditioned on D):
Let D = number of D-seeds among the 24 fresh seeds. On the D
seeds, the prediction is: CORRECT iff S'=1, else OVERFIT.
(a) If D < 6: Part A REPAIR2-INDETERMINATE (underpowered).
(b) Else misc_D = number of D-seeds where the prediction is
    wrong. Part A PASS iff misc_D <= 2.

Part B (repair-time policy, all 24 seeds): misc_B = number of
fresh seeds with polok=0. Part B PASS iff misc_B <= 4.

Overall verdict:
- REPAIR2-CONFIRMED: Part A PASS and Part B PASS.
- REPAIR2-PARTIAL: Part A PASS and Part B FAIL.
- REPAIR2-FAIL: Part A FAIL.
- REPAIR2-INDETERMINATE: Part A gate (a) fired.
- VOID: see section 8.

Secondary (reported, non-decisive): S-prime applied
unconditionally to all 24 seeds (misclassification count), and
the per-burst POLICY-R contingency (complete vs stalled bursts
by first-construct form) for transparency.

Rationale for conditioning Part A on D (frozen, same as
F1-REPAIR): the repair question arises only where a degenerate
construct exists to be repaired. Part B is unconditioned
because POLICY-R is a general claim about later-burst
mechanics, testable on any seed with a later firing burst.

## 4. Calibration status (training knowledge, frozen before this prereg)

On the 20 D-seed traces available before this prereg (9 from
the 5100-series, 11 from the 6100-series; read-only awk
inspection, no probe built): 27 later-trigger bursts commit at
least one construct. 8 run to err_after=0, all with a
DOUBLING first construct; 19 stall after exactly one
construct with err_after > 0, all with an
accumulator-preserving first construct. Zero violations of
POLICY-R. Per-seed polok = 1 on all 20 D-seeds. Full burst
tables in dev/CALIBRATION_5100_6100_POLICY.md. This is
training knowledge; the sealed test below is the
out-of-sample check.

## 5. Fresh sealed fixture design (frozen)

World family: sum2, y = 2*(x0+x1), 2 inputs, exactly as in
F1-FOLLOWUP PREREG_PART2 section 2 and F1-REPAIR section 5:
- Train: 24 episodes, x0 and x1 in 0..4 (rng range 0..5),
  truth shown.
- Hidden: 30 episodes, x0 and x1 in 5..14 (rng range 5..15),
  truth masked as ?. Truth paired file shares the (kind,
  seed, n).

Generator: the pure-Zag f1_wgen copied read-only into this
lane (byte-identical reproduction of a reference fixture
verified before any sealed generation, same procedure as
F1-REPAIR).

Fresh seed series, never used by dev, F1 sealed (1100..3100),
Part 2 (5100-series), F1-REPAIR (6100-series), or F1-BUFFER
(8100-series): for i = 0..23 (N = 24 seeds),
- train seed = 7300 + 2*i
- hidden/truth seed = 7301 + 2*i

The seed series is frozen here. The fixture SHA-256 manifest
is committed (sealed5/FIXTURE_SHA256.txt) before any sealed
run begins.

## 6. Run protocol per seed (frozen binary, read-only)

- train (seed state in) -> state/trace/pred
- hidden (masked, trained state in) -> pred
- 3/3 byte-identical reruns per seed (cmp-verified), 24 seeds.

Scoring: the frozen pure-Zag f1_score copy, `f1_score acc
<pred> <truth>` on the 30-probe hidden set.

Signature/policy extraction: the frozen pure-Zag dev/r2sig
(implements exactly section 2, committed after this prereg),
reading only the train trace. Rule application: the frozen
pure-Zag dev/r2apply (implements exactly section 3). No
definition may differ from section 2; no rule may differ from
section 3.

## 7. Frozen bars

Part A PASS iff D >= 6 and misc_D <= 2 (section 3).
Part B PASS iff misc_B <= 4 (section 3).
Overall verdict per section 3. A frozen bar is never weakened
to force a verdict.

## 8. Determinism standard and void conditions

3/3 byte-identical reruns per seed (cmp-verified); SHA-256 of
each raw output recorded. Zero randomness in decision paths.
Any nondeterminism voids that seed's results.

VOID (terminal for this prereg): ordering violation (this
prereg's commit not strictly before the implementation
commit; any fresh fixture generated, any probe built, or any
fresh learner run executed before this prereg's commit),
contamination, toolchain violation, seal leak (e.g. choosing
the seed series or definitions after seeing fresh results),
more than 2 NOTRIG worlds, more than 2 trace-parse failures,
any nondeterminism, or any forbidden researcher response
(adding SUB, DIV, PARITY, 2-threshold COND, or other
researcher-authored semantic cases).

## 9. Architecture accounting

0 cognition-substrate source lines added; no file outside this
lane is touched; the F1, F1-FOLLOWUP, F1-BUFFER, and F1-REPAIR
lanes are read-only (sources extracted via git show where
needed; binaries used read-only with sha256 verification).
New code in this lane is sealed methodology only
(signature/policy probe, rule applier, run scripts). No new
semantic cases, modes, bridges, routers, or handlers. No fix
is proposed for the F1 line: this is mechanism
characterization, not a repair patch.

## 10. K-C0A audit (frozen requirement)

The verdict requires K-C0A PASS over all new lane code
(r2sig.zag, r2apply.zag, shell scripts): grep audit for
(i) forbidden protected-semantic markers
(FIND_POLYNOMIAL_ORDER, DETECT_NEGATION, BUILD_CAUSAL_RULE,
LEARN_PROCEDURE, FIND_THRESHOLD, MAKE_CONDITIONAL and
benchmark/domain equivalents), (ii) downgrade kill-pattern
markers (COUPLED, SPECIALIZE, REIFY, SPLIT_SCAN, COND(, SUB,
DIV, PARITY researcher-addition markers), (iii)
menu/kit/candidate-family markers (menu, kit_, candidate_list,
template). Zero hits required. The frozen binary is not
modified; the probe is an external trace reader, not learner
logic.

No em-dashes are used in this document.
