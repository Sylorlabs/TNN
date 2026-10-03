# PREREG H-REVISE6 FROZEN

**Date:** 2026-09-29
**Branch:** tnn-native-lab
**Target:** H-REVISE5 DOWNGRADED (red team: REVISE5_ADV_RESULT.md)
**Status:** FROZEN before any implementation. No code written, no tests run.

## Background

H-REVISE5 SURVIVES (62/62) was DOWNGRADED by independent red team.
Two findings, both preregistered attacks succeeding:

**X-RV5-1 (correlated second counterexample):** A second counterexample
fail2=("zab"->"zzz") sharing the incidental byte 'z' at position 0 with
fail1=("zqy"->"zzz") passes the corroborate gate (returns 1). The caller
appends the wrong revision (0,122). Three held-out queries correct
pre-append are all mispredicted post-append. The gate checks that the
current program P0 mispredicts fail2, but never checks that the proposed
revision predicts fail2 correctly, and never checks that fail2
discriminates the proposed condition from alternatives.

**X-RV5-2 (condition (b) redundancy):** Corroborate condition (b)
("(p,v) discriminates fail2 from every passing input") uses only
(D, pdesc, npass, p, v) and never fail2 content. Propose runs the
identical loop on identical inputs. In every protocol-conformant call,
(b) is implied by propose's success and can never independently
withhold. The advertised three-condition gate is a two-condition gate
(fire + P0-mispredicts) in practice.

## Analysis of X-RV5-1 (frozen reasoning)

The wrong revision (0,122)+P1(broadcast-first) predicts BOTH
counterexamples correctly from the mechanism's view. The error is
visible only on held-out inputs under the hidden truth H
(IF input[2]=='y' THEN broadcast-first ELSE broadcast-last), which the
mechanism never sees. fail2's label ("zzz") is adversarially
inconsistent with H (true label "bbb"), but the mechanism is given the
label as ground truth.

**Fundamental limit (frozen):** No gate operating only on
(fail1, fail2, proposed (p,v), P0, P1, passing inputs) can distinguish
X-RV5-1 from a genuine corroboration. In the genuine Phase C case,
fail1=("xab"->"xxx"), fail2=("xqw"->"xxx"), proposed (0,120): fail2
shares the byte 'x' at position 0 with fail1, P1 predicts fail2
correctly, competitors mispredict. The observable signature is
IDENTICAL to X-RV5-1. Any check that withholds on X-RV5-1 also
withholds on genuine Phase C. This is not a fixable bug; it is
underdetermination under adversarial evidence.

**What the repair does:** It raises the bar with a meaningful
revision-correctness check (the old gate never verified the proposed
fix actually works on fail2), fixes the (b) redundancy with a truly
independent condition, and documents the X-RV5-1 residual risk
honestly instead of claiming a false fix.

## Repairs (frozen)

**R1 (revision correctness, addresses X-RV5-1 partially + X-RV5-2):**
New `diagnose_corroborate_v6` takes the discovered P1 program
(`p1:[]u8`, `nn1:i32`) as additional parameters. New condition (b):
the FULL proposed revision ((p,v), P1) must predict fail2 correctly.
Implementation: if fail2[p]==v (condition fires), apply P1 to fail2
via a direct program evaluator (mirroring vs3_apply_one logic on the
p1 bytes) and require the output to equal fail_out2. If the condition
does not fire, (b) fails (a revision that does not even apply to
fail2 cannot be corroborated by it). This check is INDEPENDENT: it can
fail while (a) and (c) pass (condition fires, P0 mispredicts, but P1
is wrong for fail2).

**R2 (honest three-condition gate, fixes X-RV5-2):** The new gate is:
  (a) fail2[p]==v (condition fires on fail2),
  (b) proposed revision ((p,v),P1) predicts fail2 correctly [NEW],
  (c) current program VS mispredicts fail2 (vs3_apply differs from
      fail_out2, or apply fails).
The old redundant (b) (discrimination re-check) is DELETED. Each of
(a), (b), (c) has an independent failure path; none is implied by the
others in protocol-conformant calls. The gate documentation states
this explicitly.

**R3 (protocol reordering):** P1 is now discovered BEFORE corroborate
(previously after), so corroborate can verify the full revision.
All 5 call sites (lines 567, 664, 733, 811, 934 in revise5.zag)
are updated: propose -> discover P1 -> corroborate_v6 (with P1) ->
revise. No other protocol changes.

**R4 (honest documentation):** The source header and result document
state the X-RV5-1 residual risk explicitly: adversarially correlated
or mislabeled second counterexamples cannot be detected by any
observation-only gate; the X-RV5-1 fixture is the concrete regression
example of this limit. The claim "X-RV4-1 failure class is closed" is
NOT reinstated. The narrowed claim stands: a lone first failure waits
(K-RV5-1 holds), genuine second counterexamples corroborate (K-RV5-5
holds), and the revision is now verified to actually fix fail2 before
appending (new).

## Kill bars (frozen)

**K-RV6-1 (new (b) is functional):** Construct a fixture where the
condition fires on fail2 (fail2[p]==v) and P0 mispredicts fail2, but
P1 predicts fail2 INCORRECTLY. The gate must return 0 (withhold).
This proves new condition (b) is independent and can fire when (a)
and (c) pass. (In H-REVISE5, this fixture would have passed the gate
and appended a broken revision.)

**K-RV6-2 (honestly three-condition):** By code reading, each of (a),
(b), (c) in diagnose_corroborate_v6 has a reachable independent
failure path in protocol-conformant calls. Specifically: (a) fails if
fail2[p]!=v; (b) fails if P1(fail2)!=fail_out2 while (a) and (c)
pass; (c) fails if VS already predicts fail2. The old redundant
discrimination loop is absent from the function.

**K-RV6-3 (regression):** All 62/62 H-REVISE5 named checks still pass.
Concretely: Phase C/G/H/I append via propose+corroborate_v6 (C3, G5,
H5, I5 checks pass with cor==1); Phase F withholds (F2: dr2==-1);
Phase J still AMBIGUOUS; Phase K VS3FULL refusal intact; Phase L
withholds with UNCORROBORATED (corL==0, vcount==0). The X-RV5-1
attack fixture is documented as a known residual, not a regression
failure.

**K-RV6-4 (deterministic):** 3/3 runs byte-identical (cmp-verified).

## Non-goals (frozen)

- Detecting adversarially correlated fail2 (X-RV5-1 pattern) is
  explicitly out of scope; documented as fundamental limit.
- No change to diagnose_propose (R1 honest scoring stands).
- No change to capacity (4), AMBIGUOUS, or VS3FULL behavior.
- No new Python. Pure Zag throughout.

## Classification (frozen)

Bounded L2+ revision, not L3. Unchanged from H-REVISE5.

## Commit lineage plan

1. This prereg committed alone (frozen).
2. Implementation: revise6.zag = revise5.zag + R1/R2/R3 (mechanism
   region diff will show only the corroborate replacement, the
   prog evaluator helper, and call-site reorderings).
3. Result commit: revise6.zag + REVISE6_RESULT.md + REVISE6_RAW.txt.
4. Verify prereg is strict ancestor of implementation.
