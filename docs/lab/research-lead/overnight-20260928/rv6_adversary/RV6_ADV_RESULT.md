# H-REVISE6 RED TEAM RESULT (X-RV6)

**Date:** 2026-09-29
**Branch:** tnn-native-lab
**Target:** H-REVISE6 SURVIVES (66/66), implementation commit 400463112
**Prereg:** `rv6_adversary/PREREG_RV6_ADV.md`, content frozen before any
attack code was written or executed. Content committed (by sweep, see
Governance) as blob in `c9e672975` at 2026-09-29 23:33:17 UTC,
byte-verified identical to the authored file. No attack code existed
at that time.
**Verdict: H-REVISE6 SURVIVES this red team.** One attack succeeded
as a CONFIRMED RESIDUAL (pre-disclosed fundamental limit, no new
downgrade). Four attacks failed (defenses held).

## Mission and stance

Assume the H-REVISE6 repair claim is false. Attack the new
revision-correctness condition (b), the reordered P1-before-corroborate
protocol, the Phase M gate behavior, and the 66/66 regression. Pure
Zag throughout. No Python at any stage (shell tools used: sh, sed,
grep, awk, cmp, md5sum, znc).

## Method

Adversary harness `rv6_adversary/rv6_adv.zag` = lines 1..507 of the
committed `revise6.zag` (the full mechanism region: allocators,
program machinery, discover, apply, vs3 store, propose, peval_prog,
prog_apply_direct, diagnose_corroborate_v6, dcopy), verified
byte-identical to `git show HEAD:revise6.zag | head -507` by cmp,
with `main()` replaced by attack drivers. The real, unmodified
`diagnose_corroborate_v6`, `peval_prog`, `prog_apply_direct`,
`diagnose_propose`, `discover`, and `vs3_*` functions are called.
Each empirical attack ran 3 times; all 3 runs byte-identical
(cmp-verified). Raw output: `rv6_adversary/RV6_ADV_RAW.txt`
(md5 3ce21e44198451c5d514467f59a2866a), run1 of 3 identical runs.
Toolchain: znc 2026.07.0-dev (edition 2026).

## Attack X-RV6-1 (correlated fail2 boundary): SUCCEEDS as CONFIRMED RESIDUAL

**Fixture (exact X-RV5-1 replay):** P0 = broadcast-last
([N],[C1],[SUB,0,1], nn=3). Passing set {abc, def, ghi, jkl}.
fail1 = ("zqy" -> "zzz"). `diagnose_propose` emits candidates
(0,122) score 1, (1,113) score 0, (2,121) score 0, returns 122,
i.e. proposed (0,122). `discover` on fail1's sequence returns
nn=3, P1 = broadcast-first ([SUB,N,N]). fail2 = ("zab" -> "zzz").

**Observed gate behavior (3/3 identical):**
`CORROBORATE PASS: condition fires, revision predicts fail2, current
program mispredicts`, gate returns 1. (a): fail2[0]='z'==122 fires.
(b): P1("zab")="zzz"==fail_out2 passes. (c): P0("zab")="bbb"!="zzz"
passes. The caller appends the wrong revision (0,122) (rc==1).
Held-out "zbq": post-append VS predicts "zzz"; truth under the
hidden H (IF input[2]=='y' THEN broadcast-first ELSE broadcast-last)
is "qqq". Held-out breaks, exactly as in the H-REVISE5 red team.

**Interpretation:** This is the pre-disclosed fundamental limit,
not a new defect. The builder's frozen underdetermination argument
is empirically confirmed against the new gate: the observable
signature (fail1, fail2, (p,v), P0, P1, passing) of this adversarial
case is structurally isomorphic to genuine Phase C corroboration,
and no observation-only gate can separate them. The new (b) raises
the bar only against revisions that fail to predict fail2; here the
wrong P1 predicts fail2 correctly by construction of the attack.
Per the frozen prereg verdict rules, X-RV6-1 succeeding =
CONFIRMED RESIDUAL. No kill. No downgrade. The narrowed claim
("X-RV4-1 class is closed" NOT reinstated) stands as documented.

## Attack X-RV6-2 (protocol reorder safety): FAILS, defense holds

**Static analysis (all 6 `diagnose_corroborate_v6` call sites):**
sites at revise6.zag lines 611 (C), 708 (G), 777 (H), 853 (I),
981 (L), 1023 (M). At every site the pattern is:
`discover(...)` -> `if(nn<0){ emit("FATAL discover ..."); return 1; }`
-> `diagnose_corroborate_v6(..., p, nn)`. All 6 sites FATAL-guard a
failed discovery before the gate; no site passes nn<0 or a P1 from
other data. `discover` takes no VS parameter; its full call graph
(peval_node, peval, pextract, pfits_at, p_binop, prog_uses_n,
discover_pass) contains zero `vs3_` calls and zero `VS[` writes
(verified by grep over lines 60-230). The reorder therefore cannot
alter any gate input relative to revise5's order; discovery is a
pure function of (S, seqs) with no VS side effects. The 66/66
byte-identical regression independently confirms no behavioral
drift in which P1 is discovered. No protocol break found.

**Robustness wart (not a kill):** during harness development, an
early harness bug passed nn=-1 to `prog_apply_direct`, which
panicked with `slice index out of bounds` (peval_prog reads
p1[(nn1-1)*3] = p1[-6]). The gate has no graceful path for nn<=0.
This is UNREACHABLE in the shipped main (all 6 sites guard), but a
future caller that skips the guard gets a panic instead of a clean
withhold. Recorded as a defense-in-depth gap, not a verdict
changer.

## Attack X-RV6-3 ((b) false withhold on genuine revision): FAILS, defense holds

**Fixture:** fail1 = ("xbc" -> "cbx") (reversal). `discover`
returns nn=5, P1 = [[1,255,255],[0,255,255],[3,255,255],[5,1,2],[6,0,3]]
i.e. nodes N, K, C1, ADD(1,2)=k+1, SUB(0,3)=n-1-k: true n-parametric
reversal, exercising `peval_prog` recursion to depth 3 including
both the ADD and SUB branches. fail2 = ("xqp" -> "pqx"):
(a) fail2[0]='x'==120 fires; (b) P1("xqp")="pqx" verified first via
direct `prog_apply_direct` call (genuine fixture confirmed valid);
(c) P0("xqp")="ppp"!="pqx". Gate returns 1:
`CORROBORATE PASS: condition fires, revision predicts fail2, current
program mispredicts`. No false withhold.

**Length generality (new coverage beyond the frozen len-3 suite):**
fail2 = ("xqpw" -> "wpqx") (len 4, fail1 len 3). P1 generalizes
(P1("xqpw")="wpqx" verified directly; the evaluator threads n=4
correctly). Gate returns 1. The new (b) is length-general within
the framework's input domain.

## Attack X-RV6-4 (regression and source audit): FAILS, defense holds

Rebuilt committed `revise6.zag` unmodified with znc; 3 runs
byte-identical (cmp), md5 bb60a29a9e4960283e16589ad51846f1, matching
committed `REVISE6_RAW.txt` exactly. Final lines:
`=== RESULT: 66/66 ===` / `H-REVISE6 SURVIVES`. The revise5-to-revise6
diff (302 diff lines) contains exactly the preregistered change set:
peval_prog + prog_apply_direct helpers (new), diagnose_corroborate
replaced by diagnose_corroborate_v6 (redundant discrimination loop
deleted; revision-correctness check added), 6 call-site updates
(discover moved before corroborate; new p1/nn1 arguments), Phase M
addition, header and H-REVISE5->H-REVISE6 label renames. No other
mechanism edits. `diagnose_propose`, capacity, AMBIGUOUS, VS3FULL
untouched. Grep over the new function bodies finds no fixture byte
literals: only opcode constants (0-6), indices, and CORROBORATE
diagnostic strings.

## Attack X-RV6-5 (independent (c) failure path): FAILS, defense holds

**Fixture:** VS = P0 broadcast-last, then `vs3_revise` appends R1
(0,120) -> broadcast-first directly (rc==1, vcount==1). fail2 =
("xqw" -> "xxx"), P1 = broadcast-first discovered from
("xab" -> "xxx"). (a): 'x'==120 fires. (b): P1("xqw")="xxx"
passes. (c): VS("xqw")="xxx" via the existing R1 revision.
Gate returns 0 with `CORROBORATE FAIL: current program already
predicts fail2 (not a counterexample)`. vcount stays 1: no duplicate
revision appended. This is the independent (c) failure path the
frozen 66/66 suite never directly demonstrated; the "honestly
three-condition" claim now has empirical coverage for all three
legs: (a) fails alone (frozen Phase L), (b) fails alone (frozen
Phase M), (c) fails alone (this attack).

## Classification

Bounded L2+ revision, not L3. Unchanged.

## Boundaries and limits (unchanged, re-confirmed)

1. X-RV5-1 pattern (adversarially correlated or mislabeled second
   counterexample) passes the new gate. Re-confirmed empirically
   here. Fundamental limit of observation-only gating, not a bug.
2. The gate trusts fail2's label.
3. Gate panics (rather than cleanly withholding) if called with
   nn<=0; unreachable in shipped main; all 6 call sites guard.

## Governance disclosures

1. Prereg content was authored and frozen before any attack code
   was written or executed. It was committed by SWEEP inside
   `c9e672975` (the H-FDCR-UNIFIED4 red-team worker's commit,
   2026-09-29 23:33:17 UTC), not in a standalone prereg commit.
   The blob is byte-verified identical (cmp) to the authored file.
   Prereg-before-implementation ordering holds in substance; the
   commit message is not mine. This is the known shared-tree sweep
   hazard, disclosed.
2. One harness bug during execution: the first attack main copied
   pextract i32 sequences byte-wise into the discover arena, which
   corrupted non-zero index values and made `discover` return -1
   for the reversal fixture. Fixed by copying with set32/get32
   (matching the frozen Phase L pattern's intent). All reported
   evidence comes from the corrected harness, 3/3 byte-identical.
   The bug was in adversary scaffolding, never in the mechanism.
3. Pure Zag. No Python at any stage: harness authoring, building
   (znc), execution, determinism checks (cmp), hashing (md5sum),
   and static analysis (grep/awk/sed) only.
4. No fixture literals in the new gate/evaluator functions.
5. Commits local only. No push.

## Commit lineage

- `1743ca053`: PREREG H-REVISE6 FROZEN (builder)
- `400463112`: H-REVISE6 implementation + result (builder)
- `c9e672975`: PREREG_RV6_ADV.md content committed (by sweep;
  blob verified identical; no attack code existed yet)
- [this commit]: rv6_adv.zag, RV6_ADV_RAW.txt, RV6_ADV_RESULT.md

## Raw output

`rv6_adversary/RV6_ADV_RAW.txt` (run1 of 3 byte-identical runs,
md5 3ce21e44198451c5d514467f59a2866a).
