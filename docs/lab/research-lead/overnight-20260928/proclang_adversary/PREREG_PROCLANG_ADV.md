# PREREG: Independent Adversary for H-PROCLANG1 (machinery-vs-content attack)

Status: FROZEN. Committed before any attack implementation, build, or run.
Role: step 6/10 of the 11-step frontier promotion pipeline
(alternative-explanation attack).
Worker: independent adversary subagent.
Date: 2026-09-29/30.

## Target

H-PROCLANG1. Builder commit: `647b4096c`. Repro: `046ab1724`
(REPRODUCED, BUILD-PASS 9/9, pure Zag). Frozen builder prereg:
`docs/lab/research-lead/overnight-20260928/proclang_frontier/PREREG_PROCLANG1.md`.

## Standing assumption

The "invention" is researcher-supplied machinery until proven otherwise.

## The caveat under attack (frozen in the builder prereg)

Builder's disclosed position: "the case-split MACHINERY (threshold scan over
the input coordinate, reification into COND) is researcher-supplied generic
machinery; the CONTENT (that a split is needed at all, the threshold value,
the sub-programs) is learner-created from data."

Builder's defense: COND(t, A, B) with A != B is provably inexpressible in D0,
so the operator extends the representational language per Criterion 0.

## Adversary null hypothesis H0

The learner performs deterministic model selection over a finite
researcher-enumerated family of 1-level threshold stumps. The operator FORM
(threshold predicate on the input coordinate, two D0 branches, reification,
cond_eval semantics) is researcher-authored code. The "content" is the unique
forced parameter setting of that form on the training data.

Under the mandatory Criterion 0 ("the researcher must not add P; searching a
finite authored menu does not count"), H0 implies H-PROCLANG1 is bounded L2+
structural search with reification machinery, NOT L3 representational
invention.

## Scope

BUILD-PASS as an engineering result (9/9 bars, independently reproduced) is
NOT contested. What is contested is the Criterion-0 / L3 interpretation that
the builder's prereg explicitly referred to the independent adversary.

## Attack A1: decision-stump enumeration

Question: is Phase B distinguishable from exhaustive enumeration of all
1-level decision stumps over D0 pieces?

Method: analytic, from the committed builder source `proclang1.zag` at
`647b4096c` plus the frozen raw output. Phase B scans every integer threshold
t in [xmin-1, xmax+1] ascending and, per t, runs fit_best (complete
enumeration of all 2955 D0 programs in a fixed deterministic order with
strict improvement) on each side. The COND form, its evaluation semantics
(cond_eval), and the reification procedure exist in researcher code before
any data is seen. The emitted operator is the argmin triple of this scan.

ATTACK-SUCCEEDS iff both hold:
(i) the COND operator form (threshold predicate on the input coordinate,
two D0 branches, reification into a persistent operator, evaluation
semantics) is fixed in researcher-authored code independent of the data;
(ii) the specific invented (t, L, R) triple is one of the complete
candidates evaluated by the researcher's scan, i.e. it was enumerated as a
complete candidate before selection.

Consequence of SUCCEEDS: DOWNGRADE the Criterion-0/L3 reading. The learner
performed model selection over a researcher-enumerated finite family. This
violates L3 criterion 2 ("not enumerated as one complete candidate",
applied to the invented operator itself) and the exclusion "brute-force
enumerating final candidates from a prewritten DSL". The representational
form was researcher-supplied; only parameter values were data-determined.

## Attack A2: machinery ablation

Question: without the threshold-scan machinery, can the learner still invent
COND or any non-D0 operator?

Method: build `adv_ablation.zag`, the H-PROCLANG1 learner with the Phase-B
block removed: on Phase-A inadequacy it emits NO_INVENTION_MECHANISM and
creates no operator. Run the four frozen tasks T1..T4 (same worlds and
training ranges as the builder). Pure Zag.

ATTACK-SUCCEEDS iff: zero INVENT/REVISE events on all four tasks, best-D0
training mismatches > 0 on all four tasks, final library size 0, and the
only operator-creating code path in the committed source is Phase B's
reification block.

Consequence of SUCCEEDS: the invention capacity resides entirely in the
researcher-supplied machinery; the learner has no independent
language-expansion capacity. This locates the creation of the operator form
in researcher code, supporting the A1 downgrade under "the researcher must
not add P". Honest counterpoint (recorded now): A2 alone does not kill the
claim, because nobody asserted invention without machinery; its force is as
part of the conjunction A1-A4.

## Attack A3: generality

Question: can the machinery invent an operator form outside the researcher's
anticipated 1-threshold shape?

Method: build `adv_generality.zag`, the full learner (Phase A + Phase B,
unchanged) applied to two new tasks, on a fresh operator library:

T5 (bump): y = 1 if -5 <= x <= 5 else -1. Train x in [-20, 20] (41 points).
T6 (parity): y = 1 if x even else -1. Train x in [-20, 20] (41 points).

Frozen in this prereg (D0-inadequacy):
T5: at (-6, -5, -4), y = (-1, 1, 1); an affine f would need f(-4) = 3, but
y(-4) = 1. No D0 program fits even three points.
T6: at (-1, 0, 1), y = (-1, 1, -1); -1 + -1 != 2 * 1. No D0 program fits
even three points.

Frozen in this prereg (no 1-threshold stump achieves total 0):
T5, t in [-21, 21]:
- t <= -5: side R contains (4, 5, 6) with y (1, 1, -1); affine forces
f(6) = 1, contradiction.
- t >= 7: side L contains (-6, -5, -4) with y (-1, 1, 1); affine forces
f(-4) = 3, contradiction.
- -4 <= t <= 6: side L contains (-7, -6, -5) with y (-1, -1, 1); affine
forces f(-5) = -1, contradiction.
Every threshold leaves a non-affine side; all D0 programs are affine (L0);
so min total >= 1.
T6, t in [-21, 21]:
- t <= -19: side R contains (0, 1, 2) with y (1, -1, 1); affine forces
f(2) = -3, contradiction.
- -18 <= t <= 18: side R contains (18, 19, 20) with y (1, -1, 1);
affine forces f(20) = -3, contradiction.
- t in {19, 20, 21}: side L contains (0, 1, 2) with y (1, -1, 1);
affine forces f(2) = -3, contradiction.
Every threshold leaves a non-affine side; so min total >= 1.
T5 needs a 2-threshold (interval) form; T6 needs an unbounded non-threshold
form. Neither is a 1-level stump.

ATTACK-SUCCEEDS iff: the full learner emits FAILURE with Phase-B min total
> 0 on BOTH T5 and T6, while Phase A also fails (mismatches > 0) on both.
That is, the machinery cannot invent the needed non-1-threshold form
despite D0-inadequacy.

Consequence of SUCCEEDS: DOWNGRADE. The "language expansion" is confined to
the researcher's anticipated 1-threshold form. The learner cannot invent
unanticipated operator forms.

## Attack A4: content triviality

Question: given the machinery and the data, is the invented content
(t, L, R) forced (unique), or does the learner exercise genuine choice?

Method: build `adv_forced.zag`. For each frozen task T1..T4 with its
training set: (i) count thresholds t with Phase-B total 0; (ii) for the
winning t, enumerate every D0 program with 0 mismatches on each side and
check each agrees with the fit_best choice on probe x in [-100, 100].

Frozen analytic note: all D0 programs are affine (machine-checked L0); two
affine functions agreeing on 2 or more points are identical everywhere;
each winning side has at least 18 training points.

ATTACK-SUCCEEDS iff: for every task T1..T4, exactly one threshold achieves
total 0, AND every zero-mismatch D0 program on each winning side computes
the same function as the chosen program on the full probe range (zero
disagreements). Then the function content is uniquely determined and only
the encoding is picked by the researcher's fixed deterministic enumeration
order.

Consequence of SUCCEEDS: DOWNGRADE. The "content creation" is deterministic
computation of the unique answer, not creation underdetermined by data; any
correct implementation of the machinery returns the identical triple.

## Overall verdict rule

- 4/4 ATTACK-SUCCEEDS: the L3 / Criterion-0 interpretation is KILLED.
H-PROCLANG1 stands as a BUILD-PASS engineering result (bounded L2+
structural search with reification machinery). It may not advance toward
SURVIVES on a representational-invention reading. A follow-up may re-enter
only if the learner supplies an unanticipated operator form (not a
researcher-enumerated finite family) with underdetermined content.
- Any ATTACK-FAILS: report exactly which attack failed and why; the
corresponding downgrade is withdrawn. Partial success still constrains the
interpretation per the consequence clauses above.

## Governance (frozen)

- Pure Zag only: implementation, builds, runs, analysis via bash, git, znc,
grep, awk, cmp, md5sum, diff. No Python anywhere. Disclosure does not cure.
- No em dashes in any documentation (byte-checked before commit).
- Commit only owned paths under
docs/lab/research-lead/overnight-20260928/proclang_adversary/.
- This prereg is committed BEFORE any attack implementation, build, or run.
- Commits stay local. No push without explicit authorization.
