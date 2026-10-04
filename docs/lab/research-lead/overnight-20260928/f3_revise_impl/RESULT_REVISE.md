# RESULT: F3 REVISE builder implementation

Verdict: REVISE-PASS.

Parent prereg: f3_revise_impl/PREREG_REVISE_IMPL.md (commit c197e7cd8),
frozen before any implementation file existed. K1 holds.
Parent design: REVISE_DESIGN.md (commit ca157c743).

## 1. What was built

f3_revise.zag: derived from frozen f3_p3.zag (commit 41ed1ef9a).
20 diff hunks, all inside the learner's L_run() and header:
- deleted all three w_worldname() call sites (name emit, both
  world-detection blocks, all four flags);
- deleted the world-specific P-PROP check and PROP_OK;
- deleted the has_conj/has_neg block and its emit;
- replaced the gated if(is_neg_world==1 && attempt==1) with the
  D1-D4 REVISE loop (ATTEMPT_MAX=3, REVISE_EXHAUSTED honest stop);
- replaced the world-specific verdict with the D6 world-agnostic
  verdict (goal_ok, RULESET_FINAL machine-readable traces,
  cost_ok, determinism markers).
F3_grow_search with condition (b) is byte-identical to the
ablation-tested version (verified by diff). No new operators,
no new semantic cases, no change to search order or trace
machinery. No sealed world file was modified.

## 2. Runs (pure Zag: shell + znc only; zero Python)

Unmodified learner, 3/3 byte-identical runs per world, zero
stderr bytes on all 9 runs:

- T-CONJ (world_adv1.zag, ADV1-conjunctive): F3P3 RESULT
  REVISE-PASS. GOAL_REAL 1 on attempt 1 (no revision fired).
  NEXPS 8, COST_OK 1. FINALRULE V=Y rule=0 [X@2 & Z@1].
- T-NEG sealed (world_tneg_a.zag, TNEG-grow-negation): F3P3
  RESULT REVISE-PASS. GOAL_REAL 0 (attempt 1) ->
  GOAL_FAIL_GROW_ATTEMPT -> GROW_OK (goal-fail) V=Y rule=0
  +lit=!Z@1 -> REVISED_GROWN replanned -> GOAL_REAL 1
  (attempt 2). NEXPS 3, COST_OK 1. FINALRULE V=Y rule=0
  [X@1 & !Z@1]. The generic trigger reproduced the
  negation-solving behavior with no world-name branch.
- T-NEG renamed (world_tneg_renamed.zag, XNEG-grow-negation):
  all 3 runs byte-identical to the sealed T-NEG runs
  (md5 a1ad9ac2b972e4c862c45238f38daa82 on all six files;
  cmp confirms). No emitted line is name-derived.

## 3. Falsifier outcomes (all frozen in the prereg)

- F-RNAME: SILENT. Renamed-world outputs byte-identical to
  sealed (3/3). The H-NAME regression does not recur.
- F-RABLN: SILENT. The ablated learner (condition (b) removed
  from F3_grow_search only; diff-confined to that region)
  reaches REVISE-FAIL on T-CONJ (grew contradictory garbage:
  !X@1, !X@2, FINALRULE V=Y rule=0 [X@2 & !X@2]) and
  REVISE-FAIL on T-NEG (goal-fail grew +lit=!X@1, GOAL_OK 0
  after 2 attempts, FINALRULE [X@1 & !X@1]). It achieves
  neither the learner verdict nor the harness literal check
  on either world. Condition (b) is causally necessary.
- F-RNAMEAUDIT: SILENT. Token w_worldname occurs zero times
  in f3_revise.zag outside comments (one occurrence inside a
  header comment describing the ban itself).
- F-RCOST: SILENT. NEXPS 8 (T-CONJ), 3 (T-NEG), 3 (renamed);
  bound nexps<=8 met everywhere.
- F-RDET: HOLDS. 3/3 byte-identical per world, zero stderr,
  pure Zag end to end.
- H-CONJ-CHECK (harness): PASS. FINALRULE contains the
  (X,+,2)&(Z,+,1) pair on Y (order-independent): [X@2 & Z@1].
- H-NEG-CHECK (harness): PASS. FINALRULE contains the
  (X,+,1)&(Z,-,1) pair on Y: [X@1 & !Z@1].

## 4. Kill bars

- K1 (prereg frozen before implementation): PASS. Prereg
  commit c197e7cd8 strictly precedes any implementation.
- K2 (all falsifiers run): PASS. F-RNAME, F-RABLN,
  F-RNAMEAUDIT, F-RCOST, F-RDET, H-CONJ-CHECK, H-NEG-CHECK
  all executed with byte-identical raw evidence committed.
- K3 (pure Zag, 3/3 identical): PASS. Shell, znc, grep, diff,
  cmp, md5sum, sha256sum only. Every reported run is 3/3
  byte-identical with zero stderr.

## 5. Honest scope

REVISE-PASS is a bounded L2 infrastructure verdict: goal-failure
revision is now a generic mechanism (no world-name gating),
with the ablation-backed growth condition still doing the work.
It claims no L3, no T-NEG-class answer correctness, and does not
revive the F3 Phase 3 BUILD-PASS (that verdict stays retracted).
Criterion 12's precursor machinery is installed; criterion 12
itself requires a future invention claim under a new frozen
prereg, new sealed re-run, and new independent adversary.
The researcher's var-name convention (X/Z/Y via w_vname) and
constants (ATTEMPT_MAX=3, nexps bound 8, 3-literal cap) remain
disclosed researcher-supplied infrastructure.

## 6. Evidence index (all under f3_revise_impl/)

- PREREG_REVISE_IMPL.md (commit c197e7cd8)
- f3_revise.zag (learner), f3_revise_abl.zag (condition-(b) ablation)
- REVISE_BUILD.sh (build script)
- run_revise_c.zag / bin_revise_c / raw_revise_c_r{1,2,3}.txt/.err
- run_revise_n.zag / bin_revise_n / raw_revise_n_r{1,2,3}.txt/.err
- run_revise_rn.zag / bin_revise_rn / raw_revise_rn_r{1,2,3}.txt/.err
- run_abl_c.zag / bin_abl_c / raw_abl_c_r{1,2,3}.txt/.err
- run_abl_n.zag / bin_abl_n / raw_abl_n_r{1,2,3}.txt/.err
- build_*.err (empty; zero build stderr)
