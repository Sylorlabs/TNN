# REPORT: Independent Adversarial Red Team on the Hardened Inquiry Mechanism

## Verdict: INQUIRY-ADVERSARY-COMPLETE

Per-attack scores against the hardened mechanism: ADV-COHERENT **KILL**,
ADV-SLOWPOISON **KILL**, ADV-SUBWASTE **SURVIVE**, ADV-PROVSPOOF
**SURVIVE**. The hardened mechanism was linked UNMODIFIED
(byte-identical copies, cmp-verified); only the adversarial teachers
and world loop are new code.

## Claim tested

INQUIRY-HARDENED-COMPLETE defeated the three preregistered attacks via
R1 provenance, R2 corroboration gate, R3 decomp decode-and-verify plus
pair-witness, and R4 waste budget, and documented one honest limitation:
a fully coherent liar maintaining a complete alternative world model
could still fabricate a strong elimination plus a strong corroborator,
which no learner-side check can rule out in principle. This worker
tests that limitation plus three further new attacks: (a) the coherent
liar instantiated, (b) a two-stage slow poison assembled below the
per-round suspect threshold, (c) a waste attack that stays under
WASTE_BUDGET=2 by alternating answer types, (d) provenance spoofing
(can inquiry answers be marked as taught?).

## Method

h_base_nomain.zag and h_patch.zag copied byte-identical from
inquiry_hardened/ (cmp clean; SHA-256 b63cce04... and d67f909e...).
New adv_driver.zag holds the four adversarial teachers (plain
functions), the NEG-AMB teaching snippet and reporting copied verbatim
from h_driver.zag, and the hardened inquiry loop. Assembled to
adv_full.zag, compiled with the pinned znc to adv_bin. Three runs,
byte-identical (SHA-256
8159122b40c4af251450c54f4393809d57672e45a98740086cc01bec1d0eb4d1).

## Results

### ADV-COHERENT (wid 20): KILL

```
GI-INDUCED -4
GI-INQUIRY request=discriminating-example ncands=2 cands=17,8 g=18
GI-ADV-COHERENT-ANSWER P=16 op=42 t=0
GI-ANSWER-ACCEPT s=16 r=42 o=0 prov=inquiry
GI-QUERIES issued=1 answered=1 verify=0/0 waste=0
GI-INDUCED-POST 1
GI-GRAMMAR nbuild=2 nlic=2 lic=43,44 D=17 a=[1,3] b=[1,3] maxlinks=1
GI-PROVENANCE taught=14 inquiry=1
GI-ADV-CHECK coherent-fact-present=1
GI-ADV-BATTERY
GI-ADV-B 0 ans=18 class=1
GI-ADV-B-VALID 1/1
```

The liar answers (16,42,0): a STRONG kill of the true d=8 (16 mod 8 =
0, degenerate pair, gi_strong_kill=1) that is a TRUE fact in the liar's
coherent D=17 world (16 decodes to (0,16), 0/16=0) and consistent with
every taught fact under d=17. The learner's corroboration gate never
fires: there is no GI-VERIFY-REQUEST, no verification round, no
corroborator needed, no GI-LIE-SUSPECT. Re-induction finds the
consistent set {17} and writes D=17 a=[1,3] b=[1,3]: wrong in the true
world (D=8 a=[2,6] b=[2,6]), trusted silently. The kill is total: even
the downstream single-target battery validates the wrong grammar
(GI-ADV-B-VALID 1/1), because pair 18 decodes to (1,1) under D=17 and
the taught eval fact (18,41,0) confirms it.

Hand verification: gi_fact_ok(8,16,42,0)=0 (bb=0) kills d=8 strongly;
gi_fact_ok(17,16,42,0)=1 (0/16=0) keeps d=17; divisors d=1,2,5 already
excluded by the taught stream; nc=1 gives 17; literal ranges from the
taught 43/44 facts decode under 17 as 18->(1,1), 36->(2,2), 54->(3,3).
Binary matches.

Scoring: KILL by the rubric (wrong grammar written and trusted, no
detection signal). This is the documented limitation made concrete:
the R2 gate only gates WEAK kills, so a liar that never needs a weak
kill walks through the strong-kill fast path untouched. The liar's
family {(16,42,0),(32,42,0),(48,42,0),...} is infinite, so the attack
generalizes to any re-query.

### ADV-SLOWPOISON (wid 21): KILL

```
GI-INDUCED -4
GI-INQUIRY request=discriminating-example ncands=2 cands=17,8 g=18
GI-ADV-SLOWPOISON-ANSWER P=35 op=42 t=2
GI-VERIFY-REQUEST d=8 reason=weak-elimination s=35 r=42 o=2
GI-ADV-SLOWPOISON-VERIFY P=16 op=42 t=0
GI-VERIFY-PASS d=8
GI-QUERIES issued=1 answered=1 verify=1/1 waste=0
GI-INDUCED-POST 1
GI-GRAMMAR nbuild=2 nlic=2 lic=43,44 D=17 a=[1,3] b=[1,3] maxlinks=1
GI-PROVENANCE taught=14 inquiry=2
GI-ADV-CHECK lie-present=1
GI-ADV-CHECK corroborator-present=1
```

Round 0: the weak lie (35,42,2) triggers GI-VERIFY-REQUEST d=8. On the
verification re-query the liar answers the coherent corroborator
(16,42,0). All six gi_inquiry_verify checks pass: B is new, an eval
fact, differs from A, kills d=8 (gi_fact_ok=0), kills it STRONGLY
(8|16), and keeps every candidate A keeps (d=17: A reads (2,1), 2/1=2;
B reads (0,16), 0/16=0). GI-VERIFY-PASS is emitted, BOTH false facts
enter W with prov=2, re-induction finds {17}, and D=17 is written with
no GI-LIE-SUSPECT at any point. verify=1/1, inquiry=2.

Hand verification: the six checks were traced against the committed
gi_inquiry_verify source (see PREREG.md); each holds exactly as the
binary shows. Binary matches.

Scoring: KILL. This is the sharper kill: it goes THROUGH the
verification round the R2 repair built to stop the preregistered liar,
and passes it, because every check in the round (new, eval, different,
strong kill of d_weak, keeps A's kept set) is satisfiable by facts that
are false in the true world but coherent in the liar's alternative
model. The corruption is assembled below the per-round suspect
threshold: no single answer trips a detection.

### ADV-SUBWASTE (wid 22): SURVIVE

```
GI-ADV-SUBWASTE-ANSWER P=20 op=41 t=-2
GI-ANSWER-ACCEPT s=20 r=41 o=-2 prov=inquiry
GI-WASTE-COUNT 1/2
GI-ADV-SUBWASTE-ANSWER P=35 op=42 t=2
GI-VERIFY-REQUEST d=8 reason=weak-elimination s=35 r=42 o=2
GI-ADV-SUBWASTE-REFUSE-VERIFY
GI-TEACHER-REFUSED
GI-QUERIES issued=2 answered=2 verify=1/0 waste=1
GI-INDUCED-POST -4
GI-GRAMMAR none
GI-PROVENANCE taught=14 inquiry=1
```

The attacker stays strictly under budget (waste=1, no GI-WASTE-STOP)
by alternating a harmless true fact with a weak lie plus refusal on
the verification re-query. But the sub-budget path self-terminates:
refusal stops the loop, fail-closed -4 holds, nothing is written, and
the lie never enters W. The attacker burns at most 2 queries and
achieves nothing.

Why alternation cannot do better (recorded in the prereg, confirmed by
the run): with nc=2 every continued round must increment waste. An
accepted answer that strictly shrinks the candidate count resolves the
ambiguity (nc=1) and ends inquiry; any non-shrinking accept increments
waste; duplicates increment waste; rejections and suspect detections
stop the loop. There is no answer sequence that burns a third query
with waste below 2. The waste budget is airtight against alternation.

Scoring: SURVIVE (fail-closed, no corruption, no detection needed).

### ADV-PROVSPOOF (wid 23): SURVIVE

```
GI-ADV-PROVSPOOF-ANSWER s=18 r=41 o=0 dup-of-taught
GI-ANSWER-DUP s=18 r=41 o=0
GI-WASTE-COUNT 1/2
GI-ADV-PROVSPOOF-ANSWER s=20 r=41 o=-2 new
GI-ANSWER-ACCEPT s=20 r=41 o=-2 prov=inquiry
GI-WASTE-COUNT 2/2
GI-WASTE-STOP
GI-PROVENANCE taught=14 inquiry=1
GI-PROVSPOOF-CHECK mismatches=0 taught_ok=14 inquiry_ok=1
```

The duplicate-of-taught bid is rejected outright (GI-ANSWER-DUP, never
added, counted as waste); the new fact is accepted with prov=2
(inquiry), and the waste budget stops the loop at 2. The driver-side
spoof audit walks every live type-1 fact: all 14 prov=1 facts are
exactly the taught triples, the single prov=2 fact is the
teacher-supplied triple, mismatches=0. Within the threat model the
teacher has no write path to the prov array: gi_prov_mark_taught runs
once after the fixed teaching, and gi_inquiry_accept is the only entry
point, marking prov=2 on accept and adding nothing on reject.

Scoring: SURVIVE (provenance boundary holds; spoof fails).

## Kill-bar audit

- K1: 3/3 runs byte-identical (SHA-256
  8159122b40c4af251450c54f4393809d57672e45a98740086cc01bec1d0eb4d1).
  PASS.
- K2: ADV-COHERENT: GI-ANSWER-ACCEPT with verify=0/0 and no
  GI-VERIFY-REQUEST; GI-INDUCED-POST 1; GI-GRAMMAR D=17; no suspect
  signals. Scored KILL by the rubric. PASS (prediction matched).
- K3: ADV-SLOWPOISON: GI-VERIFY-REQUEST then GI-VERIFY-PASS; no
  GI-LIE-SUSPECT; GI-INDUCED-POST 1; GI-GRAMMAR D=17. Scored KILL.
  PASS (prediction matched).
- K4: ADV-SUBWASTE: issued=2, waste=1 (no GI-WASTE-STOP);
  GI-INDUCED-POST -4; GI-GRAMMAR none. Scored SURVIVE. PASS.
- K5: ADV-PROVSPOOF: GI-PROVSPOOF-CHECK mismatches=0; taught=14;
  GI-INDUCED-POST -4; GI-GRAMMAR none. Scored SURVIVE. PASS.
- K6: toolchain guard: safebin active, `which python3 python` empty at
  start and rechecked after the runs; pure Zag; no forbidden executable
  invoked. PASS.
- K7: 0 modes/bridges/handlers (teachers and driver are plain
  functions); hardened sources byte-identical (cmp clean against
  inquiry_hardened/); the hardened mechanism NOT modified; paper
  untouched; nothing pushed; prereg committed (b09d2c62b) before the
  implementation commit. PASS.
- K8: no em/en dashes in prose (scanned). PASS.

## Metrics

- Cognition lines added to the learner: 0 (hardened mechanism
  unmodified). Adversary driver: ~330 lines of new Zag (4 teachers,
  world loop, spoof audit); teaching/reporting/battery snippets copied
  verbatim from h_driver.zag.
- New hardcoded semantic cases: 0. Modes/bridges/handlers: 0.
- Determinism: 3/3 byte-identical runs.
- Query spend: COHERENT 1, SLOWPOISON 1+1 verify, SUBWASTE 2,
  PROVSPOOF 2.

## What this does not claim

- The two KILLs succeed only because the liar's alternative model
  (D=17) is genuinely consistent with the taught stream; the ambiguity
  {8,17} is real, not a learner bug. The kills demonstrate the
  documented limitation; they do not refute R1-R4 against the
  preregistered attacks, which still hold.
- The adversarial teachers are driver-simulated, as in prior work.
- The P(a,b)=a*D+b family remains a researcher-owned world assumption.
- No broad generality claim: four targeted attacks on NEG-AMB.

## Follow-ups (not started)

1. The strong-kill fast path is now the primary unverified trust path:
   any (P,42,t) with d|P and degenerate decode is trusted outright. A
   second-order check on strong kills (e.g. pair-witness for the pair
   object, as R3 does for decomp facts) would force the coherent liar
   to also fabricate taught history, raising the bar further. Note the
   asymmetry the runs expose: decomp answers need pair-witness but
   strong eval kills need none.
2. The verification round's checks are necessary but not sufficient;
   closing the coherent-liar gap in principle requires grounding the
   corroborator outside the liar's channel (independent evidence the
   liar cannot fabricate), which the current single-teacher protocol
   cannot provide.
3. The downstream battery validates the wrong grammar (1/1 on D=17):
   a battery that cannot distinguish the true world from a coherent
   alternative adds no defense in depth against these kills.
