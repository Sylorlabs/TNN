# PREREG: F3 REVISE builder implementation

Status: FROZEN. This prereg is committed BEFORE any implementation file
exists. No result below may move these bars.

Parent: REVISE design (commit ca157c743, REVISE-DESIGN-COMPLETE).
Kill: F3 attack (commit 531e6069e, F3-ATTACK-KILLS, H-NAME confirmed).
Mechanism source: frozen learner f3_p3.zag at commit 41ed1ef9a
(docs/lab/research-lead/overnight-20260928/f3_phase3/f3_p3.zag).
F3_grow_search and condition (b) are kept byte-identical to the
ablation-tested version; any change there re-opens H-ABL.

## 1. What is built

A new learner file f3_revise.zag derived from f3_p3.zag with exactly
the REVISE design changes and nothing else:

1. Delete all three w_worldname() call sites in learner source
   (line ~825 name emit, lines ~921-930 world-detection block,
   lines ~1235-1244 world-detection block). The token w_worldname
   must occur zero times in f3_revise.zag outside comments.
2. Delete the world-specific P-PROP check block (is_conj_w/is_neg_w
   branches) and the PROP_OK emit. Candidate/rule traces
   (F3P3 CANDIDATES, F3P3 RULESET) are still emitted; answer
   checks move to the sealed harness.
3. Delete the has_conj/has_neg computation block and the
   HAS_CONJ/HAS_NEG emit. Keep the name-free CONVERGED emit.
4. Replace the gated goal-failure block
   (if(is_neg_world==1 && attempt==1)) with the D1-D4 REVISE loop:
   ATTEMPT_MAX=3; revise iff (goal_ok==0) AND (attempt<ATTEMPT_MAX);
   refutation evidence = post-failure ws snapshot at t_goal
   (unchanged call signature into F3_grow_search); on search
   success grow all Y rules with <3 literals, rebuild hyp, replan;
   on search failure emit REVISE_EXHAUSTED and stop honestly.
   The has_neg recomputation after grow is deleted (world-specific).
5. Replace the world-specific verdict block with the D6
   world-agnostic verdict: emit goal_ok, grown rule set in
   machine-readable F3P3 RULESET_FINAL traces, cost_ok, drill_ok,
   split_ok, search_ok. REVISE-PASS iff goal_ok==1 && cost_ok==1
   && drill_ok==1 && split_ok==1 && search_ok==1; else REVISE-FAIL.
   nexps counts goal attempts; F-RCOST bound: nexps<=8.
6. No other functional changes. No new operators, no new semantic
   cases, no change to F3_grow_search/condition (b).

Researcher-supplied constants retained and disclosed: var-name
resolution of X/Z/Y via w_vname (shared F2-format naming
convention, unchanged); ATTEMPT_MAX=3 (design recommendation);
nexps bound 8 (unchanged); rule cap 3 literals (unchanged).

## 2. Sealed worlds (unchanged, not rebuilt)

- T-CONJ: docs/lab/research-lead/overnight-20260928/f2_ablation/world_adv1.zag
  ("ADV1-conjunctive"), unmodified.
- T-NEG: docs/lab/research-lead/overnight-20260928/f3_phase3/world_tneg_a.zag
  ("TNEG-grow-negation"), unmodified.
- T-NEG-RENAMED: docs/lab/research-lead/overnight-20260928/f3_attack/world_tneg_renamed.zag
  (identical to world_tneg_a.zag except w_worldname returns
  "XNEG-grow-negation"; verified by diff in the parent context).
- No sealed world file is modified by this build.

## 3. Frozen falsifiers

- F-RNAME (H-NAME regression): run the frozen f3_revise learner on
  T-NEG-RENAMED 3 times. Every emitted line must be byte-identical
  to the sealed T-NEG run outputs (no harness-side name echo
  exists; the learner must emit nothing name-derived). Any
  divergence fires F-RNAME. Kills the build.
- F-RABLN (H-ABL regression): build an ablated learner
  f3_revise_abl.zag = f3_revise.zag with condition (b) removed
  from F3_grow_search only (everything else identical, including
  the name ban). Run it on T-CONJ and T-NEG, 3 times each.
  F-RABLN fires iff the ablated learner achieves BOTH
  learner-level REVISE-PASS and the harness literal check on
  either world. Expected: the ablated learner fails (REVISE-FAIL
  or wrong literals). If F-RABLN fires, condition (b) is
  decorative and the mechanism claim is void.
- F-RNAMEAUDIT: M-REVISE1 on committed f3_revise.zag: the token
  w_worldname occurs zero times outside comments. Checked with
  shell grep. Any occurrence in code fires.
- F-RCOST: nexps<=8 on every run. Fires if any run exceeds.
- F-RDET: 3/3 byte-identical runs per world, zero stderr bytes,
  pure Zag end to end (shell, znc, grep, diff, sha256sum,
  md5sum only; zero Python at every stage including this
  prereg's preparation).
- Harness literal checks (world-specific answer checks live in
  the harness, per D6): on T-CONJ the F3P3 RULESET_FINAL trace
  must contain a Y rule with the (X,+,2)&(Z,+,1) literal pair
  (order-independent); on T-NEG the trace must contain
  (X,+,1)&(Z,-,1). Checked with shell grep on the FINALRULE
  lines. A failure is recorded as H-CONJ-CHECK-FAIL /
  H-NEG-CHECK-FAIL and the build verdict is REVISE-FAIL
  (the mechanism did not produce the needed structure).

## 4. Verdict rule (frozen)

REVISE-PASS iff ALL of: F-RNAME silent, F-RABLN silent,
F-RNAMEAUDIT silent, F-RCOST silent, F-RDET holds,
H-CONJ-CHECK and H-NEG-CHECK pass, and the unmodified learner
reaches REVISE-PASS on both worlds. Otherwise REVISE-FAIL.

No L3 claim. No T-NEG-class claim. No revival of the F3 Phase 3
BUILD-PASS. Honest scope: bounded L2 infrastructure; revision
after counterexample is criterion 12's precursor machinery,
not criterion 12 itself.

## 5. Kill bars for this build

- K1 (prereg frozen before implementation): this document is
  committed alone before any f3_revise.zag exists.
- K2 (all falsifiers run): F-RNAME, F-RABLN, F-RNAMEAUDIT,
  F-RCOST, F-RDET, plus both harness literal checks, all run
  and recorded with byte-identical evidence.
- K3 (pure Zag, 3/3 identical): pure Zag throughout; every
  reported run is 3/3 byte-identical with zero stderr.

## 6. Expected diff scope (informational, not a result)

Against f3_p3.zag at 41ed1ef9a: delete the two world-detection
blocks and all four flags; delete the world-name emit; delete
the world-specific P-PROP check and PROP_OK; delete the
has_conj/has_neg block and its emit; replace the gated
if(is_neg_world==1 && attempt==1) with the D1/D3/D4 loop;
replace the world-specific verdict with the D6 emission;
keep F3_grow_search and condition (b) byte-identical.
