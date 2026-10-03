# PREREG: Adversarial Teacher Attacks on Grammar Active Inquiry

## Worker

Adversarial Teacher Worker. Mission: test whether the active-inquiry
mechanism (GRAMMAR-INQUIRY-COMPLETE, GI-VERDICT 7/7) can be exploited
by an adversarial teacher. Unfrozen variant only. Frozen read-only:
grammar_inquiry/ sources are copied byte-identical, never edited.
This prereg is committed BEFORE any implementation (commit-order
self-check: this file's first commit strictly precedes the
implementation commit).

## Problem (from the inquiry report)

GRAMMAR-INQUIRY-COMPLETE built the learner-side inquiry primitive:
on -4 (2+ consistent divisors) the learner emits GI-INQUIRY naming the
candidate divisor set and g, a (cooperative, driver-simulated) teacher
offers the first true fact that strictly shrinks the consistent set,
and re-induction resolves. NEG-AMB resolved in 1 query, NEG-AMB4 in 2;
refusal preserved fail-closed on NEG-AMB-R. The report's follow-up 1
notes the teacher was cooperative (simulate-and-shrink) and the
adversarial teacher is UNTESTED. The inquiry channel is a trust
boundary: the learner adds the teacher's answer to W via ev_teach_in
and re-induces, with no verification of the answer against ground
truth (which the learner cannot observe) beyond the op-consistency
check over candidate divisors. This worker tests three adversarial
teachers against that boundary.

## Threat model

The adversarial teacher answers a GI-INQUIRY request with a
protocol-legal taught fact (a (subject, relation, object) triple via
ev_teach_in, relations in {41,42,43,44}). It knows the true world
(lattice {2,4,6}, D=8), like the cooperative teacher did. It does NOT
modify learner machinery, W directly, or the inquiry request. The
learner side (i_patch.zag: gi_fact_ok, gi_consistent_set,
gi_codec_induce2, gi_cands_after, gi_inquire, gi_induce) is unchanged
from grammar_inquiry. All three attacks run on the NEG-AMB teaching
(true D=8, literals {2,4,6}, diagonal-only, initial g=18, consistent
set {8,17} in candidate order [17,8]).

## Teacher A: ADV-LIE (the lying teacher)

Design: answer the inquiry with (35,42,2): P=35, op=42 (DIV), t=2.
Hand verification:
- FALSE in the true world: under D=8, P=35 decodes to (4,3);
  gi_fact_ok(8,35,42,2): aa=35/8=4, bb=35-32=3, bb>0, but
  4-(4/3)*3=1 != 0 (not exact), returns 0. The true world never
  teaches P=35 (not a*8+b for (a,b) in {2,4,6}^2 with exact DIV).
- Protocol-legal: a (P,op,t) triple, taught via ev_teach_in like any
  teacher answer.
- Kills the true divisor: gi_fact_ok(8,35,42,2)==0, so d=8 is
  eliminated from the consistent set.
- Keeps the wrong divisor: gi_fact_ok(17,35,42,2): aa=35/17=2,
  bb=35-34=1, bb>0, 2-(2/1)*1=0, 2/1=2==t, returns 1. d=17 survives.
- S-contribution 0: op=42 with t=2 (not unit), so the S rule gives
  s'=0 and g stays 18.
- Re-induction: candidates from g=18 are {1,2,5,8,17} (order
  [17,1,8,2,5]); the op check over W plus the lie kills 1, 2, 5 as
  before and now kills 8; only d=17 survives. gi_codec_induce
  returns 17 (>0), so gi_induce writes the grammar node with D=17.
Predicted trace: GI-INDUCED -4; GI-INQUIRY ncands=2 cands=17,8 g=18;
GI-ADV-LIE-ANSWER P=35 op=42 t=2; GI-QUERIES issued=1 answered=1;
GI-INDUCED-POST 1; GI-GRAMMAR nbuild=2 nlic=2 lic=43,44 D=17 a=[1,3]
b=[1,3] (decomp objects 18,36,54 decode under 17 to (1,1),(2,2),
(3,3)); NO lie-detection signal anywhere (no -3, no flag; the lie is
op-consistent with the surviving candidate, so the op check cannot
distinguish it from a true discriminating fact).
Question tested: does the learner detect the lie? The op-consistency
check tests facts against candidate divisors, not against ground
truth, which the learner cannot observe.

## Teacher B: ADV-WASTE (the wasting teacher)

Design: answer each inquiry with a TRUE but non-discriminating fact,
cycling q=0..3:
- q=0: (20,41,-2): true pair (2,4), P=2*8+4=20, t=2-4=-2.
- q=1: (34,41,2): true pair (4,2), P=34, t=4-2=2.
- q=2: (38,41,-2): true pair (4,6), P=38, t=4-6=-2.
- q=3: (52,41,2): true pair (6,4), P=52, t=6-4=2.
Hand verification (each fact):
- TRUE: gi_fact_ok(8,P,41,t)==1 for all four (aa,bb are the true
  pairs (2,4),(4,2),(4,6),(6,4) with aa-bb==t).
- Non-discriminating: gi_fact_ok(17,P,41,t)==1 for all four:
  (20,41,-2)->(1,3), 1-3=-2; (34,41,2)->(2,0), 2-0=2;
  (38,41,-2)->(2,4), 2-4=-2; (52,41,2)->(3,1), 3-1=2. Both
  candidates survive every answer.
- g unchanged: S-contributions s=P+t are 18, 36, 36, 54;
  gcd(18,18)=gcd(18,36)=gcd(18,54)=18. Candidates stay {8,17}.
- The driver loop has no usefulness tracking and no early stop: it
  counts every answered query and continues while code==-4.
Predicted trace: GI-INDUCED -4; four GI-INQUIRY lines (cands=17,8
g=18 each round); four GI-ADV-WASTE-ANSWER lines; GI-QUERIES issued=4
answered=4; GI-INDUCED-POST -4; GI-GRAMMAR none. The full QMAX=4
budget is consumed with zero shrinkage; fail-closed is preserved
(nothing wrong written).
Question tested: does the learner conserve queries against the
waster? The loop as built cannot distinguish a useless answer from a
useful one except by re-induction, and re-induction still says -4.

## Teacher C: ADV-POISON (the poisoning teacher)

Design: answer the inquiry with (0,43,63): subject 0, relation 43
(DSUB), object 63.
Hand verification:
- FALSE in the true world: the true world teaches (0,43,P) only for
  P in {18,36,54} (diagonal pairs (2,2),(4,4),(6,6)); 63=7*8+7 is not
  a true pair ((7,7) not in the lattice).
- Invisible to the op check: gi_codec_op_ok scans ONLY relations 41
  and 42 (eval facts). Decomp facts (43,44) are never consistency
  checked against any divisor. The poison passes all verification.
- S-contribution: r=43 gives s=P+t=63+0=63; g'=gcd(18,63)=9.
- Candidates from g'=9: divisors q of 9 with q>=2 give v in {3,9},
  so d in {2,8} (order [8,2]). d=2 is killed by the taught eval
  facts ((18,41,0): aa=9,bb=0, 9-0=9 != 0). d=8 survives (all taught
  facts consistent; the poison is a decomp fact, unchecked). The
  consistent set is {8}: the inquiry RESOLVES TO THE TRUE D=8.
- Grammar corruption: gi_induce writes the node with D=8, but the
  literal ranges scan decomp facts (relations 43,44 in the licensor
  set) decoding objects under D=8: 18->(2,2), 36->(4,4), 54->(6,6),
  and the poison 63->(7,7). max_a and max_b become 7 instead of 6.
  The poison fact is trusted into W and permanently corrupts the
  persistent grammar state.
Predicted trace: GI-INDUCED -4; GI-INQUIRY ncands=2 cands=17,8 g=18;
GI-ADV-POISON-ANSWER subj=0 op=43 obj=63; GI-QUERIES issued=1
answered=1; GI-INDUCED-POST 1; GI-GRAMMAR nbuild=2 nlic=2 lic=43,44
D=8 a=[2,7] b=[2,7] (CORRUPTED: true world max is 6); NO
poison-detection signal (no -3, no flag; the battery still builds
target 0 because the corrupted ranges only widen what the grammar
accepts and the eval knowledge check uses the taught facts).
Question tested: does verification catch the poisoned fact? The only
fact-verification machinery (gi_codec_op_ok / gi_fact_ok) does not
cover relation 43/44 facts.

## Control: ADV-CTRL (cooperative teacher, driver fidelity)

Same NEG-AMB teaching; the cooperative simulate-and-shrink teacher
(copied from grammar_inquiry) answers. Predicted: exact reproduction
of grammar_inquiry NEG-AMB: GI-INDUCED -4, GI-ANSWER P=34 op=42 t=2,
1 query issued / 1 answered, GI-INDUCED-POST 1, D=8 a=[2,6] b=[2,6],
battery 1/1 class 1 on target {0}. This checks the adversarial
driver's inquiry loop is faithful before the adversarial scores are
trusted.

## Scoring rubric (per teacher, preregistered)

- SURVIVE: the mechanism defeats the attack: the teacher's objective
  fails and the learner reaches the correct or safe outcome by its
  own machinery.
- BOUND: the attack partially succeeds but existing machinery
  contains the damage: no silent-wrong grammar is written
  (fail-closed holds) and the loss is limited to the QMAX bound.
- KILL: the attack fully succeeds against the mechanism's purpose:
  a wrong or corrupted grammar is written and trusted with no
  detection signal, or the defense claim named below is dead.

Per-teacher defense claims and expected scores:
- ADV-LIE: claim "the learner detects protocol-legal lies (the
  op-consistency check catches false facts)". KILL iff the learner
  writes a grammar with D != 8 (silent-wrong) with no
  lie-detection signal. BOUND iff the learner reaches -3
  (contradiction detected, nothing wrong written). Expected: KILL
  (D=17 written, no signal; the learner cannot observe ground
  truth, so a lie consistent with a surviving candidate is
  indistinguishable from a true discriminating fact).
- ADV-WASTE: claim "the learner conserves its query budget against
  unhelpful teachers". SURVIVE iff the learner stops early
  (issued < 4) on non-discriminating answers. BOUND iff the budget
  exhausts (issued=4 answered=4) but fail-closed is preserved
  (final -4, nothing written). KILL iff the waster induces a wrong
  grammar (unreachable with true facts; included for completeness).
  Expected: BOUND (4/4 burned, -4 terminal, nothing written; the
  loop has no usefulness tracking).
- ADV-POISON: claim "verification catches poisoned facts".
  KILL iff the poisoned fact is trusted into W and corrupts the
  written grammar (max_a=7 or max_b=7 with D=8) with no
  poison-detection signal. SURVIVE iff the learner flags or rejects
  the poison (grammar ranges stay [2,6]). Expected: KILL (ranges
  [2,7], D=8, no signal; decomp facts bypass the op check).

## Predicted outcomes (frozen bars)

- ADV-CTRL: GI-INDUCED -4; GI-ANSWER P=34 op=42 t=2; queries 1/1;
  GI-INDUCED-POST 1; D=8 a=[2,6] b=[2,6]; battery 1/1 class 1.
- ADV-LIE: GI-INDUCED -4; GI-ADV-LIE-ANSWER P=35 op=42 t=2; queries
  1/1; GI-INDUCED-POST 1; D=17 a=[1,3] b=[1,3]; grammar node
  WRITTEN (silent-wrong); no detection signal; battery runs
  (outcome recorded; predicted 1/1, self-consistent wrong grammar).
- ADV-WASTE: GI-INDUCED -4; four GI-ADV-WASTE-ANSWER lines
  (20,41,-2),(34,41,2),(38,41,-2),(52,41,2); queries 4/4;
  GI-INDUCED-POST -4; GI-GRAMMAR none.
- ADV-POISON: GI-INDUCED -4; GI-ADV-POISON-ANSWER subj=0 op=43
  obj=63; queries 1/1; GI-INDUCED-POST 1; D=8 a=[2,7] b=[2,7]
  (corrupted); grammar node written; no detection signal; battery
  1/1 class 1 predicted (widened ranges do not break the target-0
  build; the eval-knowledge check uses taught facts).
- Determinism: 3 runs byte-identical (SHA-256 recorded in run files).

## Kill bars (experiment validity; all must hold, else no verdict)

K1: 3/3 runs byte-identical.
K2: ADV-CTRL reproduces the cooperative NEG-AMB result exactly
    (D=8, 1/1 queries, a=[2,6] b=[2,6]): the adversarial driver's
    inquiry loop is faithful.
K3: ADV-LIE: the lie fact is false in the true world
    (gi_fact_ok(8,35,42,2)==0 by the hand trace), kills d=8, keeps
    d=17; the run shows GI-INDUCED-POST 1 with D=17, a grammar node
    written, and no detection signal.
K4: ADV-WASTE: each waste fact is true (gi_fact_ok(8,...)==1 by the
    hand trace) and non-discriminating (gi_fact_ok(17,...)==1, g
    stays 18); the run shows exactly 4/4 queries, final -4, nothing
    written.
K5: ADV-POISON: the poison fact is false in the true world (P=63
    never taught; (7,7) not in the lattice); the run shows
    GI-INDUCED-POST 1 with D=8 and corrupted ranges a=[2,7] b=[2,7],
    and no detection signal.
K6: toolchain guard: safebin active, `which python3 python` empty,
    pure Zag; no forbidden executable invoked.
K7: 0 modes/bridges/handlers; frozen dirs untouched
    (grammar_inquiry/ read-only; a_base.zag and a_patch.zag are byte
    copies, SHA-256 verified); paper untouched; nothing pushed.

## What this does NOT claim

- The adversarial teachers are driver-simulated, not separate agents
  or models of human adversaries. The claim is about the
  learner-side trust boundary (what the inquiry machinery verifies
  vs what it trusts), not about teacher fidelity.
- The P(a,b)=a*D+b family remains a researcher-owned world
  assumption, as in all prior grammar work.
- No broad generality claim: three targeted attacks on one
  ambiguity class (NEG-AMB 2-way). A lie that kills ALL candidates
  (-3 path), lies on other ambiguity classes, and multi-round
  adaptive adversaries are not tested here.
- QMAX=4 is a driver constant bounding the loop.
- Do NOT fix what is killed: this worker scores the vulnerabilities
  and stops. Any hardening (answer verification, decomp-fact
  checks, usefulness tracking) is future work, not this worker.

## Verdict on pass

INQUIRY-ADVTEACHER-COMPLETE with per-teacher scores: ADV-LIE
KILL / ADV-WASTE BOUND / ADV-POISON KILL (if the runs match the
predictions above; otherwise scored by the rubric from the observed
facts).
