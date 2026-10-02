# H-REVISE6 RESULT

**Date:** 2026-09-29
**Branch:** tnn-native-lab
**Prereg:** PREREG_REVISE6.md, frozen as commit 1743ca053, strict ancestor of implementation.
**Verdict:** H-REVISE6 SURVIVES (66/66 checks, 3/3 byte-identical runs).

## Problem

H-REVISE5 DOWNGRADED by independent red team (REVISE5_ADV_RESULT.md).
Two findings:

**X-RV5-1:** Correlated second counterexample fail2=("zab"->"zzz")
sharing incidental byte 'z' at position 0 with fail1=("zqy"->"zzz")
passes the corroborate gate (returns 1). Wrong revision (0,122)
appended. Three held-out queries correct pre-append all mispredict
post-append. The gate verified P0 mispredicts fail2 but never verified
the proposed revision predicts fail2 correctly.

**X-RV5-2:** Corroborate condition (b) ("(p,v) discriminates fail2 from
passing") was redundant. It used only (D, pdesc, npass, p, v), never
fail2 content. diagnose_propose ran the identical loop on identical
inputs. In all 5 protocol-conformant call sites, (b) was implied by
propose's success. The advertised three-condition gate was effectively
two-condition.

## Frozen analysis of X-RV5-1 (from prereg)

The wrong revision (0,122)+P1(broadcast-first) predicts BOTH
counterexamples correctly from the mechanism's view. The error is
visible only on held-out inputs under hidden truth H
(IF input[2]=='y' THEN broadcast-first ELSE broadcast-last), which the
mechanism never sees. fail2's label ("zzz") is adversarially
inconsistent with H (true label "bbb"), but the mechanism receives the
label as ground truth.

**Fundamental limit (frozen before implementation):** No gate operating
only on (fail1, fail2, proposed (p,v), P0, P1, passing inputs) can
distinguish X-RV5-1 from genuine Phase C corroboration. In Phase C,
fail1=("xab"->"xxx"), fail2=("xqw"->"xxx"), proposed (0,120): fail2
shares byte 'x' at position 0 with fail1, P1 predicts fail2 correctly,
competitors mispredict. The observable signature is IDENTICAL to
X-RV5-1. Any check withholding on X-RV5-1 also withholds on genuine
Phase C. This is underdetermination under adversarial evidence, not a
fixable bug.

**Repair scope:** Raise the bar with a revision-correctness check (the
old gate never verified the fix works on fail2), replace the redundant
(b) with a truly independent condition, document the X-RV5-1 residual
risk honestly. The "X-RV4-1 class is closed" claim is NOT reinstated.

## Repairs implemented

**R1 (revision correctness):** New `diagnose_corroborate_v6` takes the
discovered P1 program (p1:[]u8, nn1:i32). New condition (b): the FULL
proposed revision ((p,v),P1) must predict fail2 correctly. If the
condition fires, P1 is applied to fail2 via `prog_apply_direct` (a
direct evaluator mirroring vs3_apply_one logic on p1 bytes); output
must equal fail_out2. If the condition does not fire, (b) fails.

**R2 (honest three-condition gate):** (a) fail2[p]==v; (b) revision
predicts fail2 correctly [NEW]; (c) current VS mispredicts fail2. The
old redundant discrimination loop is DELETED. Each condition has an
independent failure path.

**R3 (protocol reordering):** P1 discovered BEFORE corroborate (was
after) at all 5 call sites, so the gate can verify the full revision.

**R4 (documentation):** X-RV5-1 residual risk stated explicitly in
source header and here.

## Frozen kill bars and results

**K-RV6-1 (new (b) functional):** PASS. New Phase M constructs:
fail1=("xab"->"xxx"), P1=broadcast-first, proposed (0,120),
fail2=("xqw"->"qqq"). (a) fires ('x'==120). (c) P0 predicts "www",
mispredicts. (b) P1("xqw")="xxx" != "qqq", FAILS. Gate returns 0.
Output: "CORROBORATE FAIL: proposed revision does not predict fail2
correctly". CHECK M1 PASS, M2 (vcount==0) PASS. In H-REVISE5, the old
gate would have returned 1 here ((a) fires, old-(b) redundant given
passing inputs lack 'x' at pos 0, (c) mispredicts), appending a broken
revision.

**K-RV6-2 (honestly three-condition):** PASS by code reading.
(a) fails if fail2[p]!=v (Phase L: "aqy"[0]='a'!=122, returns 0).
(b) fails if P1(fail2)!=fail_out2 while (a),(c) pass (Phase M,
returns 0). (c) fails if VS predicts fail2 (reachable: if fail2 were
already handled). No condition implies another in conformant calls.
The old discrimination loop is absent from diagnose_corroborate_v6.

**K-RV6-3 (regression):** PASS. 66/66 checks. All H-REVISE5 behaviors
preserved: Phase C/G/H/I append via propose+corroborate_v6
(C3,G5,H5,I5 cor==1); Phase F withholds (F2 dr2==-1); Phase J
AMBIGUOUS; Phase K VS3FULL refusal; Phase L UNCORROBORATED withhold
(corL==0, vcount==0). The 4 extra checks vs 62/62 are: Phase L P1
discover (1), Phase M M1/M2 (2), plus one structural from reorder.
X-RV5-1 attack fixture documented as known residual, not a failure.

**K-RV6-4 (deterministic):** PASS. 3/3 runs byte-identical
(cmp-verified).

## Classification

Bounded L2+ revision, not L3. Unchanged.

## Boundaries and limits

1. X-RV5-1 pattern (adversarially correlated/mislabeled fail2) is NOT
   detected. Documented as fundamental limit, not a bug.
2. The gate assumes fail2's label is trustworthy. A mislabeled fail2
   that happens to be consistent with the wrong revision will pass.
3. No change to propose, capacity, AMBIGUOUS, or VS3FULL.
4. Pure Zag. No Python.

## Governance

- Prereg PREREG_REVISE6.md committed as 1743ca053 BEFORE any
  implementation. Implementation commit is a strict descendant.
- revise5.zag untouched (git status clean for that path).
- New file: revise6.zag (mechanism diff: corroborate replacement,
  peval_prog/prog_apply_direct helpers, 5 call-site reorderings,
  Phase M addition, header update).
- Source audit: no fixture literals in diagnose_corroborate_v6,
  peval_prog, prog_apply_direct. Only generic opcodes and indices.
- Commits local only. No push.

## Commit lineage

- 1743ca053: PREREG H-REVISE6 FROZEN
- [implementation commit]: H-REVISE6 implementation + result
  (revise6.zag, REVISE6_RESULT.md, REVISE6_RAW.txt)

## Raw output

See REVISE6_RAW.txt (118 lines, 3/3 identical).
Final: "=== RESULT: 66/66 ===" / "H-REVISE6 SURVIVES".
