# OpScope Design Revision: K 3 to 2 (REV-DESIGN)

Design-only document. No implementation performed. No empirical claims
made. This document revises one frozen constant of the operator/scope
design in response to OPSCOPE-FAIL.

## 1. Ancestry

- Design: commit `71f98aa72`
  (`operator_scope/OP_SCOPE_DESIGN.md`, DESIGN-COMPLETE). The original
  design text is immutable history; it is not edited by this revision.
- Prereg: commit `37300ceae` (`operator_scope_impl/PREREG_OPSCOPE.md`).
- Amendment 1: commit `6828c7228` (strict-majority binarization,
  `cnt*2>o`, plus learner threshold fix; committed before the
  canonical re-run).
- Result: commit `f01c6b69d` (`operator_scope_impl/OPSCOPE_RESULT.md`).
  Verdict OPSCOPE-FAIL: F1 FAIL (0/3, no OPREC installed), F2 FAIL
  (0/3), F3 PASS (0/0/0 audit hits), F4 FAIL (no operator to ablate),
  F5 PASS (17/20, SIZE 3/3). Kill bars K1/K2 PASS; K3 PASS with one
  disclosed procedural incident.

## 2. Diagnosis: K=3 is unsatisfiable on the frozen battery

At seen=100 the retry's candidate table reads (w=unit id;
epc/rec/sup/mtch/div/cs/cb/gate):

- w=1 ("not"): epc=16 reclen=1 sup=16 mtch=16 div=2 cs=100 cb=84
  gate=1
- w=0 ("tak"): epc=100 reclen=1 sup=52 mtch=48 div=9 cs=0 cb=84
  gate=0

The true trigger passes eligibility (e1, e2), support (16>=4),
consistency (16/16>=0.75), and the zero-parameter gate (100>84,
strict). It fails ONLY the K=3 scope-diversity bar.

The cap is structural, not data sparsity. The frozen training
battery (episodes 0..99) negates exactly two distinct forms.
`devang4.zag`: phase1 "NEG x12: (0)x6, (1)x6" (line 699) and phase2
"NEG old x4: (0)x2,(1)x2" (line 792) build utterances via
`build_utt(ep,0,1,color_wid(ci),0,3)` with ci in {0,1}: "tak not red"
x8 and "tak not blu" x8. No training NEG episode negates any other
form. The test-phase "NEG novel" block (line 861, "tak not grn" x3)
holds the frozen T1/T3 items and is not visible to discovery.

Therefore the maximum scope diversity any learner can ever observe
for the true trigger on this battery is div=2, by generator
construction, for every seed and every run. K=3 is unsatisfiable for
any learner. This is a design-parameter bug, not a machinery bug:
the design set K=3 imagining varied negated nouns, but the frozen
battery supplies two. The R1/R3 machinery is sound (baseline UNION
reaches 17/20, beating DEVANG4's 16/20; the NEG residual is exactly
the DELETION footprint).

Per the retry's diagnosis and the mandate for this task, the fix is
a design revision of K, not a builder-side patch. The builder was
correct not to weaken K=3 unilaterally.

## 3. The revision: K 3 -> 2

Revised frozen constants (all others unchanged; the binarization
rule is the strict-majority form from Amendment 1, inherited):

| Constant      | Revised | Meaning                               |
|---------------|---------|---------------------------------------|
| B0 burn-in    | 20      | episodes before first discovery check |
| E interval    | 10      | discovery/retirement check cadence    |
| N_ep recur    | 5       | min episodes containing W             |
| Fmax elig     | 1       | max features in record(W, DEFAULT)    |
| N support     | 4       | min residual events for W             |
| C consistency | 0.75    | min signature-match fraction          |
| K diversity   | 2       | min distinct scope unit forms         |
| OPMAX         | 8       | operator table cap                    |

The only change from the preregistered table is K: 3 -> 2.

## 4. Why K=2 is principled, not bar-weakening

(a) Maximum satisfiable value. On the frozen battery, div for the
true trigger is capped at 2 by construction (section 2). Every K>=3
is unsatisfiable; K=2 is the largest K the battery can support. The
revision sets K to the battery's structural maximum, not to the
observed value.

(b) The bar's purpose is preserved. The design states the diversity
bar "bars phrase memorization: the footprint must recur across
varied scope content, the opposite of pair-statistic learning."
Under K=2, a candidate whose footprint appears under a single scope
form (div=1) still fails. Single-form memorization remains barred;
the bar now requires the footprint to recur across both observed
negated forms. K=1 would admit single-pair memorization and would
defeat the bar's purpose; K=2 does not.

(c) Confounds are killed by the other bars, not by K. The
positional confound w=0 reaches div=9 but is killed by the
zero-parameter gate (cs=0, never strictly better than baseline);
no K admits it. Content words ("red", "blu", "grn") are killed by
eligibility (e2): their DEFAULT records exceed Fmax=1. The
empirical candidate table shows the true trigger is the only
candidate for which K is the binding constraint, so lowering K to
the structural maximum admits no spurious candidate the other bars
do not already reject.

(d) The revision unblocks the falsifier chain without prejudging
it. Under K=2 the true trigger passes all bars (sup=16>=4,
16/16>=0.75, div=2>=2, 100>84 strict), so the OPREC installs and
F1, F2, F4 become evaluable. F1-F5 still judge the machinery;
a PASS is not entailed. If F1 then fails with an installed
operator, the design's existing sparsity branch applies.

## 5. Falsifier-interaction extension (new frozen branch)

Added to the design's section 5 procedure, frozen by this revision:

- If F1 fails with no OPREC installed and F3 passes, run the
  K-satisfiability diagnosis before any other next step:
  1. From the frozen generator source (not from learner behavior),
     compute the maximum scope diversity achievable for the true
     trigger form on the frozen training battery.
  2. If that structural maximum is below K, the failure is a
     design-parameter bug. Revise K to the structural maximum in a
     committed design revision. Do not patch the builder, do not
     weaken other bars, do not touch the frozen battery.
  3. If the structural maximum meets or exceeds K, the failure is
     machinery-side; the sparsity branch and representation review
     apply as before.

This branch is what section 2 executes: structural maximum 2 < 3,
hence this revision.

## 6. Corrected walkthrough note

The original design's section 4.4 walkthrough illustrates
discovery "across varied scopes ('not red', 'not box', ...)".
The frozen battery's training NEG variety is ("not red",
"not blu") only. Under revised K=2 the walkthrough's claim that
"the support, consistency, and diversity bars are met" holds;
under K=3 it does not. This note corrects the illustration; the
original text stands as committed history.

## 7. Considered alternative: extend the battery, keep K=3

Keep K=3 and add a third negated form to training (e.g., negate a
third color in phase1/phase2 NEG blocks). This preserves the
original strictness but unfreezes the battery: it requires
regenerating episodes, re-verifying all 20 frozen test items and
the T1/T3/SIZE ids, re-certifying the oracle unit mapping and 3/3
determinism, and re-baselining every measurement that depends on
the episode order. The gain is 3-form versus 2-form training
diversity, which does not change what the falsifiers test: the
operator's functional generalization is tested by F2 on the novel
negated word "grn", not by the training diversity count.
Deferred. The parent may authorize it as a separate battery
revision if 3-form training diversity is later judged
load-bearing. It is not part of this revision.

## 8. Builder handoff

The next builder preregisters against THIS revision (not against
the original design's K=3):

- Adopt the revised constants table in section 3 (K=2).
- Reuse the frozen battery, the frozen T1/T3/SIZE item ids, the
  F3 audit file paths, and the oracle unit-sequence interface
  unchanged.
- Inherit Amendment 1's strict-majority binarization (`cnt*2>o`).
- Expected mechanism outcome: OPREC installs for w=1 with
  signature DELETION, created_at > 0, support >= N; F1, F2, F4
  become evaluable.
- Verdict remains BUILD-PASS or BUILD-FAIL per R4 only; only the
  complete 11-step pipeline can yield SURVIVES. No L3 claim.
- Do not weaken K=2 or any other bar after seeing results.

## 9. Honest scope

Unchanged from the original design: researcher-authored machinery
(discovery criterion, UNION combiner, OPREC structure, signature
family, routing, all constants); the learner creates the operator
inventory, the records, and the routing bindings. Bounded L2
direction, not L3. This revision changes one constant and adds one
review branch; it creates no new machinery and no new claim.

## 10. Kill bar checklist (this design task)

- K1 PASS: K revised (3 -> 2) with rationale, structural evidence,
  the full revised constants table, the falsifier-interaction
  extension, and the builder handoff.
- K2 PASS: K=2 is satisfiable. Structural maximum div=2
  demonstrated from the frozen generator source (devang4.zag NEG
  blocks, lines 699 and 792; training episodes 0..99) and
  corroborated by the retry's empirical candidate table (w=1
  div=2). Confound analysis (section 4c) shows no spurious
  candidate is admitted by the revision.
- K3 PASS: design only. No implementation, no code, no runs, no
  Python at any stage.
