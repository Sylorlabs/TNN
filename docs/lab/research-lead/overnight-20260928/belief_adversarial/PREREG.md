# PREREG: Adversarial Belief Formation (Priority H)

Frozen before implementation. Any breakage requires fresh prereg, fresh
worlds, and rerun. VOID is terminal.

## Question

The 3-phase belief formation passed. Now stress it with adversarial
evidence. Beliefs must remain rational relative to the evidence available
at each moment, never scored against omniscience.

## Mechanism (extends belief.zag, unfrozen only)

Same learner-owned machinery: evidence records persist, source
reliability learned from verification outcomes only (neutral 1000 until
2 verifications), same-source repetition discount (halving per phase),
bands U=wmax and T=2U, statuses NONE/PROVISIONAL/UNCERTAIN/CONFIDENT.

New: suspected-copy discount. The learner keeps a ring of the last 2
observation events (src, hyp, strength). If a new report matches another
source's (hyp, strength) exactly within that window, it is treated as a
suspected copy and its contribution is quartered (cd=250 per-mille).
Genuinely independent observations vary in strength and timing, so the
heuristic does not fire on them. The heuristic form (window 2, quarter)
is researcher scaffold; every application is learner-side on observable
data. No source is ever labeled copier by the researcher.

Contribution: w * rel * disc * cd / 1000000 (milli-units).

## Scenarios (each in a fresh learner state)

### A. Conflicting credible evidence
Sb calibrated 2/2 correct (rel 1000). Sc calibrated 2/2 correct (rel 1000).
Sb reports H1 strong. Sc reports H2 strong.
Expected: UNCERTAIN. Two equally credible sources disagree at equal
strength. Uncertainty is the only rational response.

### B. Deceptive source
Sd calibrated 2/2 correct (rel 1000). Sd reports H1 strong (phase 1).
World verifies truth H2: Sd wrong, rel 666. Sd reports H1 strong
(phase 2). World verifies truth H2: Sd wrong, rel 500.
Expected: rel(Sd) == 500 after 2 verified lies. A third Sd strong claim
contributes exactly 1500 (vs 3000 baseline). The learner detects the
liar from verification outcomes and discounts future claims. Past
contributions are not retroactively erased (honest limitation, noted).

### C. Independent vs copied
Copied trio (fresh state): Se H1 strong, Sf H1 strong, Sg H1 strong,
back-to-back. Expected: PROVISIONAL H1 (s1=4500 < T=6000). The learner
must not become CONFIDENT on parroted reports.
Independent trio (fresh state): Sh H1 strong, Si H1 moderate, Sj H1
strong. Strengths vary, so no copy discount fires. Expected: CONFIDENT
H1 (s1=8000 >= T=6000). Genuine consensus earns confidence.

### D. Belief reversion
Setup: Sm H2 strong, Sn H2 moderate, So H2 weak. s2=6000, CONFIDENT H2.
D1: St H1 strong. s1=3000. Expected: UNCERTAIN (margin 3000 inside band
3000). The strong contrary report creates genuine uncertainty; the
learner neither clings nor flips.
D2: Su H1 moderate, Sv H1 weak, Sw H1 strong, Sx H1 moderate, Sy H1
strong (copy-discounted, suspected copy of Sw), Sz H1 weak. s1=12750,
s2=6000, margin 6750 >= T=6000. Expected: CONFIDENT H1. The learner
reverts rationally when the new evidence outweighs the old.

## Frozen kill bars

- K1: Scenario A ends with status UNCERTAIN (code 2).
- K2: Scenario B: rel(Sd)==500 after 2 verified lies, and Sd's third
  strong claim contributes exactly 1500.
- K3: Scenario C: copied trio ends PROVISIONAL H1 (11); independent
  trio ends CONFIDENT H1 (13).
- K4: Scenario D: D1 ends UNCERTAIN (22); D2 ends CONFIDENT H1 (13).
- K5: 3/3 byte-identical run outputs (sha256 recorded).
- K6: Rationality 6/6 relative to evidence at time (A, B, C-copied,
  C-indep, D1, D2). Each is 1/1 iff the status above holds for the
  reason stated; any other status is 0/1.

K1-K6 must all PASS for BELIEF-ADVERSARIAL-COMPLETE. K7 (correctness)
is the conjunction.

## Honest scaffold split

Researcher scaffold: table layout, band rule U=wmax/T=2U, halving
discount, copy window 2 and quarter, status cutoffs, world scripts,
strength assignments. Learner-owned: all reliability values, all
support totals, wmax, every copy-discount application, every status
verdict, all provenance answers. Strength is an observation property
recorded at observation time, not a source rank.
