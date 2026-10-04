# H-PROCLANG1 Independent Adversary Report: machinery-vs-content (step 6/10)

Worker: independent adversary subagent (alternative-explanation attack).
Date: 2026-09-29/30.
Target: H-PROCLANG1, builder commit `647b4096c`, repro `046ab1724`
(REPRODUCED, BUILD-PASS 9/9). Adversary prereg: `PREREG_PROCLANG_ADV.md`
(frozen in commit `a0ea62532`, before any attack implementation, build,
or run).
Standing assumption (held throughout): the "invention" is
researcher-supplied machinery until proven otherwise.

Method: pure Zag only. Three new Zag programs assembled from the committed
builder source (verbatim `sed` extraction, no retyping of the D0 machinery)
plus new attack mains. Built with frozen toolchain `znc 2026.07.0-dev`.
Analysis used bash, git, znc, grep, cmp, md5sum only. No Python anywhere.
No em dashes in this document (byte-verified before commit).

Scope reminder: BUILD-PASS as an engineering result (9/9 bars, independently
reproduced) is NOT contested. What is contested is the Criterion-0 / L3
interpretation that the builder's prereg explicitly referred to the
independent adversary.

## Attack A1: decision-stump enumeration - ATTACK-SUCCEEDS

Method: analytic, from the committed builder source `proclang1.zag` at
`647b4096c` plus the frozen raw outputs. Both preregistered conditions hold.

Condition (i): the COND operator form is fixed in researcher-authored code
independent of the data.
- `proclang1.zag` line 149: `while(t<=xmax+1)` - the exhaustive threshold
  loop over the researcher-fixed range [xmin-1, xmax+1]. The learner never
  chooses a search range.
- Line 156: `if(x<t)` - the threshold predicate form is hardcoded. The
  learner never chooses a predicate family (no 2-D split, no interval, no
  non-threshold condition is expressible at this line).
- Lines 180-185 (`cond_eval`): the COND evaluation semantics (branch on
  threshold, evaluate a D0 program per side) are researcher-authored and
  exist before any data is seen.
- Lines 300-305: the ONLY writes to the operator library in the entire
  program. They sit inside Phase B's reification block. No other code path
  creates, modifies, or extends an operator.
- Lines 92-106 (`fit_best`): complete enumeration of all 2955 D0 programs
  in a fixed deterministic order (lengths ascending, op indices ascending,
  strict improvement); line 95 `while(pi<pn)` iterates the whole list.

Condition (ii): the specific invented (t, L, R) triple was enumerated as a
complete candidate before selection. Phase B evaluates, for every threshold
t, the best left/right D0 programs (each the argmin of the complete
enumeration), and emits the argmin triple. Supporting count from the A4 run
(`ADV_FORCED_RAW.txt`): `CANDIDATES n_thresh=43 progs=2955
triples=375477075` on every task - a finite researcher-defined family of
375,477,075 complete (threshold, leftProg, rightProg) candidates per task.
The builder's frozen raw output shows the emitted operator as this scan's
argmin (`SPLIT_SCAN n_thresh=43 best_t=0 ...`).

Consequence (per prereg): DOWNGRADE the Criterion-0/L3 reading. The learner
performed deterministic model selection over a researcher-enumerated finite
family. The invented operator itself WAS enumerated as one complete
candidate, violating L3 criterion 2 ("not enumerated as one complete
candidate") applied to the operator, and violating the exclusion
"brute-force enumerating final candidates from a prewritten DSL" (here the
prewritten language is the 1-level threshold-stump family defined by
`phaseB` + `cond_eval`). The representational FORM was researcher-supplied;
only parameter values were data-determined.

## Attack A2: machinery ablation - ATTACK-SUCCEEDS

Method: `adv_ablation.zag` = the H-PROCLANG1 learner with the Phase-B block
removed. On Phase-A inadequacy it emits `NO_INVENTION_MECHANISM` and creates
no operator. Ran the four frozen tasks T1..T4 (same worlds and training
ranges as the builder).

Evidence (`ADV_ABLATION_RAW.txt`, md5
`44a02c6201d2c599ad46c26a2c809132`, 3/3 runs byte-identical, exit 0, zero
stderr):
- T1: `PHASEA best=ID mismatches=20`
- T4: `PHASEA best=ADD -3;MUL -1 mismatches=17`
- T2: `PHASEA best=MUL 0;ADD 1 mismatches=20`
- T3: `PHASEA best=ADD -1 mismatches=20`
All four have best-D0 training mismatches > 0, as required.
- Actual invention events: zero. (`grep -c "INVENT op=\|REVISE old="` = 0;
  the substring hits on `NO_INVENTION_MECHANISM` are the ablation marker,
  not events.)
- `ABLLIB_SIZE 0`. Hidden accuracies via DSL only: 1001, 1004, 1001, 1001
  out of 2001 (chance-level halves, as expected for affine-only predictors
  on these targets).
- Code fact: the only operator-creating code path in the committed source
  is Phase B's reification block (lines 300-305, established under A1).
  With it removed the hypothesis space is exactly D0 (affine-only,
  machine-checked C0 2955/2955 in the builder's frozen run), on which all
  four tasks are provably unsolvable.

Consequence (per prereg): the invention capacity resides entirely in the
researcher-supplied machinery; the learner has no independent
language-expansion capacity. This locates the creation of the operator form
in researcher code, supporting the A1 downgrade under the mandatory
Criterion 0 ("the researcher must not add P"). Honest counterpoint recorded
in the prereg and repeated here: A2 alone does not kill the claim, because
nobody asserted invention without machinery; its force is as part of the
conjunction A1-A4.

## Attack A3: generality - ATTACK-SUCCEEDS

Method: `adv_generality.zag` = the FULL learner (Phase A + Phase B,
unchanged, verbatim from the committed source) applied to two new
D0-inadequate tasks on a fresh operator library:
- T5 (bump): y = 1 if -5 <= x <= 5 else -1, train x in [-20, 20].
- T6 (parity): y = 1 if x even else -1, train x in [-20, 20].
The prereg froze the D0-inadequacy proofs (affine 3-point violations) and
the proofs that no 1-threshold stump achieves total 0 on either task
(T5 needs a 2-threshold interval form; T6 needs an unbounded non-threshold
form). The world functions were sanity-checked in the run itself.

Evidence (`ADV_GENERALITY_RAW.txt`, md5
`573ff21465e4bbd9303abf16e32a9c3f`, 3/3 runs byte-identical, exit 0, zero
stderr):
- `PARITY_SANITY -1 1 1 -1` for x = -3, -2, 0, 1: correct.
- `BUMP_SANITY -1 1 1 -1` for x = -6, -5, 0, 6: correct.
- T5: `PHASEA best=MUL 0;ADD -1 mismatches=11` (> 0, D0 inadequate as
  proven); `SPLIT_SCAN n_thresh=43 best_t=-21 best_total=11`;
  `FAILURE no exact split`.
- T6: `PHASEA best=MUL 0;ADD 1 mismatches=20` (> 0); `SPLIT_SCAN
  n_thresh=43 best_t=-21 best_total=20`; `FAILURE no exact split`.
- `GENLIB_SIZE 0`. Zero invention events on either task.
(The best_t=-21 rows are the vacuous-empty-left-side scan endpoints whose
total equals the Phase-A residual; the minimum over all 43 thresholds is
still > 0, confirming the frozen proof empirically.)

Consequence (per prereg): DOWNGRADE. The "language expansion" is confined
to the researcher's anticipated 1-threshold form. Despite detected D0
inadequacy on both tasks, the learner cannot invent the needed
non-1-threshold operator form and halts with FAILURE. It invents no
unanticipated operator forms.

## Attack A4: content triviality - ATTACK-FAILS (formal criterion); substantive forced-content confirmed

Method: `adv_forced.zag`. For each frozen task T1..T4 with its training
set: (a) count thresholds t with Phase-B total 0; (b) for the winning t,
enumerate every D0 program with 0 mismatches on each side and check each
agrees with the `fit_best` choice on probe x in [-100, 100].

Evidence (`ADV_FORCED_RAW.txt`, md5
`6af029e3b756d9b397f691991931906c`, 3/3 runs byte-identical, exit 0, zero
stderr):
- Clause (a) "exactly one threshold achieves total 0": REFUTED.
  Observed `ZERO_TOTAL_THRESHOLDS n=`: T1: 2 (t = 0, 1); T4: 2 (t = 3, 4);
  T2: 1 (t = 0); T3: 2 (t = 1, 2).
- Analysis of the refutation (verified by hand against the scan): on the
  integer domain, the kink point admits two adjacent thresholds, t = k and
  t = k+1, that yield the IDENTICAL function. Example T1: t = 0 puts x = 0
  on the right (ID gives 0); t = 1 puts x = 0 on the left (MUL -1 gives
  -0 = 0). Both branches agree at the kink, so the two "different"
  thresholds compute the same function on all integers. The tie is broken
  by the researcher's fixed deterministic order (ascending scan, strict
  improvement), which keeps the smaller t. The builder's emitted thresholds
  (T1: 0, T4: 3, T2: 0, T3: 1) are exactly these researcher-tie-broken
  values.
- Clause (b) "every zero-mismatch D0 program on a winning side computes
  the same function as the chosen program": CONFIRMED on all 8 sides.
  `probe_disagreements=0` everywhere; per-side zero-fit program counts
  (nfit): T1 left 36, right 82; T4 left 20, right 53; T2 left 29, right 29;
  T3 left 26, right 69. Dozens of distinct encodings per side, all
  computing the identical function on the full probe range. Analytic
  backing (frozen in prereg): all D0 programs are affine by
  machine-checked L0; two affine functions agreeing on 2+ points are
  identical everywhere; each winning side has 17-24 training points.
- Net: the threshold VALUE carries a functionally-irrelevant 2-way
  ambiguity resolved by researcher code; the sub-program FUNCTIONS are
  unique; the trigger, the form, the tie-break, and the encoding choice are
  all deterministic. The learner exercises zero discretion at any step.

Verdict: ATTACK-FAILS against the preregistered formal criterion, because
clause (a) was refuted (2 admissible thresholds, not 1, on T1/T4/T3). Per
the preregistered verdict rule the A4 formal downgrade is WITHDRAWN. This
adversary does not retroactively rewrite the criterion to claim success.
The substantive finding - content is forced, with zero learner discretion -
is confirmed by the evidence (clause (b) 8/8, functional identity of the
tied thresholds, researcher-fixed tie-break) and is preserved below for the
parent's judgment.

## Overall verdict

- A1: ATTACK-SUCCEEDS (researcher-enumerated finite family; form supplied
  by researcher; invented operator was a complete enumerated candidate).
- A2: ATTACK-SUCCEEDS (no invention capacity without the machinery; form
  creation located in researcher code).
- A3: ATTACK-SUCCEEDS (no unanticipated operator forms; FAILURE on bump
  and parity despite D0 inadequacy).
- A4: ATTACK-FAILS on the preregistered formal clause (threshold-value
  uniqueness refuted: 2 functionally-identical admissible thresholds on
  T1/T4/T3); substantive forced-content confirmed (8/8 sides, 0 probe
  disagreements; tie broken by researcher order).

The 4/4 SUCCEEDS condition for killing the L3/Criterion-0 interpretation
was not met. The interpretation is therefore DOWNGRADED, not formally
killed, under the preregistered rule. That said, A1 establishes the core
point on its own: the "invented" operator is the argmin of a finite
researcher-enumerated menu of 375,477,075 complete (threshold, leftProg,
rightProg) triples per task, in a researcher-fixed operator form. Under the
mandatory Criterion 0 ("the researcher must not add P; searching a finite
authored menu does not count"), the L3 representational-invention reading
of H-PROCLANG1 does not survive. A2 and A3 corroborate: the form-creation
lives entirely in the machinery, and the machinery cannot go beyond its
anticipated 1-threshold shape.

## Recommendation

1. H-PROCLANG1 keeps its BUILD-PASS engineering standing (9/9 bars,
   independently reproduced); that verdict is not contested and is not
   affected by this report.
2. Its interpretation is DOWNGRADED to bounded L2+ structural search with
   reification machinery. It is not a Criterion-0 representational
   invention: the researcher supplied the COND form, the finite stump
   family, the scan, and the tie-breaking order; the data determined
   parameter values that were functionally unique.
3. Do NOT advance H-PROCLANG1 toward SURVIVES on a
   representational-invention reading. The pipeline steps already completed
   (prereg, implementation, sealed evaluation, reproduction, this
   alternative-explanation attack) stand as documented; the remaining steps
   should not be spent promoting this mechanism as L3.
4. A follow-up (e.g. H-PROCLANG2) may re-enter the frontier pipeline only
   if the learner supplies an operator form OUTSIDE any
   researcher-enumerated finite family, with content underdetermined by
   (data + researcher tie-breaks), i.e. a case where the learner's choice
   among genuinely distinct forms is visible in the trace.

## Determinism and provenance

| Program | Runs | Result | md5 of raw |
|---|---|---|---|
| adv_ablation.zag | 3/3 byte-identical (cmp), exit 0, zero stderr | 3/3 | 44a02c6201d2c599ad46c26a2c809132 |
| adv_generality.zag | 3/3 byte-identical (cmp), exit 0, zero stderr | 3/3 | 573ff21465e4bbd9303abf16e32a9c3f |
| adv_forced.zag | 3/3 byte-identical (cmp), exit 0, zero stderr | 3/3 | 6af029e3b756d9b397f691991931906c |

D0 machinery in all three programs is verbatim `sed` extraction from the
committed builder source at `647b4096c` (lines 1-215 for ablation/forced;
lines 1-202 plus 218-341 for generality); only the attack mains and the
two new world functions (`w_bump`, `w_parity`) are adversary-authored.
Toolchain `znc 2026.07.0-dev (edition 2026)`. No Python used anywhere.

## Files committed (owned path only)

- `docs/lab/research-lead/overnight-20260928/proclang_adversary/PREREG_PROCLANG_ADV.md`
  (frozen prereg, committed before implementation)
- `docs/lab/research-lead/overnight-20260928/proclang_adversary/adv_ablation.zag`
- `docs/lab/research-lead/overnight-20260928/proclang_adversary/adv_generality.zag`
- `docs/lab/research-lead/overnight-20260928/proclang_adversary/adv_forced.zag`
- `docs/lab/research-lead/overnight-20260928/proclang_adversary/ADV_ABLATION_RAW.txt`
- `docs/lab/research-lead/overnight-20260928/proclang_adversary/ADV_GENERALITY_RAW.txt`
- `docs/lab/research-lead/overnight-20260928/proclang_adversary/ADV_FORCED_RAW.txt`
- `docs/lab/research-lead/overnight-20260928/proclang_adversary/PROCLANG_ADV_RESULT.md`
  (this report)

## Open question for the parent (not decided here)

A4's formal clause failed while its substantive point held. If the parent
wants a strict re-test of content-triviality under a corrected formal
criterion (e.g. "the invented FUNCTION is unique up to researcher
tie-breaks"), that is a new preregistered experiment, not a reinterpretation
of this one.
