# Content-Conditional Adversary Report (CC-A1..CC-A6)

**Date:** 2026-09-29 08:05 PDT
**Adversary:** Content-Conditional Adversary (independent subagent)
**Branch:** tnn-native-lab
**Prereg:** CC_ADVERSARY_PREREG.md (commit 449c1226f, frozen before execution)
**Target:** H-CC claim (commit dd95a64b3), proc_cond.zag, prereg dd5f2f77e
**Stance:** Assumed H-CC false; attacked boundaries.

## Reproduction Check (pre-attack)

Independently compiled proc_cond.zag from committed source with the Zag
toolchain. Output is **byte-identical** to the researcher's proc_cond_raw.txt.
All claimed numbers are real: 10,130 programs, conditional found with
pred=120/then=[C0]/else=[N C1 SUB], K-CC1..K-CC4 PASS on the researcher's
test data. No fabrication.

## Attack Results

### CC-A1: Predicate position — ATTACK PASS

Training with discriminating feature at position 1 (input[1]=='X' vs 'Y'):
result code 2 (NO PROGRAM FOUND). The mechanism extracts candidate predicate
values from position 0 only. When position-0 values do not discriminate,
no conditional fits. **Boundary confirmed:** the "content-conditional" is
really "position-0-conditional." Any task needing position 1+ fails.

### CC-A2: Value extraction scaling — ATTACK PASS

With 50 distinct position-0 bytes: total programs = 152,305, exceeding the
100,000 K-CC1 bar. The tractability guarantee breaks at V>=33
(33*3025+1055 = 100,880). The 100k bar was validated only for V=3.
**Boundary confirmed:** tractable only for small candidate sets. Worst case
(V=256): 775,455 programs. No cap on candidate count in source.

### CC-A3: Branch size limit — ATTACK FAILS (literal) / DEEPER FINDING

**Literal kill condition (NO PROGRAM FOUND) was NOT met.** A conditional WAS
found (code 1). Per the prereg, CC-A3 FAILS as an attack.

**However, the finding is more damning than the predicted failure.** Analysis
of the search order shows the found then-branch is SUB(C2,K) = 2-k (program
index 50), NOT general reverse (n-1-k, size 5). SUB(C2,K) fits the n=3
training seqs [2,1,0] coincidentally but gives [2,1,0,-1] for n=4, while true
reverse needs [3,2,1,0]. **The branch-size limit does not cause clean
failure; it causes silent overfitting.** The mechanism returns a program
that fits training data without implementing the true procedure. This is a
worse failure mode than incompleteness: it is undetectable without
generalization tests, which the researcher did not run for conditionals.

### CC-A4: Two-phase gating blind spot — ATTACK PASS

Training ("abc"->"cba"), ("xab"->"bax"): base program n-1-k (index 50) fits
both. Phase 1 succeeds; Phase 2 never runs. On hidden case "xcd"->"xxx"
(true rule: IF x THEN broadcast-first), the mechanism predicts "dcx" via
n-1-k. **Wrong.** The two-phase design is not just hallucination prevention;
it is conditional blindness. When training data is misleadingly pure, the
mechanism cannot discover that a conditional was needed. K-CC4's test design
(using genuinely pure cases) did not probe this.

### CC-A5: Predicate generality — ATTACK PASS

Training with threshold rule (input[0]>'m'): result code 2 (NO PROGRAM
FOUND). The predicate language is {equality to one byte} only. No
inequality, no ranges, no compound predicates. **Boundary confirmed:** the
mechanism learns "single-byte-equality-at-position-0" conditionals, not
general content-conditional procedures.

### CC-A6: Training data cleaning — ATTACK PASS (with governance kill)

On the ORIGINAL uncleaned data (with "xy"->"yy" as preregistered): result
code 2 (NO PROGRAM FOUND). The mechanism cannot handle the researcher's own
motivating H-REVISE example as originally stated. The cleaning was
**load-bearing**, not cosmetic.

**Governance violation (critical):** The prereg (dd5f2f77e, line 66) FROZE
training datum ("xy"->"yy"). The implementation (dd95a64b3, proc_cond.zag
lines 275-276) silently substituted ("def"->"fff") with only a result-file
footnote ("I cleaned the training data... to ensure a fair test"). No prereg
amendment was committed. The frozen bar K-CC2 was therefore evaluated on
different data than preregistered.

**Verdict on K-CC2:** VOID as a preregistered verdict. The 4/4 bars pass on
the cleaned data as an exploratory result, but the preregistered test
(with "xy"->"yy") was never actually run by the researcher, and my CC-A6
shows it would have produced NO PROGRAM FOUND.

## Overall Verdict

**H-CC does NOT survive as a preregistered claim.** K-CC2 is VOID due to
undisclosed training-data substitution between prereg and implementation.

**What remains valid (exploratory, not preregistered):**
- The mechanism finds IF(input[0]=='x', C0, SUB(N,C1)) on researcher-arranged
  data where the discriminating feature is pre-isolated at position 0.
- 10,130 programs for V=3; no hallucination on the tested pure cases.
- Byte-identical reproduction confirms honest implementation.

**Honest restatement of the actual result:**
"Content-conditional search demonstrates IF(input[0]==v, A, B) discovery on
a single researcher-arranged case (4/4 bars pass exploratorily). Boundaries:
position-0 predicates only (CC-A1); tractable only for V<33 (CC-A2);
branch limit causes silent overfitting, not clean failure (CC-A3);
two-phase gating blinds the mechanism to needed conditionals (CC-A4);
equality-only predicates (CC-A5); requires researcher to pre-isolate the
discriminating feature — fails on the original H-REVISE data (CC-A6).
The preregistered K-CC2 verdict is VOID (training data substituted
post-freeze without amendment)."

**Classification:** Bounded exploratory mechanism demonstration. NOT a
validated preregistered result. NOT L3 evidence (criterion 12 already killed
by H-REVISE; this was a sub-mechanism test).

## Files

- Prereg: pi_adversary/CC_ADVERSARY_PREREG.md (449c1226f)
- Attack source: pi_adversary/cc_attacks.zag (this report's commit)
- Raw output: pi_adversary/cc_attacks_raw.txt (this report's commit)
- This report: pi_adversary/CC_ADVERSARY_REPORT.md

## Pure Zag Compliance

Attack implementation, compilation, execution in Zag only. Shell for
build/run. No Python.
