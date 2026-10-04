# AMENDMENT A1 (PRE-EXECUTION, TRANSPARENT) to PREREG.md

Lane: `docs/lab/research-lead/overnight-20260928/p7_belief_inquiry/`
Date: 2026-10-03. Status: recorded **before the implementation was
written and before any battery was executed.** No result exists yet at
this commit; the lane directory contains only `PREREG.md`,
`NAMECHECK.md` and this file.

The brief requires honest reporting, so both the reason and the
consequence are stated in full. **No kill bar is weakened, moved, or
deleted.** The 35 bar names and their structural content are unchanged;
what changes is the world's payoff scalars, two derived thresholds that
depend on them, two world constructions, and one derived-quantity
definition.

## A1.1 Defect: the prereg's own FP-M7 was unreachable by construction

PREREG 3.1 fixed `C_RIGHT=40, C_WRONG=120`, giving
`MBREAK = C_WRONG*255/(C_RIGHT+C_WRONG) = 191`, i.e. a commitment needs
a posterior share of at least 192/255 = 75%. The prereg's FP-M7 requires
that ONE decisive experiment, appended as one more observation, lift the
posterior past 191. With one root on each side and one more observation
on one side, the best attainable share is 2/3 = 170/255 even with a zero
prior. Hand-derived: solving `(160+m)*255/(352+m) >= 192` gives
`m >= 425`, but a single observation's mass is bounded by
`U_UNIT = 255`. So FP-M7 could never pass with the prereg's own
scalars. This is an internal inconsistency in the prereg, not a result.

Fix: **symmetric stakes.** `C_RIGHT=100`, `C_WRONG=100`, `C_PROBE=6`,
`C_SAFE=8`, `C_DEADLINE=30`, `HZN=2`. Then
`MBREAK = 100*255/200 = 127`, a commitment needs share >= 128/255 =
50%, which a 2-of-3 evidence ratio clears (153/255 after the decisive
observation). `C_PROBE=6` and `C_SAFE=8` are unchanged.
`PRIOR_MASS=32` and `U_UNIT=255` are unchanged.

Consequence for the bars: MBREAK enters only K-B30, K-B31 and the
status derivation. Every other bar is a comparison or an argmax
identity and is untouched.

## A1.2 Defect: a mass tie is not a reversal

PREREG 3.6 K-B23 says "add two INDEPENDENT roots for H1: `w=(288,288,32)`,
`P` tied, `bp2_select==-3`, argmax ledger value recorded as a revision".
With the argmax taken over the probability vector, a tie leaves the
argmax at the lowest index, so no reversal and no revision edge can be
produced. Internally inconsistent.

Fix: K-B23 uses **three** independent roots for H1, giving
`w=(288,416,32)`, `PROB=(99,144,11)`, a strict reversal, the
`b_rev` increment and the REVISION reason edge on the H1 belief, with
`bp2_has_k3(m_H0)==0` (no retirement, no deletion). K-B23
**additionally** asserts the two-root case `w=(288,288,32)`:
`bp2_select==-3` and NO revision edge, because a tie is not a
reversal. The bar therefore covers both the tie and the reversal.

K-B24 (case 4, reversion) follows K-B23, so it carries three roots for
H1 and adds two more for H0: `w=(544,416,32)`,
`PROB=(139,106,8)`, argmax back to H0, a second REVISION edge, eight
live ledger claims, both beliefs live. The prereg's `w=(544,288,32)`
is replaced by `w=(544,416,32)`; the structural content (second
reversal, records preserved, nothing retired) is unchanged.

## A1.3 Fix: "challenger mass" must mean evidence mass, not prior mass

PREREG 3.2 K-B11 reasons "challenger mass is 0" for the one-sided case.
Under the prereg's own `prior(h)=32`, the prior itself contributes 32
per hypothesis, so the total non-argmax mass is 64, never 0. The
derived quantity is defined wrongly.

Fix: `challenger mass` is the sum of `mass(c)` over live claims whose
`val` is a non-argmax hypothesis. Priors are excluded. This is what the
status derivation actually needs to know: whether any EVIDENCE sits
against the leader. World M is unaffected (`cm=128`, from the S4 root);
the one-sided case of K-B11 becomes correct (`cm=0` -> `KNOWN`).

## A1.4 Clarification: what the C5 sweep's alternative side is

PREREG 3.3 specifies the sweep over `n=1..5` copies of one root report
for H0, but does not say what else the world contains. Implementation
detail, frozen here: the world also contains exactly **one independent
root report for H1** and nothing else. So the copied arm is
1-vs-1 for every `n` and the independent arm is `n`-vs-1.

Hand-derived for this world (honest learner, `PRIOR_MASS=32`,
`U_UNIT=255`, `rel=128` everywhere, root mass 128):
- copied arm: `w=(32+128, 160, 32) = (160,160,32)` for every `n`;
  `P[H0]=115` constant. MBREAK 127 is never crossed, so the frozen
  layer refuses and the learner never commits, for any `n`.
- independent arm: `w=(32+128n, 160, 32)`;
  `P[H0] = 115, 153, 174, 188, 198` for `n=1..5`: strictly increasing,
  rise 83.
- with `ABL_PLAIN` on the COPIED arm (mass 255 per claim):
  `P[H0] = 120, 160, 182, 195, 204` for `n=1..5`: rise 84, and
  MBREAK 127 is crossed from `n=2` onward, so the ablation both
  reports a growing confidence AND commits to H0, which the honest
  learner never does. This decision flip is the strongest form of the
  double-counting evidence available and is reported alongside
  K-B16.

## A1.5 Defect retained, NOT fixed: FP-M9 is expected to fail

PREREG 3.1 FP-M9 predicted that with `ABL_PLAIN=1` on world M the
learner would `COMMIT(H0)` and realise `-120`. Hand-derivation shows it
will instead `RUN(channel 0)`: with symmetric stakes the value of
information from a cheap, bounded-downside experiment dominates
commitment even at a reported share of 165/255, because the downside
branch falls back to WITHHOLD at `-C_DEADLINE` while the upside branch
reaches ~94%. **FP-M9 is left exactly as written and will be reported as
a failed prediction.** The scalars were not chosen to rescue it, and the
decision-flip evidence in A1.4 is offered as supplementary, not as a
replacement bar.

## A1.6 Re-derived hand values under the amended scalars

- World M honest: `w=(160,160,32)`, `P=(115,115,23)`,
  `bp2_select==-3`, status `CONTESTED`, learner action `RUN(channel 0)`.
- World M after the decisive observation (outcome 1, source 0, rel 128,
  mass 128): `w=(160,288,32)`, `P=(85,153,17)`, `153 >= 128`,
  `bp2_select -> m_H1`, learner action `COMMIT(H1)`, realised `+100`.
- World M `ABL_PLAIN`: `w=(1052,542,32)`, `P=(165,85,5)`,
  `165 >= 128`, `bp2_select -> m_H0`, realised `-100`.
- Case 1: `P[H0]=208`, `KNOWN`, `bp2_select -> m_H0`.
- Case 8a: `P=(139,96,19)`, argmax observation side.
  Case 8b: `P=(46,187,20)`, argmax testimony side.
- Channel-0 branch posteriors on world M: `(225,25,5)`, `(79,159,15)`,
  `(106,106,42)`; channel 1 (flat) reproduces its input distribution.

## A1.7 What did NOT change
The structural invariant SI-1..SI-5, the no-mode-label rule, the
whole substrate reuse list and its SHA-256s, the ledger/mass/
reliability/contingency formulas of PREREG 2.3, the ablation switches,
the five selectors, the baseline list, the ignorance and
representation-insufficient bars K-B29/K-B30, the consequence
sensitivity bar K-B31, the claim IDs C500..C506, and every
determinism/hygiene bar. No bar was added, removed, or relaxed.