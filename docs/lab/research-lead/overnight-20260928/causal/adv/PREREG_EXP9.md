# PREREG_EXP9: H-EXP9 Repair of the H-EXP8 Red-Team Downgrade

**Date:** 2026-09-29
**Target:** committed causal/adv/exp_invent8.zag (H-EXP8 SURVIVES 5/5, DOWNGRADED by red team)
**Method:** copy exp_invent8.zag verbatim (cmp-verified), apply exactly the frozen additions below. No other change.
**Purity:** Pure Zag throughout. No Python at any stage (fixtures via shell heredocs, comparison via cmp/diff/grep/md5sum). No em dashes in loop documentation.

## The downgrade being repaired

X-E8-2 (EXP8_ADV_RESULT.md): the from-att "attempt denominator" silently excludes episodes superseded by the inherited law-change revision system (contest_feed sets EP_SUP on losing episodes; every H-EXP8 counter gates on ep_st==EP_ACT). The frozen legend sentence "from-att {0:t0,1:t1,2:t2} counts EP_ACT episodes of that action with clamped from-value 0/1/2 for the variable: the attempt denominator per from-state" does not disclose the exclusion, and the frozen honest limit "it does not condition on other variables or episode order" is false (F1 vs F2: same multiset, different order, different counts via supersession). Verdict: DOWNGRADED (documentation-inaccurate, incomplete X-E7-2 closure), not killed.

X-E8-1b (new honest limit, recorded not killed): raw to-values are recorded nowhere; D3 (raw 5->9) and C1 (raw 5->2) render identically.

## Frozen repair specification

### R1 (X-E8-2 repair): superseded-episode accounting

- New table `atts`: 36 i32 cells, same layout as `att` (((a*3)+v)*3+o). Counts EP_SUP episodes per (action,variable,clamped from-value). Helpers `atts_get`/`atts_add` mirror `att_get`/`att_add`.
- `compute_transitions` gains parameters `atts`, `tomin`, `tomax`, `todiff` (see R2). In the episode loop, after the EP_ACT branch, add an `else if(ep_st(W,e)==EP_SUP())` branch: for valid actions (0..3), count the clamped from-value per variable into `atts`. Superseded episodes remain excluded from trans/att/rmin/rmax/rdiff (the exclusion itself is arguably correct revision behavior; the defect was the undisclosed undercount).
- `emit_transition_evidence` gains parameters `atts`, `tomin`, `tomax`, `todiff`. After the ` from-att {...}` segment, if any superseded episodes exist for that (action,variable), emit ` sup-att {0:s0,1:s1,2:s2}`. Absence of the segment means zero superseded episodes for that action and variable.
- `main`: allocate `atts` (144 bytes), pass through; update both `emit_transition_evidence` call sites.

### R2 (X-E8-1b repair): raw to-value records

- New tables `tomin`/`tomax`/`todiff`: 108 i32 cells each, indexed like trans. Per counted change episode, record the raw (unclamped) to-value `ns`: observed min/max, and how many episodes' raw to-value differs from the clamped to label x. Helpers `todrec_get`/`todrec_set` mirror `rawrec_get`/`rawrec_set`. Initialized like rmin/rmax (999999999 / -999999999; todiff zeroed by z_alloc).
- In `compute_transitions`, inside the `if(ns!=os)` change branch, after the rawrec block, record the raw to-value into tomin/tomax/todiff.
- In `emit_transition_evidence`, in the per-bucket loop, after the `(raw:lo..hi)` tag block, emit `(raw-to:tlo..thi)` iff todiff>0 for that cell (mirrors the raw-from tag convention: tag appears only when at least one episode's raw to-value differs from the clamped to label).

### R3: legend corrections (frozen sentences)

Appended after the frozen H-EXP8 from-att legend sentence:

1. "Episodes superseded by the inherited law-change revision system (a CONTEST followed by RESOLVE with loser SUPERSEDED) are excluded from every table above: ACHIEVABILITY, CHANGE-TO, TRANSITION, and from-att all count EP_ACT episodes only. When such exclusions exist for an action and variable, the annotated line shows sup-att {0:s0,1:s1,2:s2} alongside from-att, and the complete observed attempt denominator is from-att plus sup-att; absence of the sup-att segment means zero superseded episodes for that action and variable. The revision system is order-sensitive, so from-att can differ between identical episode multisets presented in different orders."
2. "A from-bucket tag \"(raw-to:tlo..thi)\" records the observed raw to-value range for that cell and appears only when at least one episode's raw to-value differs from the clamped to label x; raw from-values and raw to-values are per-cell observed ranges, not per-episode and not distributions."

The frozen H-EXP8 honest limit "from-att counts EP_ACT episodes per clamped from-state per variable; it does not condition on other variables or episode order, and it is not a success probability under intervention" is SUPERSEDED by the sentences above (the order claim was falsified by X-E8-2b).

## Frozen kill bars

- K-E9-1 (X-E8-2 closed): On the red-team D2 fixture (causal/adv/d2_e8_adv.txt), the TRANSITION-EVIDENCE line for the ranked pick requiring temp==2 contains `from-att {0:1,1:1,2:10} sup-att {0:0,1:0,2:1}`. The excluded 11th attempt (the S1 base episode superseded at the seq-14 RESOLVE, verified pre-prereg) is visible with the exclusion marker; the complete observed denominator is 10+1=11. No other annotated line on D2 may carry an unmarked exclusion.
- K-E9-2 (no regression): all five K-E8 bars pass as frozen substrings on the 11 frozen fixtures (S1,S2,S0,A1,F1,G1,H1,J1,R1,C1,r1_e8_ctrl): J1 contains `TRANS a0 temp[0->1:1,1->2:1,2->2:2*]`, `0: from {1:1,2:2*(raw:5..5)} (3/4)`, `from-att {0:1,1:1,2:3}`; R1 contains `from-att {0:12,1:1,2:1}`; r1_e8_ctrl contains `from-att {0:2,1:1,2:1}`; C1 contains `TRANS a0 temp[0->1:1,1->2:1,2->2:1*]` and `2:1*(raw:5..5)`; K-E8-4(a) G1 substrings `0: from {1:3} (3/4)`, `1: from {0:2} (2/2)`; K-E8-4(b) H1 substrings `0: from {1:1} (1/11)`, `1: from {0:1} (1/1)`; K-E8-4(c) F1 row `TRANS a0 temp[0->1:1,1->2:1] pressure[] lamp[1->0:1]`; K-E8-4(d) K-E6-1/K-E6-2 checks. R1, J1, C1, and the control show zero sup-att segments (verified pre-prereg: zero RESOLVE lines in their exp8 outputs).
- K-E9-3 (X-E8-1b closed): On D3 (causal/adv/d3_e8_adv.txt), the temp from-bucket renders `2:1*(raw:5..5)(raw-to:9..9)`. On C1, the same bucket renders `2:1*(raw:5..5)` with no `(raw-to:` tag anywhere in its TRANSITION-EVIDENCE temp from-list. The raw 5->9 and raw 5->2 realities no longer render identically.
- K-E9-4 (determinism): 3 consecutive runs per fixture (all 11) are byte-identical; md5 recorded in the result doc.
- K-E9-5 (change-set purity): exp_invent9.zag is exp_invent8.zag verbatim (cmp-verified before editing) plus exactly the frozen additions R1/R2/R3; no other function touched. Diff of exp9 vs exp8 raw outputs on all 11 fixtures, after stripping the frozen addition lines (` sup-att {...}` segments, `(raw-to:...)` tags, the two new legend sentences), is EMPTY.

## Frozen fixtures

The 11 H-EXP8 frozen fixtures (S1 = causal/cum_B.txt, S2 = causal/exp_obs2.txt, S0 = causal/exp_null.txt, A1 = causal/adv/x_e3_a1.txt, F1 = causal/adv/f1_e5_adv.txt, G1 = causal/adv/g1_e6_adv.txt, H1 = causal/adv/h1_e6_adv.txt, J1 = causal/adv/j1_e7_adv.txt, R1 = causal/adv/r1_e7_adv.txt, C1 = causal/adv/c1_e7_adv.txt, r1_e8_ctrl = causal/adv/r1_e8_ctrl.txt), plus the red-team attack fixtures D2 = causal/adv/d2_e8_adv.txt and D3 = causal/adv/d3_e8_adv.txt for K-E9-1/K-E9-3. Binary: /tmp only, never committed.

## Honest limits (frozen, updated)

- Raw from-values and raw to-values are per-cell observed ranges, not per-episode; two cells with the same ranges may hide different distributions.
- from-att counts EP_ACT episodes only; superseded episodes are excluded from every table and shown in sup-att when present; the complete observed denominator is from-att plus sup-att; counts are order-sensitive through the revision system and are not success probabilities under intervention.
- The `*` self-loop flag follows deductively from the change predicate; it marks clamp-rendered self-loops, not a separate empirical discovery.
- Negative raw values are not expressible in fixtures (parse_int reads digits only); the symmetric bucket-0 artifact path could not be probed, same as the red team limitation.
- Classification target: bounded L2 discriminating-state selection with honest transition-level reporting. Not L3: no new representation is invented; the vocabulary (actions, variables, values) is given by the episode format.

## Governance

- This prereg is committed alone before any implementation edit, build, or run of exp_invent9. No amendments after execution begins.
- Only owned paths will be staged: causal/adv/PREREG_EXP9.md (this file), causal/adv/exp_invent9.zag, causal/adv/EXP9_RESULT.md, causal/adv/evidence/exp9_*_raw.txt. No binaries committed. No broad git add.
