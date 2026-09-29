# REVISE5 RED TEAM RESULT: H-REVISE5 DOWNGRADED

**Date:** 2026-09-29
**Red team:** H-REVISE5 adversary subagent (independent)
**Branch:** tnn-native-lab
**Target:** H-REVISE5 SURVIVES (62/62) (REVISE5_RESULT.md, revise5.zag)
**Prereg:** PREREG_REVISE5_ADV.md (9f534872b, frozen before attack code)
**Amendment:** PREREG_REVISE5_ADV_AMEND1.md (29baf5eeb, transparent
fixture-math correction, frozen before rerun; see Failures below)
**Attack harness:** revise5_adv.zag (this directory; mechanism lines
1-473 byte-identical to committed revise5.zag, cmp-verified; only
main() replaced)
**Raw evidence:** REVISE5_ADV_RAW.txt (md5
2569e4fcd18c8ee7c792918b7698cc3b, 3/3 byte-identical via cmp)
**Toolchain:** znc 2026.07.0-dev (edition 2026)
**Purity:** Pure Zag. No Python at any stage: no generators,
verifiers, scratch computation, or analysis code. Shell file
utilities (md5sum, cmp, grep, sed, head) only.

## Verdict: H-REVISE5 DOWNGRADED (not killed)

The frozen bars K-RV5-1 through K-RV5-5 stand: the committed
revise5.zag reproduces 62/62 byte-identically (X-RV5-3), and the
source audit is clean (X-RV5-4). What fails is the headline claim.

**Claim as stated (REVISE5_RESULT.md):** "The X-RV4-1 failure class
(confident unique misattribution) is closed by requiring the second
signal."

**Finding:** the class is narrowed, not closed. X-RV5-1 replays the
exact X-RV4-1 fixture (P0=broadcast-last, passing
abc/def/ghi/jkl, fail1=("zqy"->"zzz")) with a second counterexample
fail2=("zab"->"zzz") that shares the incidental byte 'z' at position
0. The gate passes it (corroborate==1), the caller appends the wrong
revision (0,122) with rc==1 and vcount==1, and three held-out queries
that P0 answered correctly are now all mispredicted. Confident
unique misattribution recurs with two counterexamples.

**Narrowed claim (what the evidence supports):** a lone first
failure now waits instead of guessing (K-RV5-1 holds), and genuine
second counterexamples corroborate (K-RV5-5 holds). But the gate
cannot verify that the second signal is informative: a second
counterexample jointly consistent with the wrong hypothesis is
counted as confirmation. The builder's own rationale ("two
counterexamples sharing an incidental byte is genuinely stronger
evidence than one") is false in general; the fixture is a case where
the second counterexample is demonstrably zero additional evidence.

## Attack X-RV5-1: correlated second counterexample (SUCCEEDS)

Method: harness mirrors Phase L exactly (VSL with P0=broadcast-last,
p0 bytes [1,255,255, 3,255,255, 6,0,1], nn0=3; passing set
abc/def/ghi/jkl). Hidden truth H for held-out scoring only: IF
input[2]=='y' THEN broadcast-first ELSE broadcast-last. The
mechanism never sees H.

- CHECK A0 PASS: control. Pre-append, P0 predicts "zbq"->"qqq",
  "zaq"->"qqq", "zqw"->"www": all correct per H.
- CHECK A1 PASS: diagnose_propose on ("zqy"->"zzz") returns 122,
  i.e. unique wrong top (0,122). Raw candidates: pos=0 val=122
  score=1; pos=1 val=113 score=0; pos=2 val=121 score=0.
- CHECK A2 PASS: diagnose_corroborate(VSL, D, pd, 4, ("zab"->"zzz"),
  0, 122) returns 1. The gate emits "CORROBORATE PASS: condition
  fires on fail2, discriminates, current program mispredicts".
  (a) fail2[0]='z'=122 fires. (b) no passing input has 'z' at
  pos 0 (implied by propose). (c) P0 predicts "bbb" != "zzz".
- Caller mimic (Phase C pattern): pextract + discover from fail1
  alone yields P1 nnodes=3 prog=[[1,255,255],[1,255,255],[6,0,1]]
  (node2 = n-n = 0; root 0; i.e. broadcast-first). vs3_revise
  appends (0,122).
- CHECK A3 PASS: rc==1, vcount==1. VSTORE slot1: cond pos=0
  val=122, prog=broadcast-first.
- CHECK A4 PASS (HARM): post-append, "zbq"->[122,122,122]="zzz"
  (H: "qqq"); "zaq"->[122,122,122]="zzz" (H: "qqq");
  "zqw"->[122,122,122]="zzz" (H: "www"). All three mispredicted;
  all three were correct pre-append.
- X-RV5-1 SUCCEEDS: 10/10 named checks pass.

Causal interpretation. The wrong revision (0,122)+P1(broadcast-first)
predicts BOTH counterexamples correctly: "zqy"->"zzz" and
"zab"->"zzz". From the mechanism's view the appended revision is
perfectly consistent with every observation it has. The error is
visible only on held-out inputs neither counterexample covered.
This is the same underdetermination the gate was built to fix,
persisting through the gate: the gate checks that the CURRENT
(pre-revision) program mispredicts fail2, but never checks that
fail2 discriminates the PROPOSED condition from alternatives, and
never checks that the proposed revision predicts fail2 correctly.
A second counterexample that the wrong hypothesis already predicts
is counted as independent confirmation.

Fairness note (preregistered). The mechanism has no access to H;
observations are observations. The H-REVISE5 protocol supplies the
second counterexample directly from the harness ("in a deployment
it arrives via continued monitoring"). A correlated or mislabeled
second observation is inside the threat model of a gate whose
stated purpose is to require a second INDEPENDENT signal. The
attack tests the builder's rationale on its own terms.

## Attack X-RV5-2: condition (b) redundancy (SUCCEEDS, structural)

Structural observation O1 (proven by reading, confirmed at
runtime): corroborate condition (b) ("(p,v) discriminates fail2
from every passing input") uses only (D, pdesc, npass, p, v) and
never fail2 content. Propose's discrimination test runs the
identical loop on the identical (D, pdesc, npass, p, v). In every
protocol-conformant call, (b) is implied by propose's success and
can never independently withhold.

- CHECK B1 PASS: in the X-RV5-1 run, corroborate received propose's
  (0,122) on identical passing data; (b) passed trivially (the
  A2==1 runtime result required it).
- CHECK B2 PASS: off-protocol call with (p,v)=(0,97) ('a' at pos 0;
  propose would reject it since passing "abc" has 'a' at pos 0),
  fail2=("abc"->"zzz"): (a) fires (fail2[0]='a'), (c) would pass
  (P0 "ccc" != "zzz"), but (b) returns 0 via "CORROBORATE FAIL:
  (p,v) does not discriminate fail2 from passing". This proves (b)
  is functional code.
- Source grep: all five corroborate call sites in committed
  revise5.zag (lines 567, 664, 733, 811, 934) receive propose's
  (p,v) on the same passing data. (b) is dead in all of them.

Finding: the advertised three-condition gate is a two-condition
gate (fire + current-program-mispredicts) in every conformant
execution. The corroboration signal is weaker than documented.
Informational alone; it strengthens the X-RV5-1 downgrade by
showing exactly which advertised protection is vacuous.

## Attack X-RV5-3: regression control (PASSES)

Rebuilt the COMMITTED revise5.zag unmodified with znc
2026.07.0-dev; 3 runs. md5 ddcb842dc2f6755d6fd2f90ef6907d65 on all
three (matches the builder's claimed md5 exactly); output contains
"62/62" and "H-REVISE5 SURVIVES"; 3/3 byte-identical via cmp. The
builder's evidence reproduces from source. The frozen bars stand;
the downgrade narrows the claim, it does not relitigate the bars.

## Attack X-RV5-4: source audit (PASSES)

- (a) diagnose_propose (lines 376-421): exactly one score increment
  site ("score=score+1" count == 1). No path to score 2. The R1
  honest-scoring claim holds.
- (b) diagnose_corroborate (lines 434-462): implements exactly the
  frozen R2 spec: (a) fail2[p]==v fire check, (b) discrimination
  loop, (c) vs3_apply mispredict check. No more, no less.
- (c) Mechanism region (lines 1-473, everything before fn main):
  zero test-answer literals (grep for zqy|aqy|xqw|yqw|aqc|cbx|zbq|zaq
  returns no hits). All fixtures live in main().
- (d) UNCORROBORATED path (Phase L, corL==0 branch): no vs3_revise
  call, no store mutation; CHECK L5 (vcount==0) guards it.
- (e) Attack harness mechanism region (lines 1-473) cmp-verified
  byte-identical to committed revise5.zag lines 1-473.

## Failures and corrections (owned)

1. Red-team fixture-math error, caught by the A0 control before
   any verdict. The frozen prereg miscalculated the H expectation
   for "zbq" as "bbb"; broadcast-last of "zbq" is "qqq" (last byte
   'q'). The first harness run's A0 control failed because P0
   correctly predicted "qqq". Corrected transparently in
   PREREG_REVISE5_ADV_AMEND1.md (29baf5eeb), committed BEFORE the
   rerun. The bar's logical content (harm = held-out misprediction
   vs H with P0 correct pre-append) was not weakened; only the
   miscalculated constant was fixed. The void first run is
   disclosed here and no verdict rests on it.
2. No other failures. No Python used. No staged paths beyond the
   five owned files.

## Honest limits of this red team

1. X-RV5-1 uses a harness-supplied second counterexample, as the
   protocol does. It does not show how often correlated second
   observations occur under continued monitoring; it shows the
   gate has no defense when they do.
2. X-RV5-2 is a structural proof plus probes, not a wrong-append
   demonstration; its force is in narrowing the documented gate.
3. The downgrade does not touch K-RV5-1..K-RV5-5: a lone first
   failure still waits (withhold works), and genuine second
   counterexamples still corroborate.
4. Bounded L2+ classification is unaffected; the finding concerns
   the revision protocol's evidence accounting, not the
   architecture class.

## What would repair the downgrade

A gate that measures whether the second counterexample is
informative ABOUT THE PROPOSED CONDITION, not merely a second
misprediction of the current program. Candidates (not
preregistered, offered as directions): require fail2 to be
mispredicted by the proposed revision's competitors; require the
proposed revision to predict fail2 correctly AND a held-out
generated from an alternative condition to be unaffected; or track
provenance/independence of the second observation. Any of these
needs its own prereg with frozen bars.

## Commit lineage

- Target: revise5.zag as committed (mechanism region
  byte-identical in harness).
- Red-team prereg: 9f534872b (single file, before attack code).
- Amendment: 29baf5eeb (fixture-math fix, before rerun).
- This commit: PREREG_REVISE5_ADV.md (already committed),
  PREREG_REVISE5_ADV_AMEND1.md (already committed),
  revise5_adv.zag, REVISE5_ADV_RAW.txt, REVISE5_ADV_RESULT.md
  (this file).
- Builder result under attack: REVISE5_RESULT.md (62/62
  SURVIVES; frozen bars reproduced here in X-RV5-3).

## Pure Zag compliance

Prereg, amendment, harness, compilation (znc 2026.07.0-dev),
execution (3/3 deterministic, md5
2569e4fcd18c8ee7c792918b7698cc3b), and all analysis in Zag and
shell file utilities only. No Python at any stage. No em dashes
in this document.
