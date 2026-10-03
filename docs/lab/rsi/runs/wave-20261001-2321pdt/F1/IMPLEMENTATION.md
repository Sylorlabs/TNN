# IMPLEMENTATION.md - F1 windowed failure-density trigger

Lane F1, wave wave-20261001-2321pdt. Implementation turn 2026-10-01 ~23:35 PDT.
Status: IMPLEMENTATION COMPLETE. READY FOR SEALED EVALUATION.

## 1. What changed (and what did not)

One targeted change to the prior wave's candidate, confined to
`impl/f1_learn.zag`. `impl/f1_isa.zag` is byte-identical to the prior
wave's (frozen protected ISA: READ, WRITE, COPY, ADD, EQ, BRANCH,
EXECUTE; generic execution and storage machinery only).

Changed: the failure monitor. The old `consec` consecutive-failure
counter (fire at K1 = 2 consecutive err > 0, reset on any correct
prediction) is replaced by a windowed failure-density trigger:

- `WIN() = 8`: sliding window over the last 8 truth-episodes, each stored
  as 1 (prediction failure, err > 0) or 0. Implemented by `win_push`
  (shifts when full) and `win_fails` (counts failures in the window).
- `FMIN() = 2`: fire when `win_fails >= 2`.
- On fire: log `TRIGGER <ep> winfail=<f> win=<w> buf=<b>`, run the
  construction burst unchanged, then clear the window (`wnn = 0`) so the
  same failures cannot retrigger.

Unchanged: the ISA, the EXECUTE interpreter, the trial
(single-ISA-element insertions before the terminal WRITE, frozen ISA
order, strictly-improving argmin), the burst (up to KB = 4 events),
supersession at the node cap, state persistence, trace format (except the
TRIGGER line fields), and all constants other than the trigger's
(KB = 4, MAXN = 24, BUFN = 8).

The superset property is verifiable from source: 2 consecutive failures
are 2 failures in the window, so every stream that fired the old trigger
fires the new one at the same episode. The window records only the
learner's own binary error stream: generic machinery, no domain content,
no semantic cases, no candidate families.

## 2. Frozen binary

`impl/f1_learn`, sha256
`6f2b155b233a95ad1a8323e8565b9a798dc822db6eff57e065b71b5be8882847`.
Compiled by the pinned znc from `impl/` (no dev files). Functional
equivalence with the dev-validated prototype verified by cmp on trace,
state, and pred outputs (identical).

Protocol unchanged: `f1_learn <episodes> <state_in|-> <state_out>
<trace> <pred>`.

## 3. Development validation (builder's own fixtures, not sealed data)

Dev fixtures used 9000-series seeds (sealed uses 1100-3100 series).
Prototype validated before the prereg commit; implementation is the
identical source.

Interleaved trigger tests (equality gate y = 2 iff x0==x1 else 0):
- eqA alternating: TRIGGER at ep 2 (winfail=2); 2 constructs
  (EQ r0,f0,f1 err 4->2; ADD r0,r0,r0 err 2->0); hidden 30/30 = 100%.
- eqB 1-in-3: TRIGGER at ep 3; 2 constructs; hidden 30/30.
- eqC 1-in-4: TRIGGER at ep 4; 2 constructs; hidden 30/30.
- eqD bursty 2-on-6-off: TRIGGER at ep 1 and ep 3; 4 constructs;
  hidden 30/30.
The old binary produces 0 triggers on the alternating pattern
(reproduces the W1 defect; used as NC-TRIG).

Clean worlds (false-positive check):
- C-A seed on y = 0: 0 triggers.
- C-B sum2-trained state on fresh y = 2*(x0+x1): 0 triggers, 30/30.
- C-C quad-trained state on fresh y = 4x: 0 triggers, 30/30.

Regression (fresh-seed equivalents of prior passing laws):
- sum2 y = 2*(x0+x1): hidden 30/30; structure [4 4 4 2],
  non-isomorphic to [4 2].
- chg24 2x->4x: hidden 30/30 after revision (TRIGGER 2, STALL 14,
  STALL 16, TRIGGER 18, construct 4x); 2+ construction events.

K-C0A audit: zero hits for forbidden protected semantics, downgrade
kill-pattern markers, and menu/kit/candidate-family markers in impl/.

## 4. Informative negatives (outside the trigger scope, reported honestly)

- sum3 y = 3*(x0+x1): the greedy depth-1 trial overfits (5 constructs,
  0/30 hidden). The OLD binary also fails identically (9 triggers,
  5 constructs, 0/30), confirming a pre-existing constructor limitation
  (greedy argmin on a small buffer), not a trigger regression. Not part
  of the frozen battery; the battery uses laws the constructor is known
  to solve so the trigger variable is isolated.
- chg25 2x->5x was generated but not used in the frozen battery for the
  same reason (harder law, constructor untested on it).

## 5. Architecture accounting

Baseline: prereg freeze commit 50de69403 (implementation files first
appear after it).

- Cognition-substrate source lines added: 0. No file outside this lane
  was touched.
- New hardcoded semantic cases: 0. New modes: 0. New bridges: 0.
  New routers: 0. New task-specific handlers: 0.
- Net source delta in impl/f1_learn.zag: the trigger section (constants
  K1/consec replaced by WIN/FMIN/win_push/win_fails, about +40/-10
  lines). No other logic touched.

## 6. Verdict for this turn

IMPLEMENTATION COMPLETE. READY FOR SEALED EVALUATION. The frozen binary
is `impl/f1_learn` (sha256 above). Dev logs and traces in `dev/work/`.
No em-dashes in this document.
