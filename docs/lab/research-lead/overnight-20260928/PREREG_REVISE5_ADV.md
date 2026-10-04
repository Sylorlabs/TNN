# PREREG H-REVISE5 RED TEAM (ADV)

**Date:** 2026-09-29
**Branch:** tnn-native-lab
**Target:** H-REVISE5 SURVIVES (62/62) (REVISE5_RESULT.md, revise5.zag)
**Status:** FROZEN. Committed BEFORE any attack code is written or
executed. If a frozen bar below breaks during implementation, amend
transparently and re-freeze; bars are never weakened to force a pass.

## Mission

Assume the H-REVISE5 repair claim is false. Attack it. The claim:
"The X-RV4-1 failure class (confident unique misattribution) is
closed by requiring the second signal (corroboration)."

## Background facts (verified by reading committed revise5.zag)

- `diagnose_propose` (line 376): single binary signal (v in
  fail_out). Returns best_p*1000+best_v, -2 on tie, -1 if none.
- `diagnose_corroborate` (line 434): returns 1 iff (a) fail2[p]==v,
  (b) (p,v) discriminates fail2 from every passing input
  (bounds-respecting), (c) current program VS mispredicts fail2.
- Caller appends ONLY on propose>=0 AND corroborate==1; else
  UNCORROBORATED (-3), store unchanged.
- Structural observation O1: corroborate condition (b) uses only
  (D, pdesc, npass, p, v) and never fail2 content. Propose's
  discrimination test uses the identical loop on the identical
  (D, pdesc, npass, p, v). Hence in every protocol-conformant call
  (corroborate receiving propose's (p,v) on the same passing data),
  (b) is implied by propose's success and can never independently
  withhold. The advertised three-condition gate is a two-condition
  gate in every conformant execution.
- Structural observation O2: the gate checks that the CURRENT
  (pre-revision) program mispredicts fail2 (condition c), but never
  checks that fail2 discriminates the PROPOSED condition from
  alternatives, and never checks that the proposed revision would
  predict fail2 correctly. A second counterexample fully consistent
  with the wrong hypothesis passes the gate.

## Attack X-RV5-1: correlated second counterexample

Fixture mirrors Phase L exactly: P0 = broadcast-last
(p0 bytes [1,255,255, 3,255,255, 6,0,1], nn0=3), passing set
D = {"abc","def","ghi","jkl"} (4 inputs).

- fail1 = ("zqy" -> "zzz"). Hidden truth H for held-out scoring:
  IF input[2]=='y' THEN broadcast-first ELSE broadcast-last.
- CHECK A1: diagnose_propose(D, pd, 4, fail1, "zzz") MUST equal 122,
  i.e. unique wrong top (0,122). Rationale: p=0 'z' discriminates
  (no passing input has 'z' at pos 0) and scores 1 ('z' in "zzz");
  p=1 'q' and p=2 'y' discriminate but score 0. If propose != 122
  the fixture is VOID and X-RV5-1 cannot run.
- fail2 = ("zab" -> "zzz"): shares the incidental byte 'z' at pos 0
  with fail1. (a) fail2[0]='z'=122 fires. (b) implied by propose
  (O1). (c) P0 predicts "bbb" != "zzz", mispredicts. Predicted
  corroborate == 1.
- CHECK A2: diagnose_corroborate(VS, D, pd, 4, fail2, "zzz", 0, 122)
  is recorded; the mechanism's design predicts 1.
- Caller mimic: P1 = discover from fail1 alone (same caller pattern
  as Phase C); rc = vs3_revise(VS, 0, 122, p1, nn1).
- CHECK A3: rc==1 and vcount==1 (wrong revision appended).
- Held-out harm vs H: "zbq" -> H says "bbb"; "zaq" -> H says "qqq";
  "zqw" -> H says "www". Control: pre-append, P0 predicts all three
  correctly.
- CHECK A4 (HARM): at least one held-out is mispredicted
  post-append while P0 predicted all three correctly pre-append.

KILL CRITERION X-RV5-1: if A1==122 AND corroborate==1 AND rc==1
AND HARM, then X-RV5-1 SUCCEEDS. The gate is fooled by a second
counterexample that is jointly consistent with the wrong hypothesis
(the wrong revision predicts both counterexamples correctly, so the
second provides zero discriminating evidence yet counts as
confirmation). The "failure class closed" claim is false; the class
is narrowed, not closed. Verdict contribution: DOWNGRADED.
If corroborate==0 or rc!=1 or no HARM, X-RV5-1 FAILS (gate held).

Note on fairness: the mechanism has no access to H; observations
are observations. The harness protocol supplies the second
counterexample directly (prereg honest limit 1: "in a deployment it
arrives via continued monitoring"). A mislabeled or correlated
second observation is within the threat model of a revision gate
whose purpose is to require a second INDEPENDENT signal. The
builder's own rationale ("two counterexamples sharing an incidental
byte is genuinely stronger evidence than one") is what this attack
tests; the fixture is a case where the second counterexample is
demonstrably zero additional evidence.

## Attack X-RV5-2: condition (b) redundancy (structural)

- Probe B1 (in-protocol): in the X-RV5-1 execution, corroborate is
  called with propose's (0,122) on identical (D, pd, npass). By O1,
  the (b) sub-check must pass trivially. Recorded as the runtime
  confirmation of the structural proof.
- Probe B2 (off-protocol, proving (b) is live code): call
  diagnose_corroborate directly with (p,v)=(0,97) ('a' at pos 0;
  'a' IS at pos 0 of passing "abc", so propose would reject it),
  fail2=("abc" -> "zzz"): (a) fail2[0]='a'=97 fires; (b) must
  return 0 via the discrimination check. This proves (b) is
  functional code that is dead in-protocol.
- Also grep the committed source: diagnose_corroborate has no
  caller other than the propose-conformant call sites.

KILL CRITERION X-RV5-2: if B1 confirms (b) passes trivially
in-protocol AND B2 confirms (b) fires off-protocol, then X-RV5-2
SUCCEEDS as a structural finding: the three-condition gate is a
two-condition gate in every conformant execution; the corroboration
signal is weaker than documented. Contribution: supports
DOWNGRADE (informational alone).

## Attack X-RV5-3: regression control

Rebuild the COMMITTED revise5.zag unmodified with znc
2026.07.0-dev. Run 3 times. Expected: md5
ddcb842dc2f6755d6fd2f90ef6907d65, output contains "62/62" and
"H-REVISE5 SURVIVES". If mismatch, investigate and report; a
reproducibility failure is a finding in its own right.

## Attack X-RV5-4: source audit

- (a) diagnose_propose has exactly one score increment site; no
  path to score 2 (grep "score=score+1" count == 1 in the function).
- (b) diagnose_corroborate implements exactly (a)(b)(c) per the
  frozen R2 spec.
- (c) No test-answer literals in the mechanism region (lines 1-473,
  everything before fn main): grep for zqy|aqy|xqw|yqw|aqc|cbx|zbq|zaq
  in lines 1-473 must return zero hits.
- (d) The UNCORROBORATED path in Phase L performs no store
  mutation (no vs3_revise call on the corL==0 path).
- (e) Attack harness mechanism region (lines 1-473) byte-identical
  to committed revise5.zag lines 1-473 (cmp).

## Verdict rule

- X-RV5-1 SUCCEEDS -> H-REVISE5 DOWNGRADED (not killed): the
  X-RV4-1 failure class is narrowed, not closed; corroboration
  cannot verify the second signal is informative.
- X-RV5-2 SUCCEEDS -> structural narrowing, supports the
  downgrade; informational on its own.
- X-RV5-3 / X-RV5-4 are controls; failures become findings.

## Method

Pure Zag. No Python at any stage: no generators, verifiers, analysis
scripts, or scratch computation. Shell file utilities (md5sum, cmp,
grep, head) only. Toolchain znc 2026.07.0-dev (edition 2026).
Attack harness: committed revise5.zag lines 1-473 copied verbatim
(cmp-verified), only main() replaced. New files:
PREREG_REVISE5_ADV.md (this file), revise5_adv.zag,
REVISE5_ADV_RAW.txt, REVISE5_ADV_RESULT.md. Only owned paths
staged. No em dashes in loop documents.
