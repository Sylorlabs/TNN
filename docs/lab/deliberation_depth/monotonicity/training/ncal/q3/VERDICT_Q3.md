# VERDICT — NEC v3 Q3 Follow-up: B13 Scale Degradation (adopted m11)

Date: 2026-09-25 UTC. Frozen amendment §3 target: `B13_s100 ≤ B13_s10 ≤ B13_s1`,
B3 ≤ 3, B2=0, no broken passing bar, Q2 gaming probes passed.

## Baseline (corrected)

| Scale | B13 |
|-------|-----|
| s1 | 6 |
| s10 | 23 |
| s100 | **24** (was misreported as 23; extra: ceiling/D d2, G=-0.1106) |

## Diagnosis

- **D1 (pooled-ledger/prior washout): CONFIRMED.** Family-blind class bins converge
  to adversarially pooled empirical rates (cls 15: 0.7756, cls 5: 0.5152, etc.).
  Honest-first cold ledger starts high; warm ledger washes out; per-item ceiling
  locks the washed value for d2+.
- **D2 (fixture composition shift): NOT CONFIRMED.** s10/s100 are exact sequential
  replications; composition identical per pass.
- **D3 (personal-cap ablation): CONFIRMED.** Cap contributes +2 violations at
  s10/s100 (redteam d2/d4). Without it K12 stays at ≈0.996. Cap is load-bearing;
  retained.

## FIX-* head-to-head (3× byte-identical, post-addendum)

| Candidate | s1 | s10 | s100 | B3 | B2 | Meets target |
|-----------|----|-----|------|----|----|--------------|
| FIX-A (anchors to 0.95) | 0 | 0 | 0 | 2 | 0 | **YES** |
| FIX-B (1:1 honest) | 5 | 11 | 12 | 2 | 0 | NO (B13) |
| FIX-C (matched traps) | 5 | 18 | 18 | 2 | 0 | NO (B13) |
| FIX-D (thin wrongs) | 0 | 0 | 0 | 6/5 | 0 | NO (B3>3) |
| m12 (shrinkage prior) | 3 | 11 | 11 | 2 | 0 | NO (B13, predicted) |

Gaming probes for FIX-A: GP-1 PASS (0.0185 ≤ 0.10), GP-2 PASS (0.0917 ≤ 0.50),
GP-3 PASS (K12 d2+ = 0.000).

## Decision

**FIXTURE.** D1 and D3 confirmed, D2 not confirmed, and FIX-A meets the full
target (B13 0≤0≤0, B2=0, B3=2≤3, no broken bar, gaming probes passed).

NOT PRIOR-WASHOUT: the principled scale-invariant prior (m12, (emp+p0)/2)
misses (3/11/TBD), confirming the addendum's prediction that convex shrinkage
cannot repair the washed classes.

NOT MECHANISM: no mechanism change was needed; the ledger and cap are sound.
The defect is in the training curriculum (fixture), not the mechanism.

## Adoption eligibility (§5)

FIX-A is NOT yet adoption-eligible:
1. Fixture generator is Python (`fixbuild.py`); "Pure Zag final mechanisms/
   fixtures" requires a pure-Zag port.
2. White-box audit (§2 T1–T4) not yet performed.
3. Amendment §5 also requires the nonincreasing B13 property to hold under the
   adopted fixture — met (0≤0≤0) — but the pure-Zag port must re-prove it.

## Caveats

- Protocol ordering: exploratory diagnosis preceded the pre-run addendum
  (disclosed in RUNLOG_Q3.md). All FIX runs are post-addendum.
- FIX-D's B13=0 is disqualified by B3=6/5; thinning wrongs is not viable.
- s100 baseline corrected 23→24; all "improvement" deltas use 24.
