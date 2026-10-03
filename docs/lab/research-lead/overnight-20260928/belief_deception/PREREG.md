# PREREG: Belief-Stance Trajectories Detect Source Defection (H-DECEPT-1, P1)

Frozen: 2026-10-02. This preregistration strictly precedes implementation.
Any deviation amends this file transparently and re freezes; no silent
threshold moves. Commit order self check: this file (with NAMECHECK.md)
commits before any implementation source exists.

## Question

Belief formation (C211) and belief-delayed (C223) proved: reliability
learning is causal, the independence discount works, provenance prevents
double counting, and reliability tracks defection monotonically
(1000 to 800 to 666 in Phase D). UNTESTED: can the learner detect
DECEPTION as a pattern, a source that builds reliability over many
rounds then exploits it with a single high-stakes falsehood? This is the
belief to deception transfer: from tracking reliability scores to
recognizing the defection trajectory.

## Hypothesis H-DECEPT-1

The belief learner (a) rejects a high-stakes falsehood from a
high-reliability source when two independent weaker sources contradict
it, and (b) downgrades the defector FASTER than linear reliability
decay would, recognizing the defection pattern rather than just the
single instance.

## Mechanism (unfrozen variant, same learner as C211/C223)

Identical learner owned machinery: evidence records, source reliability
learned from verification outcomes only (neutral 1000 until 2
verifications, then 1000 * correct / total), independence discount
(k-th claim by the same source for the same hypothesis in one phase
contributes half the previous), event identity register on (duplicates
rejected), belief score B = s1 - s2 in milli units, bands U = wmax
(largest single contribution ever observed) and T = 2U, statuses
NONE / PROVISIONAL / UNCERTAIN / CONFIDENT with the same cutoffs.

Only change: evidence table capacity EVN 32 to 64 with the state layout
shifted accordingly (pure capacity constant, zero semantic change), so
the 33-record deception run never touches FIFO eviction incidentally.

Researcher scaffold (honest): table layout, band rule forms, discount
halving, status cutoffs, event id assignment, weight assignment
(1 weak, 2 moderate, 3 strong; stakes are represented by claim weight).
Learner owned: every reliability value, every support total, wmax,
every status verdict, all provenance answers, the identity register
contents.

## World D1: the deception (fresh learner state)

Sources: 90 = S (the defector), 31 = W1, 32 = W2 (independent weaker
sources).

Build (rounds 1-20): S makes 20 correct weak calibration claims on
verifiable facts (eids 4001-4020). W1 and W2 each make 2 correct weak
calibration claims (eids 4101-4102, 4201-4202). All reliabilities reach
1000.

Deception episode (phase 1): S asserts H1 STRONG (w=3, eid 4301).
W1 asserts H2 moderate (w=2, eid 4302). W2 asserts H2 moderate
(w=2, eid 4303). Ground truth: H2. S's claim is a high-stakes
falsehood, contradicted by two independent weaker sources.

Exposure: the researcher verifies the episode. S claimed H1, truth H2:
S wrong (eid 4304, calibration update only; the recorded evidence
weights s1/s2 are not retro edited).

Aftermath: 5 further calibration rounds, S wrong every round
(eids 4305-4309). This traces the downgrade trajectory.

## World R1: the reverse trap (fresh learner state)

Same build for S (20 correct weak, eids 5001-5020). W1 and W2 each make
2 correct weak calibration claims on the SAME verifiable facts in
lockstep (eids 5101-5102, 5201-5202): their correlation is observable
in the world history, though the learner has no correlation structure.

Reverse episode (phase 1): S asserts H1 STRONG (w=3, eid 5301) and it
is TRUE. W1 and W2 each assert H2 WEAK (w=1, eids 5302-5303) and are
FALSE. S tells an unpopular truth against two correlated weak sources.

## Preregistered mechanistic predictions

P1 (D1 build): rel(S) == 1000 after 20 rounds; rel(W1) == rel(W2)
   == 1000 after 2 rounds each.
P2 (D1 episode): after S's claim st == 11 (PROVISIONAL H1: s1 = 3000,
   s2 = 0, wmax = 3000, T = 6000, 3000 < 6000); after W1's claim
   st == 12 (s2 = 2000, gap 1000 inside U = 3000); after W2's claim
   st == 22 (s1 = 3000, s2 = 4000, gap 1000 inside U = 3000, leader H2).
   Final: s1 == 3000, s2 == 4000.
P3 (D1 exposure): rel(S) == 952, exactly 1000*20/21. The belief stance
   does not move (s1/s2 already recorded); the downgrade lives entirely
   in the source model.
P4 (D1 aftermath): rel(S) after +1..+5 wrong rounds == 909, 869, 833,
   800, 769, exactly 1000*20/(21+k). The trajectory is exactly linear:
   each wrong outcome moves reliability by one instance, no more.
P5 (R1 episode): after S's claim st == 11; after W1's claim st == 12
   (s2 = 1000, gap 2000 inside U); after W2's claim st == 12
   (s1 = 3000, s2 = 2000, gap 1000 inside U). The learner holds with S.
   It does not follow the 2-vs-1 majority: the machinery weights
   evidence, it does not count heads.
P6 (R1 correlation note): the learner has no correlation tracker, so
   W1+W2 are treated as independent (s2 = 2000). The correlation is
   visible in history but not consumable by the machinery; it does not
   change the outcome here because 2000 < 3000 either way.

## Hypothesis verdict rule (frozen)

H-DECEPT-1 holds iff (a) the learner rejects the falsehood, i.e. the
final D1 stance sides with the independent sources (st == 22, P2), AND
(b) the downgrade is faster than linear, i.e. rel(S) after exposure is
STRICTLY BELOW 952 or the aftermath trajectory drops below
1000*20/(21+k) at any point.

Mechanistic analysis of the frozen machinery predicts (a) PASS and (b)
FAIL: reliability is a plain correct/total fraction with no
trajectory-shaped or stake-weighted update, so the downgrade cannot be
faster than linear. If the runs confirm P1-P6 exactly, H-DECEPT-1 is
NOT SUPPORTED as stated: instance rejection works, pattern recognition
is absent. That negative is the finding; it specifies the missing
mechanism (trajectory-shaped reliability / betrayal penalty) as the
next hypothesis.

Rationality scoring (relative to evidence at time): D1(a) st == 22 is
rational 1/1 (two independent moderate sources outweigh one strong
claim; uncertainty is honest given S's real 20-round record). R1
st == 12 is rational 1/1 (S's strong claim outweighs two weak claims;
the correlation is not visible to the machinery, and counting them
independently still loses). Total: 2/2.

## Kill bars

K1: 3/3 runs byte identical (sha256 of stdout equal across run1..run3).
K2: P1 and P2 hold exactly (rel 1000/1000/1000; stance trajectory
    11, 12, 22; s1 == 3000; s2 == 4000).
K3: P3 and P4 hold exactly (952; then 909, 869, 833, 800, 769). Per the
    verdict rule this CONFIRMS instance-only decay and FALSIFIES (b).
K4: P5 holds exactly (stance trajectory 11, 12, 12; s1 == 3000;
    s2 == 2000; final st == 12).
K5: 0 modes, 0 bridges, 0 handlers, 0 new semantic cases. Pure Zag for
    all research logic. Safebin PATH, no forbidden executables.
    Unfrozen variant only; frozen source untouched; paper untouched;
    nothing pushed; explicit pathspecs on every git add/commit.

## Analysis plan

Report per world: reliability checkpoints, per-claim stance trajectory,
the exposure step, and the aftermath trajectory table with the linear
null printed alongside every observed value. Byte verify stdout of the
binary before trusting it (od -c spot check). State plainly whether
H-DECEPT-1 is supported, partially supported, or not supported, with
the exact frozen verdict rule cited.
