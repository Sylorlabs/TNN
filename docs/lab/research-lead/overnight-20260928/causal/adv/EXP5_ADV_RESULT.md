# H-EXP5 Red Team: Adversary Report

Date: 2026-09-29. Pure Zag, no Python at any stage.
Prereg: causal/adv/PREREG_EXP5_ADV.md (commit 394af3bde, frozen
BEFORE any adversarial fixture was executed; verified strict
ancestor of this result commit).
Mechanism: exp_invent5.zag rebuilt from source with
znc 2026.07.0-dev (edition 2026); binary in /tmp only, not committed.

## Verdict: H-EXP5 DOWNGRADED (not killed)

Two of four preregistered attacks succeed. Both are DOWNGRADE
findings that narrow the honesty claim; neither touches the
frozen K-E5-1..K-E5-6 bars, which are not retroactively altered.

## X-E5-1: flag-silent carryover demonstration -- SUCCEEDS (DOWNGRADE)

**Fixture F1** (new file `f1_e5_adv.txt`, committed with this
report): S1 base (cum_B.txt, 11 episodes) plus one adversary
episode `T 0 0 1 | 0 | 0 0 0` (lamp 1->0 via action 0).
lamp==1 is observed ONLY in the pre-existing S1 phase-B
episode `T 2 0 1 | 2 | 2 0 1` (start lamp==1, outcome lamp==1:
pure carryover, zero change). No action ever produced lamp==1
as a change outcome.

**Observed output** (3/3 byte-identical,
md5 700edc07fd3f918dfaf9342f1a2d4fd5):
- CONTROLLABILITY: lamp=controllable (1 changes). The
  per-variable NEEDS-EXTERNAL-SETUP flag is SILENT for lamp.
- Top pick (0 0 1) requires lamp==1.
- REACHABILITY: "NO-UNCONTROLLABLE-VARS (setup NOT verified)".
- ACHIEVABILITY: "lamp==1 demonstrated by action(s) {2} (1 eps)".

**Why this is a downgrade.** The result doc presents K-E5-2
(S1) as "the sharpest honesty property of H-EXP5:
demonstrated-as-outcome does not clear the change-based hazard
flag." That property was demonstrated in the flag-FIRES case.
Here the backstop is silent: the output presents a
carryover-only "demonstration" with no hazard flag and no
per-line carryover signal, although no action ever produced
the value as a change. The flag's granularity (per-variable
change count) is coarser than the achievability claim
(per-(variable,value) outcome). The K-E5-2 honesty property
is therefore conditional on the flag firing; when the variable
changed at least once for other values, value-level
carryover-only demonstrations pass with no machine-readable
distinction from change-demonstrations. The legend documents
the outcome-vs-change distinction in prose, but the mechanism
emits no per-line signal for it.

## X-E5-2: lumped change-action and carryover-action -- SUCCEEDS (DOWNGRADE)

**Setup.** Frozen S1 fixture (cum_B.txt), ranked state [2]
(2 0 0), reproduced byte-identical to committed evidence
(md5 ae8d42e417f38228de6aa707350bf5bd).

**Per-episode verification** (from the fixture):
- action 0 yields temp==2 twice: `T 1 0 0 | 0 | 2 0 0`
  (temp 1->2: genuine CHANGE) and `T 2 0 0 | 0 | 2 0 0`
  (temp 2->2: carryover).
- action 2 yields temp==2 twice: `T 2 1 0 | 2 | 2 1 0` and
  `T 2 0 1 | 2 | 2 0 1` (both temp 2->2: carryover; action 2
  NEVER changed temp to 2).

**Observed output.** State [2] ACHIEVABILITY line:
"temp==2 demonstrated by action(s) {0,2} (4 eps)". The line
lumps an action with change-evidence and an action with
carryover-only evidence, with no per-action change signal.
REACHABILITY for [2] flags lamp, not temp, so no backstop
covers temp. The ACHV table shows outcome counts but not
change-vs-carryover. A setup planner choosing between actions
0 and 2 receives no machine-readable indication that action 2
never produced temp==2 as a change. This shows the "which
action" half of the half-closed gap does not distinguish
change-evidence from carryover-evidence at the granularity
the line is consumed.

## X-E5-3: regression and reproduction -- FAILS (holds)

All four frozen fixtures reproduced byte-identical to the
committed evidence: S1 ae8d42e417f38228de6aa707350bf5bd,
S2 cd949065b4ad6ed4f33dbbd47bdacf2e,
S0 64fc5fde5f36107e2889ccf2703bef42,
A1 4c4e9954fe4fcbd64470e777f934515c.
The exp5-vs-exp4 diff shows exactly the four preregistered
additions (121 added lines; the only removed lines are the
4-line H-EXP4 legend being replaced). No silent functional
changes. The 6/6 stand.

## X-E5-4: source audit -- FAILS (all checks pass)

(a) compute_achievability: 36 i32 cells (z_alloc(144)), index
((a*3)+v)*3+x, EP_ACT episodes only, outcome values from
ep_ns, clamped to 0..2, actions guarded to 0..3. Matches
prereg. (b) emit_achv_table header and emit_achievability
format strings match the frozen formats exactly. (c) Legend
text matches the frozen legend exactly (5 emit lines).
(d) No test-answer literals in mechanism code: only format
strings, comments, and structural constants. (e) Diff
exp_invent4.zag vs exp_invent5.zag confirms only the four
preregistered additions.

## Revised claim

H-EXP5 remains a bounded L2 honesty improvement: the
achievability report is computed correctly, deterministically,
and without new overclaim language. But the "half-closed gap"
claim narrows: (1) the K-E5-2 honesty property (flag preserved
alongside demonstration) is conditional on the per-variable
change flag firing, and the flag cannot see value-level
carryover; (2) the demonstrating action set does not
distinguish change-evidence from carryover-evidence, so the
"which action" in "which action sets which value" is weaker
than the line's phrasing suggests to a setup planner.
Change-to counts remain the explicit future work; these
findings show why they matter.

## Governance

- Prereg 394af3bde strictly precedes all adversarial
  execution (verified via git log timestamps and
  merge-base --is-ancestor).
- Pure Zag throughout (fixture files, builds, runs, greps).
  No Python at any stage.
- Only adversary-owned files staged/committed:
  PREREG_EXP5_ADV.md, EXP5_ADV_RESULT.md (this file),
  f1_e5_adv.txt, EXP5_ADV_F1_RAW.txt, binary excluded.
- No em dashes in new docs.
- Determinism: F1 fixture 3/3 byte-identical; all four
  frozen fixtures reproduce committed md5s.

## Files (this commit)

- causal/adv/PREREG_EXP5_ADV.md (prereg, 394af3bde)
- causal/adv/EXP5_ADV_RESULT.md (this file)
- causal/adv/f1_e5_adv.txt (X-E5-1 adversarial fixture)
- causal/adv/EXP5_ADV_F1_RAW.txt (X-E5-1 raw evidence,
  md5 700edc07fd3f918dfaf9342f1a2d4fd5, 3/3 identical)

## Recommended follow-ups for the parent

1. H-EXP6 repair direction: per-(action,variable,value)
   CHANGE-to counts (not just outcome counts), or a per-line
   carryover annotation, so the demonstrating action set
   carries change-evidence.
2. Consider a value-level hazard signal to complement the
   per-variable flag, closing the granularity mismatch.
3. The F1 fixture (flag-silent carryover) is the regression
   test for any H-EXP6 rework.
