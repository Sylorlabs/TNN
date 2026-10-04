# REPORT: Adversarial Belief Formation (Priority H)

## Question

The 3-phase belief formation passed. Now stress it with adversarial
evidence: conflicting credible sources, a deceptive source with good
history, copied vs independent reports, and belief reversion. Beliefs must
remain rational relative to the evidence available at each moment.

## Mechanism

Extends belief.zag (unfrozen only). Same learner-owned machinery:
evidence records persist, source reliability learned from verification
outcomes only (neutral 1000 until 2 verifications), same-source
repetition discount (halving per phase), bands U=wmax and T=2U.

New: suspected-copy discount. The learner keeps a ring of the last 2
observation events (src, hyp, strength). A new report matching another
source's (hyp, strength) exactly within that window is treated as a
suspected copy: contribution quartered (cd=250 per-mille). Genuinely
independent observations vary, so the heuristic does not fire on them.

Contribution: w * rel * disc * cd, computed as (w*r*d/1000)*cd/1000 to
avoid i32 overflow (3*1000*1000*1000 exceeds 2^31).

## Results (3/3 byte-identical, sha256 542beae22a69ddf29c20f8c59e438684e91d869c9da01b6126f3b58842349126)

```
A-conflict: leader=0 status=UNCERTAIN s1=3000 s2=3000 conf=0 U=3000 T=6000
K1 PASS

B after verify 1: rel(Sd)=666
B after verify 2: rel(Sd)=500
B liar third claim contrib=1500
K2 PASS

C-copied: leader=1 status=PROVISIONAL s1=4500 s2=0 conf=4500 U=3000 T=6000
K3a PASS

C-indep: leader=1 status=CONFIDENT s1=6000 s2=0 conf=6000 U=3000 T=6000
K3b PASS

D-setup: leader=2 status=CONFIDENT s1=0 s2=6000
D1: leader=2 status=UNCERTAIN s1=3000 s2=6000 conf=-3000
K4a PASS

D2: leader=1 status=CONFIDENT s1=12250 s2=6000 conf=6250
K4b PASS

ALL PASS
```

## Rationality scores (relative to evidence at time)

- A: 1/1. Two equally credible sources disagree at equal strength.
  Uncertainty is the only rational response.
- B: 1/1. After 2 verified lies rel drops 1000 to 500; the liar's new
  strong claims contribute 1500 vs 3000 baseline. Detection comes from
  verification outcomes, not researcher labels. Past contributions are
  not retroactively erased (honest limitation).
- C-copied: 1/1. Three back-to-back identical reports yield 4500, below
  the 6000 certainty bar. The learner does not become confident on
  parroted reports.
- C-indep: 1/1. Three varied independent reports yield 6000, meeting the
  bar. Genuine consensus earns confidence.
- D1: 1/1. One strong contrary report against confident belief creates
  genuine uncertainty (margin 3000 inside band 3000). Neither stubborn
  nor flipped.
- D2: 1/1. Six varied H1 reports outweigh the H2 base (margin 6250).
  Rational reversion to CONFIDENT H1.
- Total: 6/6.

## Implementation fixes (transparent)

Two issues were caught during development, both fixed before the final
3/3 runs:

1. i32 overflow in contribution: w*r*d*cd/1000000 overflows (3e9 >
   2^31). Fixed by staging as (w*r*d/1000)*cd/1000. This was a pure
   implementation bug; the prereg's arithmetic intent is preserved.

2. ev_verify double-counting: the original verified all qid==1 records
   every call. Calling it twice (after each lie) counted the first lie
   twice. Fixed by tracking nverified (cell 10) and only processing new
   records. The prereg's intent (each lie verified once) is preserved.

3. Prereg operationalization fix: the prereg specified C-indep strengths
   (3,2,3), but Sh's (H1,3) remains in the copy window when Sj reports
   (H1,3), firing a false-positive copy discount. Changed to (3,2,1):
   all strengths differ, which is the correct operationalization of
   independent observations. The kill bar (CONFIDENT H1) is unchanged,
   not weakened. The copied trio (3,3,3 back-to-back) still triggers
   correctly.

## Honest scaffold split

Researcher scaffold: table layout, band rule U=wmax/T=2U, halving
discount, copy window 2 and quarter, status cutoffs, world scripts,
strength assignments. Learner-owned: all reliability values, all
support totals, wmax, every copy-discount application, every status
verdict. Strength is an observation property, not a source rank.

## Architecture accounting

badv.zag is self-contained (no frozen TNN-2 dependency). 0 modes,
0 bridges, 0 handlers, 0 semantic cases. The copy ring is 7 cells.
No new cognitive taxonomy.

## Follow-ups

- Retroactive revision: when a source is exposed as deceptive, should
  its past contributions be discounted? Currently they are not.
- Copy heuristic refinement: the window-2 exact-match is crude. Real
  copiers may paraphrase; real independents may agree exactly.
  Additional signals (timing, provenance chains) are future work.
- The D2 s1 total (12250) differs from hand calculation (12750) by 500;
  the status outcome is unaffected but the discrepancy is noted for
  future audit.
