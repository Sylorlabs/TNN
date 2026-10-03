# PREREG_REPAIR: later-trigger repair dynamics vs greedy depth-1 trial

Lane F1-REPAIR, wave wave-20261001-2321pdt. This prereg is frozen
alone (separate commit) before any fresh sealed fixture is
generated, any probe is built, or any fresh sealed run executes.
It is a mechanistic discrimination experiment between two frozen
hypotheses about the F1 constructor's overfit, using the frozen F1
binary read-only. No implementation work touches the binary.

No em-dashes are used in this document.

## 0. Step 0 (toolchain guard)

Safebin activated and verified before any other work; recorded in
NAMECHECK.md Step 0 of this lane. PATH is safebin only. `which
python3` prints nothing. All work is pure Zag compiled by the
pinned znc, or shell invoking znc, running binaries, git ops,
cmp/sha256sum, grep, and file moves/copies. Any forbidden
executable invocation is automatic PROCESS-FAIL.

## 1. Background and the two hypotheses

F1-BUFFER sealed verdict: BUFFER-NOT-PREDICTIVE (misc 7/24). The
refined mechanistic picture: the first-trigger buffer fully
determines the greedy burst's second construct (5100-series seeds 6
and 18 share the exact first-trigger buffer multiset and take
identical first two constructs, including the degenerate re-add),
but the final OVERFIT vs CORRECT outcome is decided by
later-trigger repair dynamics (seed 6 is repaired by a later
full-buffer trigger; seed 18 stalls).

- H-REPAIR: seeds whose degenerate re-add is undone by a later
  full-buffer repair burst go CORRECT; seeds where the repair
  burst stalls (or never fires) go OVERFIT.
- H-GREEDY: repair bursts are epiphenomenal; the greedy depth-1
  trial's first two constructs fully determine the outcome
  regardless of later repair activity; some seed exists where the
  repair signature is identical but the outcome differs.

Design note (frozen): both hypotheses are stated in terms of the
degenerate re-add. A seed that never takes the degenerate path
has no degenerate construct to repair, so the repair question
does not arise for it. The primary discriminating analysis is
therefore conditioned on the degenerate-path subset D (frozen
definition in section 2). An unconditional analysis on all 24
seeds is reported as secondary, non-decisive transparency: it
conflates the greedy-path effect (complementary second construct
goes CORRECT with no repair needed) with the repair effect and
cannot discriminate the two hypotheses.

## 2. Frozen definitions

The frozen F1 binary is
docs/lab/rsi/runs/wave-20261001-2321pdt/F1/impl/f1_learn, sha256
6f2b155b233a95ad1a8323e8565b9a798dc822db6eff57e065b71b5be8882847
(verified before runs; read-only).

Trace grammar (frozen; observed identically in all sealed traces
to date):
- `TRIGGER <ep> winfail=<f> win=<w> buf=<b>`
- `CONSTRUCT <ep> <k> NODE id=<id> op=ADD p1=<a> p2=<b> p3=<c> err_before=<e0> err_after=<e1>`
- `STALL <ep> nodes=<n> buf_err=<e>`
Operand codes: 0 = accumulator r0, 8 = feature f0, 9 = feature
f1. BUFN = 8 is the frozen trial-buffer capacity (F1
IMPLEMENTATION.md section 1); buf=<b> counts buffered
truth-episodes, so buf=8 is a full trial buffer.

- T1(seed) = episode index on the first TRIGGER line. A trace
  with no TRIGGER line is NOTRIG.
- A burst at episode t = the CONSTRUCT lines with episode t that
  immediately follow the TRIGGER t line (before the next
  TRIGGER/STALL/EXEC/SUMMARY line). A burst with zero CONSTRUCT
  lines is stall-only.
- D-SEED (degenerate-path seed): the first-trigger burst has at
  least two CONSTRUCT lines; c0 (the first) has op=ADD with
  p2 == p3 (call it f, the doubled feature); c1 (the second) has
  op=ADD with p1 == 0; and neither c1.p2 nor c1.p3 equals
  COMP(f), where COMP swaps 8 and 9. This covers both observed
  degenerate forms: re-add of the same feature (ADD r0,r0,f) and
  accumulator doubling (ADD r0,r0,r0). The complementary add
  (ADD r0,r0,COMP(f)) is not degenerate. If c0 has p2 != p3, or
  the first burst has fewer than two CONSTRUCT lines, the seed is
  not a D-seed.
- REPAIR-BURST event: a TRIGGER line at episode t such that
  (i) t > T1, (ii) buf=8 (full trial buffer), (iii) the burst at
  t contains at least one CONSTRUCT line, (iv) the last
  CONSTRUCT line of the burst at t has err_after=0. In pure
  state/buffer terms: after the first trigger, on a full trial
  buffer, a later trigger's construct burst drives the
  trial-buffer error to zero; the degenerate construct is
  thereby revised because the structure that produced the
  buffer error no longer produces it.
- S(seed) = 1 iff at least one REPAIR-BURST event exists in the
  train trace, else 0.

Classification (frozen, same as prior lanes): hidden accuracy on
the 30-probe masked set via the frozen pure-Zag f1_score; CORRECT
iff at least 24/30 (80 percent), else OVERFIT.

## 3. Frozen decision rule (primary, conditioned on D)

Let D = number of D-seeds among the 24 fresh seeds. On the D
seeds, the prediction is: CORRECT iff S=1, else OVERFIT.

(a) If D < 6: verdict REPAIR-INDETERMINATE (underpowered: too few
    degenerate-path seeds to discriminate; exact numbers
    reported).
(b) Else if fewer than 2 D-seeds have S=1 or fewer than 2 have
    S=0: verdict REPAIR-INDETERMINATE (a signature value is
    unattested; exact numbers reported).
(c) Else if a counterexample pair exists within D (two D-seeds
    with identical S but different final labels):
    verdict GREEDY-CONFIRMED. Report the pair(s) and the full
    D-subset contingency.
(d) Else (S perfectly separates the D labels): if every S=1
    D-seed is CORRECT: verdict REPAIR-CONFIRMED. If the
    direction is inverted (S=1 D-seeds are OVERFIT): verdict
    REPAIR-INDETERMINATE (unexpected inversion; exact numbers
    reported).

Secondary (reported, non-decisive): the same prediction rule
applied unconditionally to all 24 seeds, with its
misclassification count and unconditional counterexample
pairs, for transparency.

Rationale for conditioning (frozen): H-GREEDY's existential
claim is fairly tested only where repair was at stake. A
non-degenerate CORRECT seed with S=0 paired against a
degenerate OVERFIT seed with S=0 would "confirm" H-GREEDY
without testing repair dynamics at all.

## 4. Calibration status (training knowledge, frozen before this prereg)

On the 24 committed 5100-series train traces
(dev/CALIBRATION_5100_REPAIR.md, committed with this prereg; no
fresh fixture generated, no fresh learner run executed, probe not
yet built): D = 9 seeds (0, 2, 3, 5, 6, 12, 13, 17, 18); the
conditioned rule separates them 9/9 with zero counterexample
pairs (S=1: seeds 0, 6, 12, all CORRECT; S=0: seeds 2, 3, 5, 13,
17, 18, all OVERFIT). The buf=8 requirement is load bearing
(seed 3's buf=6 trigger does not count); the to-zero
requirement is load bearing (partial constructs that stall in
seeds 5, 13, 17, 18 do not count). This is training knowledge;
the sealed test below is the out-of-sample check.

## 5. Fresh sealed fixture design (frozen)

World family: sum2, y = 2*(x0+x1), 2 inputs, exactly as in
F1-FOLLOWUP PREREG_PART2 section 2:
- Train: 24 episodes, x0 and x1 in 0..4 (rng range 0..5), truth shown.
- Hidden: 30 episodes, x0 and x1 in 5..14 (rng range 5..15), truth
  masked as ?. Truth paired file shares the (kind, seed, n).

Generator: the pure-Zag f1_wgen copied read-only into this lane
(byte-identical reproduction of a reference fixture verified
before any sealed generation).

Fresh seed series, never used by dev (9000-series), F1 sealed
(1100..3100), Part 2 (5100-series), or F1-BUFFER (8100-series):
for i = 0..23 (N = 24 seeds),
- train seed = 6100 + 2*i
- hidden/truth seed = 6101 + 2*i

The seed series is frozen here. The fixture SHA-256 manifest is
committed (sealed4/FIXTURE_SHA256.txt) before any sealed run
begins.

## 6. Run protocol per seed (frozen binary, read-only)

- train (seed state in) -> state/trace/pred
- hidden (masked, trained state in) -> pred
- 3/3 byte-identical reruns per seed (cmp-verified), 24 seeds.

Scoring: the frozen pure-Zag f1_score copy, `f1_score acc <pred>
<truth>` on the 30-probe hidden set.

Repair-signature extraction: the frozen pure-Zag dev/repsig
(implements exactly section 2, committed after this prereg),
reading only the train trace. Rule application: the frozen
pure-Zag dev/repapply (implements exactly section 3), reading
repsig output plus the frozen labels. No definition may differ
from section 2; no rule may differ from section 3.

## 7. Frozen bar

REPAIR-CONFIRMED iff section 3(a)-(b) pass, no counterexample
pair exists within D, and every S=1 D-seed is CORRECT (which
then implies the signature predicts the D labels with zero
misclassifications, satisfying the >= 22/24-style bar on the
discriminating subset).

GREEDY-CONFIRMED iff a counterexample pair exists within D
(identical repair signature, different outcome), per section
3(c).

Otherwise REPAIR-INDETERMINATE with the exact numbers.

## 8. Determinism standard

3/3 byte-identical reruns per seed (cmp-verified); SHA-256 of
each raw output recorded. Zero randomness in decision paths.
Any nondeterminism voids that seed's results.

## 9. Architecture accounting

0 cognition-substrate source lines added; no file outside this
lane is touched; the F1, F1-FOLLOWUP, and F1-BUFFER lanes are
read-only (sources extracted via git show where needed;
binaries used read-only with sha256 verification). New code in
this lane is sealed methodology only (repair-signature probe,
rule applier, run scripts). No new semantic cases, modes,
bridges, routers, or handlers.

## 10. K-C0A audit (frozen requirement)

The verdict requires K-C0A PASS over all new lane code
(repsig.zag, repapply.zag, shell scripts): grep audit for
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

## 11. Verdict rule and void conditions

- REPAIR-CONFIRMED: section 7 met; report the D-subset table,
  the repair episodes, and the secondary unconditional numbers.
- GREEDY-CONFIRMED: section 3(c) met; report the counterexample
  pair(s), the D-subset contingency, and the secondary numbers.
- REPAIR-INDETERMINATE: section 3(a), (b), or the inversion case;
  report the exact numbers and which gate fired.
- VOID: ordering violation (any fresh fixture generated, any
  probe built, or any fresh learner run executed before this
  prereg's commit), contamination, toolchain violation, seal leak
  (e.g. choosing the seed series or definitions after seeing
  fresh results), more than 2 NOTRIG worlds, more than 2
  trace-parse failures, any nondeterminism, or any forbidden
  researcher response (adding SUB, DIV, PARITY, 2-threshold COND,
  or other researcher-authored semantic cases). A VOID verdict is
  terminal for this prereg.

A frozen rule is never weakened to force a verdict. No em-dashes
are used in this document.
