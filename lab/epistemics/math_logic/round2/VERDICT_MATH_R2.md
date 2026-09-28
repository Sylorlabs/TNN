# VERDICT: MATH R2 Head-to-Head Evaluation (2026-09-25)

## Decision
**The round-1 DUAL verdict STANDS.** No new engine wins >=2 of the 3 primary bars
(PB1/PB2/PB3) against BOTH ONE-R1 and DUAL-R1. All four testable new engines
fail to displace the round-1 champion.

## Primary Bars

| Engine | PB1 (KB1X >=7/10) | PB2 (KB2 pass) | PB3 (B5X <=18 incorr) | Bars won |
|--------|-------------------|----------------|----------------------|----------|
| HYB | 0 wins (FAIL) | PASS | 60 incorr (FAIL) | 1/3 |
| REF-FIRST | 0 wins (FAIL) | PASS | 24 incorr (FAIL) | 1/3 |
| NFEE | 0 wins (FAIL) | FAIL | 60 incorr (FAIL) | 0/3 |
| LEARN-FORM | 0 wins (FAIL) | PASS | 36 incorr (FAIL) | 1/3 |

**PB1:** B3R interleaved pairwise. All engines 10/10 (except NFEE 9/10). Zero
pairwise wins for any new engine vs either parent. The interleaved-revision
interface is not the differentiator; all engines handle B3R.

**PB2:** KB2 contrast (20 pairs). HYB, REF-FIRST, LEARN-FORM pass both sub-bars.
NFEE fails the ONE-bar (conf 0 on solvable B3_03; B3 coverage gap).

**PB3:** B5X incorrect <= half of worse parent (ONE: 36 incorr; half = 18).
HYB 60, REF-FIRST 24, NFEE 60, LEARN-FORM 36. None <= 18. All fail.

## Hypotheses

**H1 (HYB long-chain): FAIL.** B3R pairwise wins 0 vs both parents (need >=5).
HYB matches parents on B3R (10/10) but does not exceed. B6X: HYB 2/3 (misses
B6X_03 120-chain despite design goal).

**H2 (REF-FIRST contradiction-blind): NOT FALSIFIED.** B5X false_withheld:
REF-FIRST 0, DUAL 0. REF-FIRST does not withhold more than DUAL; it over-derives
like DUAL (24 false_derived each). The contradiction-first strategy does not
induce blindness, but it also does not improve over DUAL.

**H3 (NFEE no-free-elimination): FAIL.** B6X: NFEE 2/3 with B6X_03 UNSUPPORTED
(bar required deriving B6X_03). NFEE also collapses on B5X (0/60).

**H4 (LEARN-FORM learned formalizer): FAIL.** B7F: LEARN-FORM 2.5/100 vs 70 bar
and 47.9 curated baseline. The 1-template learner abstains on 12/20 and scores
0-17 on the rest. B1N: 9 DERIVED all via unfaithful P01-template; falsely
derives open P05.

**H5 (QUOT quota-bounded): BLOCKED-WITH-EVIDENCE.** Repair not received; local
partial panics on B2_01. Excluded from decision.

## Battery Summary (solved/total, incorrect)

| Battery | ONE-R1 | DUAL-R1 | HYB | REF-FIRST | NFEE | LEARN-FORM |
|---------|--------|---------|-----|-----------|------|------------|
| B2R (12) | 12/12, 0 | 12/12, 0 | 12/12, 0 | 12/12, 0 | 12/12, 0 | 12/12, 0 |
| B3R (10) | 10/10, 0 | 10/10, 0 | 10/10, 0 | 10/10, 0 | 9/10, 1 | 10/10, 0 |
| B4R (15) | 15/15, 0 | 15/15, 0 | 15/15, 0 | 12/15, 3 | 15/15, 0 | 15/15, 0 |
| B4X (15) | 10/15, 5 | 10/15, 5 | 10/15, 5 | 6/15, 9 | 10/15, 5 | 10/15, 5 |
| B5X (60) | 24/60, 36 | 36/60, 24 | 0/60, 60 | 36/60, 24 | 0/60, 60 | 24/60, 36 |
| B6X (3) | 3/3, 0 | 3/3, 0 | 2/3, 1 | 3/3, 0 | 2/3, 1 | 3/3, 0 |

All incorrect are false_withheld except: DUAL/REF-FIRST B5X (24 false_derived each).
Zero divergence across 3x byte-identical reruns. Zero RNG (grep verified).
Sealed guard exits 3 on all 9 binaries.

## KB4 Audit Coherence
**PENDING GRADER DISPATCH.** Packet of 356 blinded audits (aliases A-F) is
committed (`kb4_packet.json`). Three independent grader subagents must be
spawned by the parent (coordinator is depth 2/2, cannot spawn). Requires
inter-rater alpha > 0.8 or the bar is void (round failure per prereg).
If ONE's mean rating is >=1.0 below DUAL's, DUAL is falsified as audit-hostile.

Alias key: A=DUAL-R1, B=NFEE, C=ONE-R1, D=REF-FIRST, E=LEARN-FORM, F=HYB.
(Key in `kb4_key.json`; do not share with graders.)

## Key Findings

1. **B5X exposes a sharp divide.** 36 derivable / 24 withhold. DUAL and REF-FIRST
   derive everything (36 right, 24 false_derived). ONE and LEARN-FORM withhold
   everything (24 right, 36 false_withheld). HYB refutes everything (0/60).
   NFEE withholds derivable + refutes withholdable (0/60). No engine gets both
   right. The "derivability vs withholdability" discrimination remains unsolved.

2. **HYB's long-chain goal unmet.** Misses B6X_03 (120-chain) and collapses on
   B5X (refutes everything). The hybrid assembly does not deliver.

3. **REF-FIRST matches DUAL but doesn't beat it.** Same B5X pattern (36/60),
   worse on B4X (6/15 vs 10/15) and B4R (12/15 vs 15/15). The referee overhead
   costs coverage without gaining precision.

4. **LEARN-FORM's template is unfaithful.** The P01-derived template fires on
   9 B1N problems, producing identical `imp(p,q),p|-q` formalizations for
   distinct mathematical statements, including a false derivation of open P05.
   This is pattern-matching, not learning.

5. **Sealed-key defects (F-SEAL-01, F-SEAL-02).** B2_07 marked DERIVED but
   underivable; B7F README stale. Corrected/scored from actual fixtures.

## Answer to the Prereg Question
**Was the engine space the limiting factor, or does the formalization bottleneck dominate?**

Both, but the formalization bottleneck dominates. The engines (ONE/DUAL/HYB/
REF-FIRST/NFEE) all solve the formal batteries similarly (B2R/B3R/B4R near-perfect;
B4X 10/15 except REF-FIRST). The differentiator is B5X (withhold vs derive
discrimination), where no engine succeeds. LEARN-FORM's failure on B7F/B1N shows
that NL→formal is the hard problem: a 1-template learner cannot formalize, and
even the curated baseline only reaches 47.9. The engine space (inference) is
mature; the formalization bottleneck (NL understanding) is where progress is needed.
