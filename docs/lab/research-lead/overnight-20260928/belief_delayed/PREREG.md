# PREREG: Belief under Delayed Evidence and Rediscovery (H extension)

Frozen: 2026-10-02. This preregistration strictly precedes implementation.
Any deviation amends this file transparently and re freezes; no silent
threshold moves.

## Question

Belief formation (commit 78e5a5eac) proved 3/3 rational belief revision with
reliability learning and the independence discount both causal by ablation.
UNTESTED: (1) delayed evidence arriving long after a belief settled; does
the delay itself weaken the prior? (2) evidence evicted under memory
pressure then rediscovered; does the belief double count, or does
provenance prevent it? (3) a source reliable for many rounds that turns
adversarial; does reliability learning track the turn?

## Mechanism (unfrozen variant, extends 78e5a5eac)

Same learner owned machinery as the baseline: evidence records, source
reliability learned from verification outcomes only (neutral 1000 until 2
verifications), independence discount (k-th claim by same source for same
hypothesis in one episode contributes half the previous), belief score
B = s1 - s2 in milli units, bands U = wmax (largest single contribution
ever observed) and T = 2U, statuses NONE/PROVISIONAL/UNCERTAIN/CONFIDENT
with the same cutoffs.

New machinery for this experiment (all learner state, no new subsystems):

1. Finite evidence table (EVN = 32 records) with FIFO eviction under
   memory pressure. Eviction drops the record but the score contribution
   persists: the learner remembers the bottom line and forgets the receipt.
   This is the honest forgetting model under test.
2. Event identity register (IDN = 128 event ids). Every observation carries
   a researcher assigned event id. A re presented event whose id is already
   registered is rejected as a duplicate: no new record, no score change,
   ndup counter increments. This is familiarity without recall: the
   learner cannot reproduce the evicted receipt but knows it has seen
   this evidence before. Genuine new events (new ids) are always counted.
3. Ablation arm NAIVE: identity register disabled entirely (baseline
   behavior under pressure). Expected to double count on rediscovery;
   this arm is the bug control, not a rationality pass.

Researcher scaffold (honest): table layout, FIFO order, identity register
form, band rule forms, discount halving, status cutoffs, event id
assignment. Learner owned: every reliability value, every support total,
wmax, every status verdict, every duplicate verdict, all provenance
answers, the identity register contents.

## World script (fixed, deterministic, no randomness)

Sources: 1=Sa, 2=Sb, 3=Sc, 4=Sd, 5=Se, 6=Sf, 7=Sg, 8=Sh, 9=Si,
10..21 delay sources, 30..61 burst sources, 90=Sx.
Weights: 1 weak, 2 moderate, 3 strong.

Calibration (seqs 1-4): Sa claims H1 weak truth H1 correct; Sa claims H2
weak truth H1 wrong (Sa 1/2, rel 500); Sb claims H2 weak truth H2 correct;
Sb claims H2 moderate truth H2 correct (Sb 2/2, rel 1000). wmax = 2000.

Phase A, settle H1 (seqs 5-7, phase 1, eids 101-103): Sb, Sc, Sd each report
H1 moderate once. Contributions 2000 each. s1 = 6000, s2 = 0.

Phase B1, delay (seqs 8-19, eids 1001-1012): 12 unrelated calibration
events on verifiable facts with fresh sources 10..21, weak claims,
alternating truth. Each contribution 1000, below wmax. No reliability
change for any phase A or B source. The delay contains more events (12)
than the entire prior history (7).

Phase B2, delayed strong H2 evidence (seqs 20-23, phase 2, eids 201-204):
fresh sources Se, Sf, Sg, Sh each report H2 strong once. Contributions
3000 each. wmax becomes 3000, U = 3000, T = 6000.

Phase C, pressure burst (32 events, eids 2001-2032): 32 unrelated weak
calibration events with fresh sources 30..61. Pre burst records = 23
(4 cal + 3 A + 12 delay + 4 B2). Table capacity 32, so exactly the 23
oldest records are evicted FIFO, including all 4 H2 records. Scores
persist by design.

Phase C, rediscovery (phase 3): the SAME 4 H2 strong events re presented
with identical eids 201-204, sources, and weights. Then one genuine new
H2 strong event from fresh source Si with new eid 205.

Phase D, adversarial turn (separate fresh state): Sx does 20 correct weak
calibration rounds, then one Sx H1 moderate observation (eid 3031,
phase 1), then 10 wrong weak calibration rounds, then one Sx H1 moderate
observation with a new eid (eid 3052, phase 2).

## Preregistered expectations

E1 (Phase A): st == 13 (CONFIDENT H1), s1 == 6000, s2 == 0.
E2 (Phase B1 delay): status, s1, s2, wmax all unchanged vs pre delay
   (st == 13, s1 == 6000, s2 == 0, wmax == 2000). The delay itself does not
   weaken the prior: no contrary evidence, no change. Rational 1/1.
E3 (Phase B2): after 1st strong claim st == 12 (UNCERTAIN, leader still H1:
   the settled 6000 prior leads the single 3000 contrary claim by 3000,
   exactly inside the uncertainty band U = 3000); after 2nd st == 2
   (UNCERTAIN, tied); after 3rd st == 22; after 4th st == 23
   (CONFIDENT H2). first_contrary_seq == 20, revision_seq == 23, contrary
   pieces to confident revision == 4, final s2 == 12000. Rational 1/1:
   strong independent evidence outweighs the settled prior; the learner
   neither flips on first contact nor holds stubbornly. Amendment
   2026-10-02 (transparent, before frozen evaluation runs): the original
   text wrote st == 22 after the 1st claim; that was an arithmetic slip
   in the prereg (s1 = 6000 still exceeds s2 = 3000 after one claim).
   The band rule predicts 12, and the directional uncertainty (leaning
   the settled prior) is itself a finding. No other expectation changes.
E4 (Phase C eviction): nevicted == 23, s1 == 6000, s2 == 12000, st == 23,
   belief_why(H2) returns 0 retained records while the identity register
   reports the 4 H2 eids as seen.
E5 (Phase C rediscovery, PROV arm): all 4 re presented events rejected,
   ndup == 4, record count unchanged, s2 == 12000. No double count.
   Rational 1/1.
E6 (Phase C rediscovery, NAIVE arm): 4 fresh records added,
   s2 == 24000. Double count demonstrated: the standing belief contains
   the same 4 events twice. Scored 0/1 as the expected fail bug control.
E7 (Phase C genuine new): eid 205 accepted, s2 == 15000. The register
   does not over block. Rational 1/1 (counted with E5).
E8 (Phase D): rel after 20 correct == 1000; rel after 5 adversarial ==
   800; rel after 10 adversarial == 666; monotonic decrease. Reliable
   phase claim contribution == 2000; adversarial phase claim contribution
   == 1332 < 2000. Reliability learning tracks the turn. Rational 1/1.

Rationality total: 5/6 (A, B1, B2, C-PROV, D pass; C-NAIVE is the
documented bug control at 0/1).

## Kill bars

K1: 3/3 runs byte identical (sha256 of stdout equal across run1..run3).
K2: E1 holds exactly (st 13, s1 6000, s2 0).
K3: E2 holds exactly (delay changes nothing).
K4: E3 holds exactly (latency 4, seqs 20/23, final st 23, s2 12000).
K5: E4 and E5 hold exactly (PROV arm: nevicted 23, ndup 4, s2 12000).
K6: E6 holds exactly (NAIVE arm s2 24000; the bug must appear, else the
    provenance machinery is unmotivated and the result is VOID).
K7: E7 holds exactly (s2 15000 after genuine new event).
K8: E8 holds exactly (rels 1000/800/666, contribs 2000 vs 1332).
K9: 0 modes, 0 bridges, 0 handlers, 0 new semantic cases. Pure Zag for
    all research logic. Safebin PATH, no forbidden executables.
    Unfrozen variant only; frozen source untouched; paper untouched;
    nothing pushed; explicit pathspecs on every git add/commit.

## Analysis plan

Report per phase: status line (leader, status, s1, s2, conf, U, T),
revision latency, eviction counts, duplicate counts, reliability
checkpoints, and the why provenance listings. Byte verify stdout of the
binary before trusting it (od -c spot check). Compare PROV vs NAIVE on
the rediscovery step as the causal test of the identity register.
