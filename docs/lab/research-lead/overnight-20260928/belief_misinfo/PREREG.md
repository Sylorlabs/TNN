# PREREG: Belief under Copied Misinformation and Source Degradation (Parent Queue #7)

Frozen: 2026-10-02. This preregistration strictly precedes implementation.
Any deviation amends this file transparently and re freezes; no silent
threshold moves. Commit order self check: this file (with NAMECHECK.md)
commits before any implementation source exists.

## Question

H-DECEPT-1 (R1) proved the learner holds a minority-true belief against a
false majority: it weights evidence, it does not count heads. UNTESTED:
(a) copied misinformation: the learner copies a FALSE fact from a
high-reliability source; can it later correct when contradicting evidence
arrives, and how many observations does correction require? (b) source
degradation: a previously reliable source becomes noisy over time; does
the learner downgrade its reliability, and by what trajectory? Standing
question: the forgiveness-clock: if the degraded source becomes reliable
again, does it recover, or is the downgrade permanent?

## Mechanism (unfrozen variant, same learner as C211/C223/H-DECEPT-1)

Identical learner owned machinery: evidence records, source reliability
learned from verification outcomes only (neutral 1000 until 2
verifications, then 1000 * correct / total), independence discount
(k-th claim by the same source for the same hypothesis in one phase
contributes half the previous), event identity register, belief score
B = s1 - s2 in milli units, bands U = wmax (largest single contribution
ever observed) and T = 2U, statuses NONE / PROVISIONAL / UNCERTAIN /
CONFIDENT with the same cutoffs. EVN = 64, unchanged from H-DECEPT-1.

Researcher scaffold (honest): table layout, band rule forms, discount
halving, status cutoffs, event id assignment, weight assignment
(1 weak, 2 moderate, 3 strong). Learner owned: every reliability value,
every support total, wmax, every status verdict, all provenance answers,
the identity register contents.

## World M1: copied misinformation, correction, fragility (fresh state)

Sources: 90 = S (trusted, then liar), 31 = W1, 32 = W2 (independent).

Build (rounds 1-20): S makes 20 correct weak calibration claims on
verifiable facts (eids 7001-7020). W1 and W2 each make 2 correct weak
calibration claims (eids 7021-7024). All reliabilities reach 1000.

Copy (phase 1): S asserts H1 STRONG (w=3, eid 7030). Ground truth is H2.
The learner copies the misinformation: provisional H1 belief.

Exposure: the researcher verifies the episode. S claimed H1, truth H2:
S wrong (eid 7031, calibration update only; recorded evidence weights
are not retro edited).

Contradiction (phase 2): W1 asserts H2 moderate (w=2, eid 7032). W2
asserts H2 moderate (w=2, eid 7033).

Fragility (phase 3): S reasserts H1 moderate (w=2, eid 7034) at its now
downgraded reliability. Measures whether the correction survives a
reassertion by the liar.

## World M1b: single-source correction count (fresh state)

Same build as M1 with eids 7101-7124. Phase 1: S asserts H1 STRONG
(w=3, eid 7130), false, truth H2. Phase 2: W1 ALONE contradicts H2
moderate three times (w=2, eids 7131-7133), subject to the independence
discount (contributions 2000, 1000, 500). Measures the correction count
when only one contradicting source exists.

## World M2: noisy source degradation with control (fresh state)

Build: S 20 correct weak (eids 7201-7220). W1 2 correct weak
(eids 7221-7222). Both reach 1000.

Degrade (6 rounds): S goes noisy: wrong, wrong, right, wrong, right,
wrong (hyp 1, truth 2/2/1/2/1/2, eids 7223-7228). W1 stays correct all
6 rounds (eids 7229-7234): the control that downgrade is source
specific, not global drift.

Downstream (phase 1): S asserts H1 moderate (w=2, eid 7235) at its
degraded reliability. Measures how the downgrade discounts S's future
evidence weight in belief.

## World M3: the forgiveness-clock (continues M2 learner state)

Recovery (20 rounds): S becomes fully reliable again: 20 correct weak
calibration claims (hyp 1, truth 1, eids 7301-7320), on the same learner
state as M2 (no reset). Measures whether reliability recovers or the
downgrade is permanent.

## Preregistered mechanistic predictions

P1 (M1 build): rel(S) == 1000 after 20 rounds; rel(W1) == rel(W2) == 1000.
P2 (M1 copy): after S's strong false H1, st == 11 (PROVISIONAL H1:
   s1 == 3000, s2 == 0, wmax == 3000, T == 6000). The learner copies the
   misinformation.
P3 (M1 exposure): rel(S) == 952, exactly 1000*20/21. The stance does not
   move (st stays 11): exposure updates the source model only, the
   recorded false evidence is not retro edited, so the false belief
   persists through exposure.
P4 (M1 contradiction): after W1 moderate H2: st == 12 (s1 == 3000,
   s2 == 2000, gap 1000 inside U == 3000). After W2 moderate H2:
   st == 22 (s2 == 4000, gap 1000 inside U). Correction completes after
   exactly 2 contradicting observations, final stance sides with truth.
P5 (M1 fragility): S reasserts H1 moderate at rel 952: contrib ==
   2*952*1000/1000 == 1904 (first claim in phase 3, discount 1000).
   s1 == 4904, s2 == 4000, gap 904 inside U == 3000: st == 12. The
   correction does NOT survive reassertion; the stance reopens to
   UNCERTAIN. The liar reasserting re-fragilizes belief.
P6 (M1b): W1's three moderate H2 claims contribute 2000, 1000, 500
   (discount halving). Stance trajectory: 12, then 2 (s1 == s2 == 3000,
   exact tie), then 22 (s2 == 3500). Correction count with one
   contradicting source: 3 observations.
P7 (M2 degrade): rel(S) trajectory exactly the fraction:
   952, 909, 913, 875, 880, 846. That is 1000*20/21, 1000*20/22,
   1000*21/23, 1000*21/24, 1000*22/25, 1000*22/26. The downgrade is
   exactly instance linear: each wrong outcome moves reliability by one
   instance, no defector acceleration; noise (2/6 correct) barely
   recovers (909 to 913, 875 to 880). rel(W1) == 1000 throughout.
P8 (M2 downstream): S moderate H1 at rel 846: contrib == 1692
   (2*846*1000/1000), strictly less than the 2000 a rel-1000 source
   would contribute. st == 11 (s1 == 1692, s2 == 0). The downgrade
   discounts future evidence weight.
P9 (M3 forgiveness): continuing from M2 (22/26 == 846), 20 correct
   rounds give rel == 1000*(22+k)/(26+k): at +5: 870, +10: 888,
   +15: 902, +20: 913. After 20 fully clean rounds rel(S) == 913, still
   87 short of 1000. The fraction rule has no forgetting: recovery is
   asymptotic, finite history never restores 1000. The downgrade is
   effectively permanent; the forgiveness-clock as a mechanism is
   ABSENT. This specifies the missing mechanism (recency-weighted
   reliability or a forgiveness window) as the next hypothesis.

## Hypothesis verdict rule (frozen)

BELIEF-MISINFO-COMPLETE iff K1 through K5 all hold. The report must
state: correction counts (2 contradicting observations from two
independent sources; 3 from one discounted source), the fragility result
(one reassertion by the liar reopens uncertainty), the degradation
trajectory versus the linear null, the downstream weight discount, and
the forgiveness behavior (asymptotic recovery to 913 after 20 clean
rounds; downgrade effectively permanent under the fraction rule).

Rationality scoring (relative to evidence at time): M1 correction
st == 22 is rational 1/1 (two independent moderate sources outweigh one
strong stale claim). M1 reassertion st == 12 is rational 1/1 (S at 952
with 20 correct rounds is still a credible source; its reassertion
honestly reopens the question). M1b correction st == 22 is rational 1/1
(discounted contributions still exceed S's stale 3000). M2 downgrade is
rational 1/1 (fraction tracks evidence exactly). M3 non-recovery is
rational 1/1 given the fraction rule, and it is the finding: the rule
itself lacks forgiveness. Total: 5/5.

## Kill bars

K1: 3/3 runs byte identical (sha256 of stdout equal across run1..run3).
K2: P1-P6 hold exactly (M1 build/copy/exposure/contradiction/fragility;
    M1b correction count 3).
K3: P7-P8 hold exactly (M2 degradation trajectory and downstream
    discount; W1 control stays 1000).
K4: P9 holds exactly (M3 recovery 870/888/902/913; nevicted == 0 across
    the combined M2+M3 run of 55 records).
K5: 0 modes, 0 bridges, 0 handlers, 0 new semantic cases. Pure Zag for
    all research logic. Safebin PATH, no forbidden executables.
    Unfrozen variant only; frozen source untouched; paper untouched;
    nothing pushed; explicit pathspecs on every git add/commit.

## Analysis plan

Report per world: reliability checkpoints, per-claim stance trajectory,
the exposure step, degradation and recovery trajectory tables with the
fraction null printed alongside every observed value, correction counts,
and the fragility step. Byte verify stdout of the binary before
trusting it (od -c spot check). State plainly whether each prediction
held, with the exact frozen verdict rule cited, and whether the
forgiveness-clock exists in the current machinery.
