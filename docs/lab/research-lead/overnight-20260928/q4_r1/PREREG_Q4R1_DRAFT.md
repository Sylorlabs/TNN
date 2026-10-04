# R1 Preregistration (DRAFT): Multi-seed robustness on F-PARCOND

Date: 2026-09-30. Worker: Q4-R1 Prereg Drafter.
Status: DRAFT. Not frozen. No implementation. No runs.

This is the R1 prereg draft per revival plan 290f0d061 section 1.5.

## 1. Question

Does the beam reach true 64/64 on fresh seeds when the evidence covers
all 8 combos, defeating the underdetermination reading of the Q4
discovery result (attack 73d9637a2)?

## 2. Frozen mechanism (no change permitted)

Target: F-PARCOND, D = IF X1 THEN (X2 XOR X3) ELSE (X2 AND X3), 6
operators. Sealed family 5 of q4_parcond.zag, commit 5f56cc491 as
corrected by cffc56e5b.

Learner: the frozen Q4 Phase-1 discovery machinery, byte-for-byte the
attack Phase-1 build (altexp.zag build_learner32 / phase1_rand, commit
73d9637a2), which copied the Phase-1 machinery verbatim from
q4_parcond.zag. The IV-selection arm is the P-RAND arm (select_iv_rand).

Beam configuration (frozen): width 32 (top 32 by score desc, opc asc,
node asc); simplicity tax 200 per operator (a2 = 200*opc); keep bars:
accuracy >= best-observable accuracy + 0.15 margin on evidence, and
operator count <= 7; growth trace recorded.

Passive-sample protocol (verbatim passive()): 8 samples. Samples 1..6
retry up to 1000 draws until bit5 == y (the X6-confound bias). Samples
7..8 are free draws. Then 24 rounds of (beam_extend; policy select;
do_iv), then a final beam_extend and scoring on the full 32-sample
evidence set.

Purity requirement: the build must be pure Zag end to end, with the
source SHA recorded before any run. The prior Phase-1 result was not
governance-clean (byte checks used Python). Any R1 run must use a
clean pure-Zag rebuild with recorded source hash; the previous
binary is not admissible evidence.

## 3. Policy (named after R4)

R4 completed at 8b0ede871: R4-FAIL, F-R4 fired, P-DIS honestly retired
(SUM_DIS=92, SUM_RAND=95, mean margin -0.25, below the +0.75 dual bar).
Per revival plan section 4.4 (F-R4) and section 6 (Phase B), R1 runs
with the surviving policy:

POLICY = P-RAND (attack fn select_iv_rand): count the unused x in
0..63; select index rng_range(st, cnt) over the ascending unused list,
with rng_range the seeded LCG (s = s*1103515245 + 12345 mod 2^31).
Deterministic given the seed. No mechanism change permitted.

## 4. Seeds (frozen)

5 fresh seeds, pairwise distinct, disjoint from:
- tainted exploratory seeds {11, 22, 33, 44, 55}
- R4 seeds {61977, 62954, 63931, 64908, 65885, 66862, 67839, 68816, 69793, 70770, 71747, 72724}
- all other committed seed sets {123456789, 555555555, 770404483}

S1=81113, S2=82090, S3=83067, S4=84044, S5=85021
(S_i = 80000 + i*977 for i=1..5.)

## 5. Bar (frozen)

R1-PASS: on at least 4 of the 5 seeds, BOTH:
(a) the P-RAND policy achieves 8/8 combo coverage (distinct (x & 7)
    among the 32 observations: 8 passive + 24 IVs), AND
(b) the beam's kept expression reaches true 64/64 accuracy on the
    full 64-row truth table of D.

Rationale: with 8/8 coverage the evidence uniquely determines D
(ENUM result TIES=1, TRUEUNIQUE=1 from 73d9637a2), so a 64/64 is
attributable to evidence plus search rather than to a tie broken by
the 200/opc tax plus single-seed luck.

## 6. Falsifier (frozen)

F-R1: fewer than 4 seeds satisfy (a) and (b) jointly. R1 FAILS.

## 7. Mandatory diagnostics (per seed, non-governing but must be reported)

Tax-off diagnostic: rank the beam's finalists by accuracy alone,
ignoring the 200/opc tax, and report whether the top-ranked is
unique. Under 8/8 coverage this must be unique; a tie indicates a
harness or beam defect and invalidates the seed.

Reported per seed: combo coverage (/8), evidence fit of kept
expression (/32), true accuracy (/64), operator count, tax-off
uniqueness flag.

## 8. Failure localization (preregistered interpretation)

- Coverage shortfall implicates the policy (P-RAND failed to reach
  8/8 in 24 rounds).
- Evidence-fit shortfall at 8/8 coverage implicates the beam (the
  SEED=55 mode: 23/32 fit at 8/8 coverage).
- Accuracy shortfall at full coverage and full evidence fit
  implicates generalization (the kept expression matches evidence
  but not the true D).

If the policies tie on coverage but kept accuracy differs, that is a
beam effect, not a policy effect.

## 9. Determinism and purity (frozen)

- 3/3 byte-identical runs per seed (identical md5, zero stderr).
- Fixed seeds only; seed list in section 4 is the only randomness source.
- Pure Zag at every stage: implementation, build, execution,
  verification, analysis. Zero Python invocations anywhere,
  including scratch, debugging, and byte checks.

## 10. Governance

- This draft's first commit strictly precedes any R1 freeze commit,
  and the freeze commit strictly precedes any R1 run.
- R1 is UNBLOCKED: R4 completed at 8b0ede871 before this draft, so
  the section-6 sequencing precondition is satisfied in ancestry.
  The freeze names P-RAND explicitly (section 3).
- Revival remains CONJUNCTIVE per 290f0d061 section 0. R4 FAILED,
  so a full Q4 revival is already impossible regardless of R1's
  outcome. R1 still tests multi-seed robustness of the surviving
  passive-plus-random mechanism, localizes the discovery weakness,
  and becomes the defined next target if it fails. R1-PASS does NOT
  revive Q4 and does NOT touch L3 or Criterion 0.
- Owned path: docs/lab/research-lead/overnight-20260928/q4_r1/ only.
- No em dashes. No Python.

## 11. Draft kill bars

- K1: Draft complete. This document exists and names the target,
  mechanism, policy, seeds, budget, bars, falsifier, diagnostics,
  determinism standard, and purity clause.
- K2: Seeds specified. Section 4 fixes S1..S5, verified disjoint
  from R4 seeds, tainted seeds, and all committed seed sets.
- K3: No implementation. This commit contains only this prereg
  document. No binary, no .zag source, no raw outputs, no results.
