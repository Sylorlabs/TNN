# RESULT: L3C v2 Independent Adversary Attack (pipeline step 10)

Date: 2026-09-30. Verdict: **L3C-V2-ADV-SURVIVES-THIS-ROUND**.

The v2 construction claim survives this attack round. All three families
matched their frozen predictions; no break bar was tripped. The untested
paths (depth-3 recursion, declare-and-withhold on the disc2 blind spot,
default-edge refine) all behaved exactly as the mechanism's design implies.

## Kill-bar results

- K1 prereg precedence: attack prereg committed ALONE as 2c0e52739 before
  any attack file existed. Verified: git merge-base --is-ancestor
  2c0e52739 <this result commit> returns true; this commit touches no
  frozen bar. The prereg was never amended.
- K2 frozen predictions vs results (mechanism copy verbatim, committed
  l3c_v2.zag unmodified): all three families matched. 3/3 runs
  byte-identical (sha256
  75aaf7117066853d740a79becec3db56ae72bd5c16671148b84e535374a9a5d2,
  recorded in sha256sums.txt). Attack source sha256 recorded in
  sha256sums.txt; the mechanism prefix is byte-identical to committed
  l3c_v2.zag lines 1-700 (diff-verified).
- K3 purity: pure Zag plus shell only, zero Python. No em or en dashes
  (check_no_dash.sh clean). Contaminated paper untouched (verified empty
  diff). Builder's v1 harness not re-run; this is an independent attack.

## Per-family outcomes

- F1 (sig 701) depth-3 successive refinement: REFINE fired twice
  (edge=1 atom (3,0,9) at D1; edge=3 atom (2,0,2) at D2), built delta 3,
  eval 4/4, structure checks CHK_F1_depth3=PASS and CHK_F1_atoms=PASS.
  The dump confirms the chain D1 -(f1==1)-> D2 -(f3==9)-> D3 -(f2==2)-> TERM
  with inherited defaults at each level. Recursion composes to depth 3;
  the leaf-edge staleness analysis from the prereg holds empirically.
- F2 (sig 702) disjunction blind spot: exactly 3 HONEST_FAIL trace lines,
  built delta 0, unresolved delta 3, CHK_F2_withhold=PASS (rule(702) still
  TERM(2)), no dispatch for 702 anywhere in the dump, zero AMBIGUOUS
  events anywhere in the run. The system declares and withholds on the
  vocabulary blind spot exactly as designed.
- F3 (sig 703) default-edge refine: REFINE fired once on edge=6 with
  lk=0 (the DEFAULT edge), built delta 2, eval 5/5, CHK_F3_defrefine=PASS,
  CHK_F3_defedge_lk0=PASS. The dump shows D1's default edge re-pointed at
  D2 (f3==9), D2 inheriting the old TERM(2) default. The untested path
  works as designed.

## Disclosed harness-labeling slip (not a mechanism finding)

Prereg section 4 F2 stated the eval as "2/4" scored against ground truth
(two of four eval points have truth 0 but the withheld system predicts 2).
The attack main instead measured the equivalent withhold signature:
all four eval points predict the base class 2 (4/4). The frozen
mechanism-facing facts are identical under both scorings (built=0,
3x HONEST_FAIL, rule still TERM, no dispatch), and both express the same
declare-and-withhold outcome. No bar was altered; this is a label
clarification only.

## Static audit findings (prereg S1-S3, confirmed empirically)

The pre-design audit closed three candidate holes by code reading:
leaf-edge staleness (F1's clean depth-3 run confirms), silent
misresolution (every interp miss surfaced as counted/stashed event;
e<0 unreachable), disc2 fiat (FOUND requires exactly one separator;
AMBIGUOUS exact). No family was wasted on them.

## Single recommended next step for the L3C line

The construction claim's tested envelope is now: unique-separator vocab,
depth-3 recursive refine on both labeled and default edges, deferred
EVID_MIN=2, honest withhold on blind spots. The strongest remaining
unattacked property is simultaneous competing refinements on DIFFERENT
edges of the same DISP node (two live nested-clash records racing on
sibling edges) plus a mixed-output check after a refine chain has been
built. If that passes, the L3C line should move to the v3 design question
the prereg deliberately left open: a vocabulary that can learn OR, since
F2 confirms OR is a permanent, by-design blind spot of disc2.
