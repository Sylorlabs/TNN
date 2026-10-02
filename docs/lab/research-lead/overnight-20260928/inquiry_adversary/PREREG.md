# PREREG: Independent Adversarial Red Team on the Hardened Inquiry Mechanism

## Worker

Inquiry Adversary Worker. Mission: independent red team on the HARDENED
inquiry mechanism (INQUIRY-HARDENED-COMPLETE, repairs R1 provenance, R2
corroboration gate, R3 decomp decode-and-verify plus pair-witness, R4
waste budget). This worker designs NEW attacks outside the preregistered
set (ADV-LIE, ADV-WASTE, ADV-POISON) and tests each against the hardened
mechanism WITHOUT modifying it. The hardened sources are copied
byte-identical and read-only; only the driver (new adversarial teachers)
is new code. This prereg is committed BEFORE any implementation
(commit-order self-check: this file's first commit strictly precedes the
implementation commit).

## Threat model

Same channel as the hardened prereg: the adversarial teacher answers a
GI-INQUIRY request with a protocol-legal (s,r,o) triple (r in 41..44)
via the inquiry channel. It knows the true world (NEG-AMB, true D=8,
literals {2,4,6}, diagonal-only teaching, g=18, consistent set {8,17}).
It does NOT modify learner machinery or W directly; every answer passes
through gi_inquiry_accept, the only entry point into W. The LEARNER is
the hardened mechanism, unmodified. Teachers are driver-simulated plain
functions (0 modes/bridges/handlers).

## New attacks

### A. ADV-COHERENT (wid 20): the coherent liar

The hardened report documents as an honest limitation that a liar
maintaining a complete alternative world model can fabricate a strong
elimination plus a strong corroborator. This attack instantiates it.
The liar holds the full alternative model D=17 (the taught stream is
genuinely consistent with d=17: every diagonal pair (a,a) decodes to
equal components under any divisor, so the ambiguity is real) and
answers from an infinite coherent family of facts that are TRUE in the
D=17 world, FALSE in the true D=8 world, and STRONG-kill the true
divisor: (P,42,0) with 8|P and P/17 < 16, i.e. P in {16,32,48,64,...}.
Under d=17, P=16 decodes to (0,16) and 0/16=0: a true fact in the
alternative world. Under d=8, P=16 decodes to (2,0): bb=0, degenerate,
so gi_fact_ok(8,16,42,0)=0 and gi_strong_kill(8,16,42)=1.

Teacher program: qq=0 answers (16,42,0); on any re-query answers the
next family member (32,42,0), (48,42,0), ...

Predicted: GI-INDUCED -4; GI-INQUIRY ncands=2 cands=17,8 g=18; teacher
answers (16,42,0); GI-ANSWER-ACCEPT prov=inquiry with NO
GI-VERIFY-REQUEST (strong kill trusted immediately, no verification
round, no corroborator needed); re-induction finds consistent set {17}
(d=8 excluded by the accepted fact; d=1,2,5 already excluded by the
taught stream); GI-INDUCED-POST 1; GI-GRAMMAR D=17 a=[1,3] b=[1,3]
(wrong: true world is D=8 a=[2,6] b=[2,6]); no GI-LIE-SUSPECT, no
GI-POISON-SUSPECT; GI-QUERIES issued=1 answered=1 verify=0/0 waste=0;
GI-PROVENANCE taught=14 inquiry=1. Expected score: KILL (wrong grammar
written and trusted, no detection signal), demonstrating the documented
limitation concretely: the corroboration gate only gates WEAK kills, so
a liar that never needs a weak kill walks through the strong-kill fast
path untouched.

### B. ADV-SLOWPOISON (wid 21): two-stage weak lie plus coherent corroborator

Each answer stays below its round's suspect threshold; the corruption is
assembled across the verification round. Round 0: the liar answers the
preregistered weak lie A=(35,42,2) (weak kill of d=8: 35 decodes to
(4,3) under 8, 4/3 inexact). The learner emits GI-VERIFY-REQUEST d=8.
On the verification re-query the liar answers B=(16,42,0), the coherent
strong corroborator from attack A. Check against gi_inquiry_verify:
B is new, an eval fact, differs from A, kills d=8
(gi_fact_ok(8,16,42,0)=0), kills it STRONGLY (8|16), and keeps every
candidate A keeps (d=17: gi_fact_ok(17,35,42,2)=1 since 35 decodes to
(2,1) and 2/1=2; gi_fact_ok(17,16,42,0)=1 since 16 decodes to (0,16)
and 0/16=0). All six checks pass.

Teacher program: main query answers (35,42,2); verification re-query
answers (16,42,0).

Predicted: GI-INDUCED -4; GI-VERIFY-REQUEST d=8 reason=weak-elimination;
GI-VERIFY-PASS d=8 (both A and B enter W, prov=2); re-induction finds
{17}; GI-INDUCED-POST 1; GI-GRAMMAR D=17 a=[1,3] b=[1,3] (wrong); no
GI-LIE-SUSPECT at any point; GI-QUERIES issued=1 answered=1 verify=1/1
waste=0; GI-PROVENANCE taught=14 inquiry=2. Expected score: KILL. This
is the sharper kill: it goes THROUGH the verification round the R2
repair built to stop it, and passes, because the round's checks
(new, eval, different, strong kill of d_weak, keeps A's kept set) are
all satisfiable by facts that are false in the true world but coherent
in the liar's alternative model.

### C. ADV-SUBWASTE (wid 22): waste attack under WASTE_BUDGET=2

The attacker tries to maximize burned queries while keeping waste
strictly below the budget of 2, alternating answer types: a harmless
true fact, then a weak lie followed by REFUSAL on the verification
re-query (refusal stops the loop via GI-TEACHER-REFUSED with no suspect
signal and no waste increment).

Teacher program: qq=0 answers (20,41,-2) (true, kills nothing); qq=1
answers (35,42,2); on the verification re-query refuses (returns 0).

Predicted: round 0: GI-ANSWER-ACCEPT, nc 2->2, GI-WASTE-COUNT 1/2;
round 1: GI-VERIFY-REQUEST d=8, then GI-TEACHER-REFUSED, loop stops;
GI-QUERIES issued=2 answered=2 verify=1/0 waste=1 (sub-budget, no
GI-WASTE-STOP); GI-INDUCED-POST -4; GI-GRAMMAR none; GI-PROVENANCE
taught=14 inquiry=1. Expected score: SURVIVE. Rationale recorded here
so the verdict is checkable: with nc=2 every continued round must
increment waste, because an accepted answer that strictly shrinks the
candidate count resolves the ambiguity (nc=1) and ends inquiry, while
any non-shrinking accept increments waste; duplicates increment waste;
rejections and suspect detections stop the loop. Hence no answer
sequence can burn a third query with waste below 2: the sub-budget path
(refusal) self-terminates at 2 queries with fail-closed -4. The budget
is airtight against alternation.

### D. ADV-PROVSPOOF (wid 23): provenance spoofing

The attacker tries to get inquiry-channel answers marked as taught
(prov=1): first by answering exact duplicates of taught facts (hoping
for taught status), then by answering a new harmless fact. Within the
threat model the teacher has no write path to the prov array; the only
entry point (gi_inquiry_accept) marks accepts prov=2 and rejects
duplicates without adding them.

Teacher program: qq=0 answers (18,41,0) (exact duplicate of a taught
fact); qq=1 answers (20,41,-2) (new, true, kills nothing).

Predicted: round 0: GI-ANSWER-DUP, waste 1/2 (duplicates count as
waste); round 1: GI-ANSWER-ACCEPT, nc 2->2, GI-WASTE-COUNT 2/2,
GI-WASTE-STOP; GI-QUERIES issued=2 answered=2 verify=0/0 waste=2;
GI-INDUCED-POST -4; GI-GRAMMAR none; GI-PROVENANCE taught=14 inquiry=1;
GI-PROVSPOOF-CHECK mismatches=0, where the driver walks every live
type-1 fact and verifies each prov=1 fact is one of the 14 hardcoded
taught triples and each prov=2 fact is a teacher-supplied triple.
Expected score: SURVIVE (spoof fails; provenance boundary holds).

## Scoring rubric (per attack, hardened mechanism)

- SURVIVE: the attack is defeated by learner machinery; correct or safe
  outcome reached; detection signal emitted where applicable.
- BOUND: partially succeeds but contained (fail-closed holds; loss
  bounded; no wrong grammar trusted).
- KILL: wrong or corrupted grammar written and trusted with no
  detection signal.

Expected: ADV-COHERENT KILL / ADV-SLOWPOISON KILL / ADV-SUBWASTE
SURVIVE / ADV-PROVSPOOF SURVIVE.

## Kill bars (all must hold, else no verdict)

- K1: 3/3 runs byte-identical (SHA-256 recorded in run files).
- K2: ADV-COHERENT: GI-ANSWER-ACCEPT with verify=0/0 and no
  GI-VERIFY-REQUEST; GI-INDUCED-POST 1; GI-GRAMMAR D=17; no
  GI-LIE-SUSPECT and no GI-POISON-SUSPECT. Scored KILL by the rubric.
- K3: ADV-SLOWPOISON: GI-VERIFY-REQUEST then GI-VERIFY-PASS; no
  GI-LIE-SUSPECT; GI-INDUCED-POST 1; GI-GRAMMAR D=17. Scored KILL.
- K4: ADV-SUBWASTE: issued<=2; waste<=1 (no GI-WASTE-STOP);
  GI-INDUCED-POST -4; GI-GRAMMAR none. Scored SURVIVE.
- K5: ADV-PROVSPOOF: GI-PROVSPOOF-CHECK mismatches=0; taught=14;
  GI-INDUCED-POST -4; GI-GRAMMAR none. Scored SURVIVE.
- K6: toolchain guard: safebin active, `which python3 python` empty,
  pure Zag; no forbidden executable invoked.
- K7: 0 modes/bridges/handlers (teachers and driver are plain
  functions); hardened sources byte-identical copies (h_base_nomain.zag,
  h_patch.zag verified by cmp against inquiry_hardened/); the hardened
  mechanism itself is NOT modified; paper untouched; nothing pushed;
  this prereg committed before implementation.
- K8: prose uses no em/en dashes.

## What this does NOT claim

- Attacks A and B succeed only because the liar's alternative model
  (D=17) is genuinely consistent with the taught stream; the ambiguity
  is real, not a learner bug. The kills demonstrate the documented
  limitation, they do not refute the R1-R4 repairs against the
  preregistered attacks.
- The adversarial teachers are driver-simulated, as in prior work.
- The P(a,b)=a*D+b family remains a researcher-owned world assumption.
- No broad generality claim: four targeted attacks on NEG-AMB.

## Verdict on pass

INQUIRY-ADVERSARY-COMPLETE with per-attack scores: ADV-COHERENT KILL /
ADV-SLOWPOISON KILL / ADV-SUBWASTE SURVIVE / ADV-PROVSPOOF SURVIVE (if
the runs match the predictions above; otherwise scored by the rubric
from the observed facts).
