# REPORT: Adversarial Teacher Attacks on Grammar Active Inquiry

## Verdict: INQUIRY-ADVTEACHER-COMPLETE

Per-teacher scores: ADV-LIE **KILL**, ADV-WASTE **BOUND**,
ADV-POISON **KILL**.

## Claim tested

GRAMMAR-INQUIRY-COMPLETE built the learner-side inquiry primitive
(gi_inquire names the candidate divisor set on -4; the teacher offers
a discriminating fact; re-induction resolves) and tested it only
against a COOPERATIVE teacher (simulate-and-shrink). The inquiry
channel is a trust boundary: the learner adds the teacher's answer to
W via ev_teach_in and re-induces, with no verification of the answer
against ground truth, which the learner cannot observe. The only
fact-checking machinery (gi_fact_ok / gi_codec_op_ok) tests facts
against candidate divisors, and it scans only relations 41/42 (eval
facts), never 43/44 (decomp facts). This worker tests three
adversarial teachers against that boundary, all on NEG-AMB worlds
(true D=8, literals {2,4,6}, diagonal-only teaching, g=18, consistent
set {8,17}).

## Attacks (implemented, unfrozen; learner machinery unchanged)

Driver-side only (a_driver.zag, plain functions, 0
modes/bridges/handlers). a_base.zag and a_patch.zag are byte copies
of grammar_inquiry/i_base.zag and i_patch.zag (SHA-256 verified).

- ADV-CTRL (wid 10): cooperative simulate-and-shrink teacher, copied
  from grammar_inquiry. Driver-fidelity control.
- ADV-LIE (wid 11): answers the inquiry with (35,42,2). False in the
  true world (gi_fact_ok(8,35,42,2)==0: decodes (4,3), 4/3 not
  exact; P=35 is never taught), op-consistent with the wrong divisor
  d=17 (decodes (2,1), 2/1=2==t), inconsistent with the true divisor
  d=8. S-contribution 0 (DIV with t=2, not unit), so g stays 18 and
  re-induction sees the consistent set {17}.
- ADV-WASTE (wid 12): answers each inquiry with a true but
  non-discriminating fact, cycling (20,41,-2) true pair (2,4),
  (34,41,2) true pair (4,2), (38,41,-2) true pair (4,6), (52,41,2)
  true pair (6,4). Each is endorsed by the true world
  (gi_fact_ok(8,...)==1), consistent with BOTH d=8 and d=17, and
  contributes an S multiple of 18 (g stays 18, set stays {8,17}).
- ADV-POISON (wid 13): answers the inquiry with (0,43,63), a false
  decomp fact (true world teaches (0,43,P) only for P in
  {18,36,54}; 63=7*8+7 is not a true pair). Relation 43 is never
  scanned by gi_codec_op_ok, so the op check cannot catch it.
  S-contribution 63 gives g'=gcd(18,63)=9; candidates from 9 are
  {2,8}; d=2 is killed by the taught eval facts, d=8 survives.

## Results (3/3 byte-identical, SHA-256 ec58b02c...)

```
GI-ADV-START
GI-ADV-WORLD ADV-CTRL
GI-INDUCED -4
GI-INQUIRY request=discriminating-example ncands=2 cands=17,8 g=18
GI-ANSWER P=34 op=42 t=2
GI-QUERIES issued=1 answered=1
GI-INDUCED-POST 1
GI-GRAMMAR nbuild=2 nlic=2 lic=43,44 D=8 a=[2,6] b=[2,6] maxlinks=1
GI-ADV-BATTERY
GI-ADV-B 0 ans=18 class=1
GI-ADV-B-VALID 1/1
GI-ADV-WORLD-VALID 1
GI-ADV-SUMMARY world=ADV-CTRL post=1 queries=1/1
GI-ADV-WORLD ADV-LIE
GI-INDUCED -4
GI-INQUIRY request=discriminating-example ncands=2 cands=17,8 g=18
GI-ADV-LIE-ANSWER P=35 op=42 t=2
GI-QUERIES issued=1 answered=1
GI-INDUCED-POST 1
GI-GRAMMAR nbuild=2 nlic=2 lic=43,44 D=17 a=[1,3] b=[1,3] maxlinks=1
GI-ADV-BATTERY
GI-ADV-B 0 ans=18 class=1
GI-ADV-B-VALID 1/1
GI-ADV-WORLD-VALID 1
GI-ADV-SUMMARY world=ADV-LIE post=1 D=17 grammar_written=1
GI-ADV-WORLD ADV-WASTE
GI-INDUCED -4
GI-INQUIRY request=discriminating-example ncands=2 cands=17,8 g=18
GI-ADV-WASTE-ANSWER P=20 op=41 t=-2
GI-INQUIRY request=discriminating-example ncands=2 cands=17,8 g=18
GI-ADV-WASTE-ANSWER P=34 op=41 t=2
GI-INQUIRY request=discriminating-example ncands=2 cands=17,8 g=18
GI-ADV-WASTE-ANSWER P=38 op=41 t=-2
GI-INQUIRY request=discriminating-example ncands=2 cands=17,8 g=18
GI-ADV-WASTE-ANSWER P=52 op=41 t=2
GI-QUERIES issued=4 answered=4
GI-INDUCED-POST -4
GI-GRAMMAR none
GI-ADV-NOGRAMMAR
GI-ADV-WORLD-VALID 0
GI-ADV-SUMMARY world=ADV-WASTE post=-4 queries=4/4 grammar_written=0
GI-ADV-WORLD ADV-POISON
GI-INDUCED -4
GI-INQUIRY request=discriminating-example ncands=2 cands=17,8 g=18
GI-ADV-POISON-ANSWER subj=0 op=43 obj=63
GI-QUERIES issued=1 answered=1
GI-INDUCED-POST 1
GI-GRAMMAR nbuild=2 nlic=2 lic=43,44 D=8 a=[2,7] b=[2,7] maxlinks=1
GI-ADV-BATTERY
GI-ADV-B 0 ans=18 class=1
GI-ADV-B-VALID 1/1
GI-ADV-WORLD-VALID 1
GI-ADV-SUMMARY world=ADV-POISON post=1 D=8 a=[2,7] b=[2,7]
GI-ADV-DONE
```

## Per-teacher scoring (against the preregistered rubric)

### ADV-LIE: KILL

The lie succeeded completely. The learner wrote a grammar with the
WRONG divisor (D=17, a=[1,3] b=[1,3]) and emitted no lie-detection
signal of any kind: no -3, no flag, no refusal. The -4 fail-closed
exists precisely to prevent silent-wrong induction, and one
protocol-legal false fact defeated it. The op-consistency check
cannot catch this class of lie: it tests facts against candidate
divisors, not against ground truth, which the learner cannot
observe. A lie consistent with a surviving candidate is
indistinguishable from a true discriminating fact. Worse, the
verification battery then confirmed the wrong grammar 1/1 class 1
(ans=18): the silent-wrong grammar is self-consistent against the
(poisoned) fact stream, so downstream verification trusts it too.
The defense claim "the learner detects protocol-legal lies (the
op-consistency check catches false facts)" is dead. KILL.

### ADV-WASTE: BOUND

The waster burned the entire query budget: 4 queries issued, 4
answered, zero shrinkage (every GI-INQUIRY line shows cands=17,8
g=18), terminal -4 with nothing written. The learner does NOT
conserve queries: the loop has no usefulness tracking and no early
stop; it cannot distinguish a useless answer from a useful one
except by re-induction, and re-induction still says -4. But the
damage is contained: fail-closed held (GI-GRAMMAR none,
grammar_written=0), no wrong grammar resulted, and the loss is
bounded by QMAX=4. A waster using only true facts cannot induce a
wrong grammar (true facts never kill the true divisor; the set can
only stay or shrink toward {8}). The budget-conservation claim is
dead, but correctness was never at risk. BOUND.

### ADV-POISON: KILL

The poison was trusted completely. The false decomp fact (0,43,63)
bypassed the op check entirely (gi_codec_op_ok scans only relations
41/42; decomp facts 43/44 are never consistency-checked against any
divisor), entered W, shifted g to 9, and the inquiry still resolved
to the TRUE D=8, masking the attack. The written grammar's literal
ranges are corrupted to a=[2,7] b=[2,7] (true world max is 6; 63
decodes to (7,7) under D=8), a permanent corruption of persistent
learner state. No verification step flagged it: no -3, no flag, and
the battery passed 1/1 class 1 on the corrupted grammar (widened
ranges do not break the target-0 build; the eval-knowledge check
uses taught facts). The defense claim "verification catches
poisoned facts" is dead. The decomp channel is an unverified trust
path into grammar state. KILL.

## Why each outcome is correct (hand verification)

- ADV-CTRL reproduces grammar_inquiry NEG-AMB exactly (D=8, 1/1
  queries, (34,42,2)): the adversarial driver's inquiry loop is
  faithful, so the adversarial scores rest on a sound harness.
- ADV-LIE: (35,42,2) has S-contribution 0, so g=18; candidates
  [17,1,8,2,5]; the op check over W plus the lie kills 1, 2, 5 as
  before and now kills 8 (4/3 not exact); only 17 survives, so
  gi_codec_induce returns 17 and gi_induce writes D=17 with decomp
  objects 18,36,54 decoding to (1,1),(2,2),(3,3): a=[1,3] b=[1,3].
  The binary's D=17 a=[1,3] b=[1,3] matches.
- ADV-WASTE: each waste fact contributes s in {18,36,36,54}, all
  multiples of 18, so g stays 18; both d=8 and d=17 stay
  op-consistent (hand traces in the prereg); the loop has no early
  stop, so it runs all 4 rounds and exits on qq=4 with -4 and
  nothing written. The binary's 4/4, -4, GI-GRAMMAR none match.
- ADV-POISON: (0,43,63) contributes s=63, g'=gcd(18,63)=9,
  candidates {8,2}, d=2 killed by (18,41,0) (9-0=9 != 0), d=8
  survives; gi_induce writes D=8 with the poison fact's object 63
  decoding to (7,7): max_a=max_b=7. The binary's D=8 a=[2,7]
  b=[2,7] matches. The poison is not a licensor for any BUILD fact
  (object 63 != 18), so nbuild/nlic/lic are unchanged.

## Kill-bar audit

- K1: 3/3 runs byte-identical (SHA-256
  ec58b02cea4e3dad0a625a16fc93ec634511268c7761b6dc5999749512fe5dcd).
  PASS.
- K2: ADV-CTRL reproduces the cooperative NEG-AMB result exactly
  (D=8, 1/1 queries, a=[2,6] b=[2,6]). PASS.
- K3: ADV-LIE shows GI-INDUCED-POST 1 with D=17, grammar_written=1,
  no detection signal; the lie is false in the true world and kills
  d=8 while keeping d=17 (hand trace). PASS.
- K4: ADV-WASTE shows exactly 4/4 queries, final -4, nothing
  written; each waste fact is true and non-discriminating (hand
  trace). PASS.
- K5: ADV-POISON shows GI-INDUCED-POST 1 with D=8 and corrupted
  ranges a=[2,7] b=[2,7], no detection signal; the poison fact is
  false in the true world (hand trace). PASS.
- K6: safebin active, `which python3 python` empty, pure Zag, no
  forbidden executable invoked. PASS.
- K7: 0 modes/bridges/handlers (teachers are plain driver
  functions); grammar_inquiry/ untouched (read-only); a_base.zag
  and a_patch.zag byte-identical to the inquiry sources (SHA-256
  a29972ca... and 1c88c5d9...); paper untouched; nothing pushed.
  The adversarial teachers' specific numbers (35, 63, waste pairs)
  are teacher-side world knowledge, like the cooperative teacher's
  lattice knowledge; the LEARNER machinery is unchanged. PASS.

## Metrics

- Cognition lines added: 0 to the learner (a_patch.zag byte copy).
  Driver-only: three adversarial teacher functions, the ADV-CTRL
  teacher copy, the QMAX=4 inquiry loop, reporting, and a
  single-target battery; 0 to base.
- Modes/bridges/handlers: 0. New semantic cases: 0. Base
  modifications: 0.
- Determinism: 3/3 byte-identical runs (SHA-256 ec58b02c...).
- Frozen dirs untouched.

## What this does not claim

- The adversarial teachers are driver-simulated, not separate agents
  or models of human adversaries. The claim is about the
  learner-side trust boundary (what the inquiry machinery verifies
  vs what it trusts), not about teacher fidelity.
- The P(a,b)=a*D+b family remains a researcher-owned world
  assumption, as in all prior grammar work.
- No broad generality claim: three targeted attacks on one
  ambiguity class (NEG-AMB 2-way). A lie that kills ALL candidates
  (the -3 path), lies on other ambiguity classes, multi-round
  adaptive adversaries, and lies via the BUILD channel are not
  tested here.
- The scores are about the mechanism as built. The learner's
  inferences are CORRECT relative to its (adversarially shaped)
  evidence in all three attacks; the vulnerabilities are in trust,
  not in inference.

## Follow-ups (not started; nothing fixed, per instructions)

1. The inquiry channel has no authentication: any taught fact is
   trusted. Hardening directions (answer provenance, cross-checking
   answers against prior evidence weight, decomp-fact op checks)
   are future work, not this worker.
2. The decomp channel (43/44) bypasses all consistency checking;
   extending gi_codec_op_ok or a decomp analog to cover it would
   close the exact path ADV-POISON used.
3. The loop has no usefulness tracking; a learner-side
   non-shrinkage detector with early stop would turn ADV-WASTE
   from BOUND into SURVIVE.
4. A lie that kills all candidates (driving -3 instead of wrong-D)
   would test whether contradiction at least fails safe; untested.
