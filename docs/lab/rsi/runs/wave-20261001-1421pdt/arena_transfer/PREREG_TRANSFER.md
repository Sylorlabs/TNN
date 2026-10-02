# PREREG_TRANSFER.md: TRANSFER / REUSE sealed evaluation (lane B, wave-20261001-1421pdt)

Status: FROZEN at write time. Implementation (.zag) written only after this
file is complete. Kill bars below may not be altered after results are seen.
Any amendment requires a new prereg version and a fresh run.

## 1. Claim under test

Transfer, operationalized as: a structure S_A learned by the learner during
a LEARN phase on world A improves later cognition on world B, where A and B
are materially different (different surface form, different law family).
This is the direct behavioral probe of Criterion 0 clause C0-D (cognitive
reuse): the invented structure must improve later cognition, existence alone
is insufficient.

Scoring follows the baseline arena C6 rule
(docs/lab/research-lead/overnight-20260928/baseline_arena/BASELINE_ARENA_DESIGN.md):
examples-to-criterion on B with the A-structure present, divided by
examples-to-criterion of a fresh control. Score S = 1 - (T_B / F_B),
clipped to [0, 1]. Positive means transfer helped.

Prior state (parent-provided): the actual TNN contestant measures 0.676
(v4, 7/7 kill bars passed); the clean canonical score remains 0.573 until a
clean refreeze reproduces composition without contamination. Transfer is a
zero capability in both. This lane does not move the canonical 0.573. Any
positive result here is a CANDIDATE score pending the refreeze protocol
with the actual frozen TNN-2 contestant, stated explicitly in the result.

## 2. Worlds (sealed, fixed literals in the implementation)

World A (LEARN):
- Surface: decimal integer tokens, space separated, e.g. "3 7 11 15 19".
- Law family: arithmetic progression t(n+1) = t(n) + c, c constant per
  sequence, c drawn from {3, 7, -4, 12, -9, 5}, start values varied
  (negatives included, no zeros), lengths 5 to 7.
- 24 training sequences, 12 held-out sequences. Task: next-term prediction
  (given first L-1 terms, predict term L).

World B (TRANSFER):
- Surface: letter-code tokens per the briefing code table (base-26:
  1..26 map to A..Z, 27..702 to two letters, larger to three letters),
  space separated, e.g. "B D H P AF" for 2 4 8 16 32. The code table is
  part of the world briefing and is identical across all conditions; the
  decoder is interface machinery, not a learned structure.
- Law family: geometric progression t(n+1) = r * t(n), r in {2, 3} per
  sequence, starts and lengths varied (lengths 5 to 6, all terms positive
  and within code range).
- 24 training sequences, 12 held-out sequences, all (start, r, length)
  combos disjoint from training. Task: next-term prediction, same as A.

Material difference (frozen as K5): surface differs (digit tokens vs letter
tokens; verified zero shared tokens) and law family differs (additive vs
multiplicative; verified each world's law fails on every sequence of the
other world).

## 3. Learner (simulated, generic; evaluator-only, not TNN)

Hypothesis space (fixed generic forms over integer sequences, no domain
detectors):
- H_COPY: predict t(L) = t(L-1).
- H_MEAN: predict t(L) = integer mean of t(1)..t(L-1).
- H_DIFF: if all consecutive differences of t(1)..t(L-1) are equal to c,
  predict t(L-1) + c, else the hypothesis fails to form (counts as wrong).
- H_RATIO: if every t(i) != 0 and every t(i+1) is an exact integer multiple
  of t(i) with equal quotient r, predict t(L-1) * r, else fails to form.

Learner state: an ordered checklist of the four hypothesis ids, failed
marks, a current hypothesis (or none), a consecutive-support counter, and a
next-trial pointer. Default no-experience checklist order (simplest first):
[H_COPY, H_MEAN, H_DIFF, H_RATIO].

Online protocol (identical in A and B): training sequences arrive one at a
time. The learner makes exactly ONE prediction per sequence (using the
current hypothesis, re-fit on the first L-1 terms; or, with no current
hypothesis, the first non-failed checklist item). Correct: support += 1
(a trial success installs the hypothesis as current). Wrong: support = 0,
current hypothesis discarded on counterexample, tried item marked failed.

Learning rule (A phase only): when a hypothesis is confirmed as current,
the checklist is reordered to [confirmed] + [untried in default relative
order] + [tried-and-failed in trial order]. The resulting checklist is the
learned structure S_A. It persists in learner state across the A to B
phase boundary. Failed marks reset at the phase boundary; only the ORDER
carries (conservative: T does not get to skip baselines for free).

Criterion: support reaches V = 3 consecutive correct predictions AND the
current hypothesis scores 12/12 on the fixed held-out set (re-fit per
held-out sequence). Examples-to-criterion = number of training sequences
consumed when the criterion is first met. Caps: A_MAX = 24, B_MAX = 24.
If the cap is hit without criterion, examples-to-criterion = cap.

## 4. Conditions (same binary, same briefing, same B order and held-out)

- T (transfer): A phase (learn S_A; A criterion must be met), then B phase
  with S_A in state. Measure T_B.
- F (fresh): state reset; B phase only with the default checklist.
  Measure F_B.
- X (ablated): A phase, then S_A wiped (checklist reset to default,
  current cleared), then B phase. Measure X_B. The gain must vanish here
  or it is not attributable to S_A.
- M (storage control): memorize all A raw strings mapped to their next
  terms; on B, verbatim lookup of the raw B surface string; on miss (always,
  by the surface shift) predict 0 (never correct: all B terms >= 2).
  Measure M_B. Pure storage must score zero.

## 5. Scoring

S = 1 - (T_B / F_B), clipped to [0, 1], reported scaled x10000 as an
integer. Design walkthrough predicts T_B = 4, F_B = 6, X_B = 6, M_B = 24,
S = 0.3333. These are predictions, not results; the run decides.

## 6. Frozen kill bars

- K1 TRANSFER GAIN: S >= 0.25.
- K2 ABLATION ATTRIBUTION: |X_B - F_B| / F_B <= 0.10 AND X_B > T_B.
- K3 ANTI-MEMORIZATION: M_B >= F_B (storage gain <= 0).
- K4 DETERMINISM: 3/3 runs byte-identical full stdout (cmp).
- K5 MATERIAL DIFFERENCE: (a) zero shared tokens between A-train raw
  strings and B-train raw strings, verified in-run and reported;
  (b) the A-law (constant differences) is rejected on all 36 B sequences
  (24 train + 12 held-out) and the B-law (constant exact integer ratios)
  is rejected on all 36 A sequences, verified in-run and reported.
- K6 CRITERION VALIDITY: A phase reaches criterion within A_MAX and F
  reaches the B criterion within B_MAX; otherwise the comparison is VOID
  (no learned structure, or no valid fresh baseline).
- K7 PURE ZAG: one znc-compiled binary; shell only for compile, run, cmp,
  sha256sum; no python/python3 or any other interpreter invoked anywhere
  in the lane; no .py files in the lane directory.
- K8 NO-CONFOUND: identical B briefing, identical B training order,
  identical B held-out set across T/F/X; the only difference between T and
  X/F entering B is the presence of S_A.

Verdict mapping: all of K1..K8 PASS gives a CANDIDATE transfer score S
(pending the refreeze protocol with the frozen TNN-2 contestant; does not
move the canonical 0.573). Any bar FAIL gives per-bar FAIL verdict. K6
FAIL gives VOID.

## 7. Architecture accounting (frozen expectations)

- TNN source touched: none. This is an evaluator-only protocol probe.
- Cognition source lines added: the single .zag harness (a few hundred
  lines), all inside the lane directory.
- New hardcoded semantic cases: 0. H_COPY/H_MEAN/H_DIFF/H_RATIO are generic
  sequence operations in the evaluator's hypothesis space, not TNN
  semantic cases and not domain detectors.
- New modes: 0. New bridges: 0. New routers: 0. New task-specific
  handlers: 0.
- Learner-state structures created: the checklist order + current
  hypothesis inside the simulated learner state (S_A).
- The decoder for the B surface is briefing interface machinery, applied
  identically in T/F/X, never counted as learned.

## 8. Honest boundaries

This evaluation uses a minimal simulated learner, not the frozen TNN-2
binary (no runnable TNN-2 binary was available to this lane). It validates
the transfer measurement protocol and the C0-D effect size achievable with
a generic learner under the frozen bars. It does not establish that TNN-2
itself transfers. A positive S is a CANDIDATE for the arena composition,
admissible only through the clean refreeze protocol.

Freeze declaration: this prereg is frozen as written. The implementation
follows it. No bar is altered after results are seen.
