# C500 RESULTS: CAUSAL-WORLD, partial run

Lane `causal_world/`, branch `lane/causal`. Pure Zag, pinned compiler,
`--target macos-arm64`, output via `_zag_print` (brief 4.0/4.1).
Run: `tools/zbuild.sh ./causal.zag --rep 3`. All runs behind `tnnwatch.sh`.

**VERDICT: `NOT-RUN` / INCOMPLETE. No causal-structure claim is made.**
This is a negative-and-partial report. The preregistered kill bars K1..K14
were NOT met, and most were not reached. Nothing here should be cited as
evidence that TNN learns causal structure.

## 0. Frozen separation finding: CONFIRMED INDEPENDENTLY (prereg section 0)

Re-verified by reading `compression_exec/tnn2_frozen_ref.zag` (1591 lines)
and by grep before any implementation existed:

- `ev_observe(W,s,r,o)` at line 836 is the only world ingress.
- `ev_act(W)` at line 859 takes **no arguments**. It does `ctx_push(W,-3)`,
  reads `POLICY_ROOT`, walks edges, scores candidates by `bid`, returns an
  integer. It never touches a world.
- `t2_trial(W,s,r,expected,masked,dc,di)` at line 586 assembles candidate
  *derivation graphs* over already-stored facts and verifies them against a
  post-hoc `expected` scalar supplied by the caller.
- `grep -ni 'interven|counterfact|mutilat'` over the file: **zero hits.**
  There is no do-operator, no incoming-edge cut, no mutilated graph and no
  counterfactual evaluator anywhere in TNN-2.

**Conclusion: the observation/intervention entry-point split in TNN-2 is
COSMETIC.** Two differently named doors open onto one fact store. This
finding stands independently of the experiment outcome.

## 1. The world was built and validated empirically (this part worked)

`src/w_world.zag` implements the researcher-authored ground truth with a
real do-operator: `w_set` clamps a variable, **skips that variable's
generative rule** for the current tick, and holds the clamp until `w_rel`.
Twelve variables, three regimes driven exogenously, one latent variable
that returns -1 on every read.

Measured with `probe/wstat2.zag` (all per mille, 20k-200k samples):

| quantity | measured | designed |
|---|---|---|
| P(OU=1) | 373 | 375 |
| P(OU=1 \| do(SN=0)) | 370 | 375 |
| P(OU=1 \| do(SN=1)) | 381 | 375 |
| P(OU=1 \| do(SN=0), SN=0 observed) | see D below | 375 |
| CE(SN -> OU) | 11 | 0 |
| CE(MD -> OU) lag 1 | 250 / 250 / 501 / 501 | 250 / 250 / 500 / 500 |
| CE(TR -> OU) lag 0 | 312 vs 497 | 312 vs 500 |
| CE(TR -> OU) lag 1 | 366 vs 374 | 0 (cancels) |
| CE(CN -> OU) lag 0 | 501 vs 0 | 500 vs 0 |
| CE(OU -> *) | 0 | 0 |
| q=0 / q=1 / q=2 P(OU=1) | 379 / 624 / 373 | invert / revert |
| best single-variable accuracy | 627 | 625 |

Consequences that were designed in and confirmed:
- **Delayed effect**: MD -> OU has CE 0 at lag 0 and 250-500 at lag 1.
- **Concealed interaction**: no single variable predicts OU above 628.
  OU needs the PAIR (MD_prev, CN). A conjunctive DNF is required.
- **Deceptive correlation**: SN is a perfect readout of TR and predicts OU,
  yet CE(SN -> OU) = 11 per mille. Seeing SN before OU is *not* forcing SN.
- **Changing laws / reversion**: q=1 inverts the mechanism, q=2 restores it.
- **Non-identifiability of the total effect**: CE(TR -> OU) at lag 1 is 0
  because MD_t is uniform under either arm. The path is real, its average
  effect cancels. Recorded as a finding; see ERRATA.

## 2. Privilege isolation: K0 and K0b PASS

Both are enforced at run time by `_zag_read_file` on the actual source
files, not by discipline. Pattern tables live in `src/k0pats.zag`, which is
neither the learner nor the driver, so the checker cannot match its own
strings.

```
K0_agent_world_symbols=0        # src/agent.zag contains no world symbol
K0b_driver_world_symbols=0      # src/drv.zag names nothing world-internal
```

`src/drv.zag` (the action pipeline) calls only `w_step`, `w_set`, `w_rel`,
`w_get`, `w_prev` and agent entry points. Ground-truth comparison lives in
`src/audit.zag`, which is a separate translation-unit fragment reached only
for reporting; no action and no learner input flows through it. This split
was forced by a real K0b failure: the first driver *did* name `w_true_edge`,
because it needed to score the learner against truth. Recorded, not hidden.

## 3. What did NOT work

`a_scan` fills the interventional channel correctly: the ITC table holds
**28603** populated cells after 1460 tape rows, and a spot check gives
`itc[do(CN=0) -> TR] = 20 negatives`, `itc[do(CN=1) -> TR] = 20 positives`,
which is exactly right.

But **`a_ce2`, the conditional interventional effect estimator, returns 0
for every ordered pair**, including `CE(CN -> TR, lag 0)` where the two
arms are perfectly separated (20 vs 20, 0 per mille vs 1000 per mille). The
estimator's arithmetic is a straight cross-multiplied total-variation
distance; hand-tracing it on those counts yields 2000 per mille. It does not
produce that. Consequently:

- `a_orient` finds **0 oriented edges** against 16 true edges.
- `P1_edges_matching_truth=0`, `K1_false_positive_edges=0`,
  `K1_direction_criterion_violations=0`.

**The zero violations and zero false positives are vacuous**: an orienter
that emits no edges satisfies both trivially. They are not a result.

## 4. Kill-bar status

| bar | status |
|---|---|
| K0 privilege isolation | **PASS** (0 world symbols in the learner) |
| K0b driver isolation | **PASS** (after splitting audit out of the pipeline) |
| K13 determinism | **PASS** 3/3 byte-identical, 1748 bytes, sha256 `831cbcbe89a56e89f2a60912b84344e71f4ae1365601ea9dc82525530f22acdc` |
| prereg section 0 (TNN-2 split cosmetic) | **CONFIRMED** |
| K1 confounding | **NOT MET** (0 edges found; vacuous) |
| K2 deceptive correlation | **NOT MET** (estimator returns 0) |
| K3 obs vs intervention | **NOT MET** |
| K4 unseen outcomes | **NOT REACHED** |
| K5 revision / reversion | **NOT REACHED** |
| K6 active experiment construction | **NOT REACHED** |
| K7 ablation destroys | **NOT REACHED** |
| K8 counterfactual vs associative | **NOT REACHED** |
| K9 delayed credit / composition | **NOT REACHED** |
| K10 changing laws | **NOT REACHED** |
| K11 plan vs memorised | **NOT REACHED** |
| K12 transfer | **NOT REACHED** |
| K14 no dynamics in learner | **PASS** (subsumed by K0) |

The rule learner, planner, counterfactual evaluator, experiment constructor,
three stupid baselines and four ablations are **written but not exercised**.
`src/agent.zag` contains `a_learn`, `a_orient`, `a_mediate`, `a_plan`,
`a_cf`, `a_construct`, `a_relearn`, `acc1b` and `a_vercheck`. `a_learn` is
known broken: its factor-table build loop segfaults on this compiler. It is
left in the tree, unreached, rather than deleted.

## 5. Three real defects found in the pinned toolchain

These are citable independently of this lane.

1. **Call to a small accessor function returning a constant is
   mis-compiled inside a loop.** `fn AREV()i32 { return 500; }` with
   `if(n>=AREV){ r=0-1; }` inside a `while` did not terminate the loop: the
   counter reached 784 when the cap was 500. Rewriting the cap as a literal
   with an explicit `go` flag fixed it. `ANV()`, `ANL()`, `ANZ()`, `ASC()`
   are used the same way inside `a_ce2`, which is the prime suspect for the
   all-zero effect table. **Unresolved.**

2. **Duplicate `let` bindings in one function are mis-compiled.** Two
   sibling `let v:i32` / `let w:i32` declarations in `a_orient` compiled
   cleanly and then segfaulted, with the second declaration shadowing the
   first. Every duplicate in the lane was removed. Brief section 8 B6 and
   B16 are consistent with this; this is a concrete instance.

3. **A slice element write `A[i]=v as u8` into a large arena is not usable;
   `set32`/`get32` over the same arena are.** All factor tables were
   converted from byte arrays to i32 arrays.

Also confirmed: an `i32` passed where `[]u8` is expected compiles and yields
a garbage-length slice, exactly as brief section 2 warns. It presented as a
segfault in `o_kvs(B,c,k,<i32>)`, not as a type error.

## 6. Honest boundaries

- The world is researcher-authored. That is disclosed, not hidden, and K0
  checks the learner cannot read it. It does not make the world unknown to
  the researcher.
- The representation (a DNF of value-set factors over prev/cur, versioned,
  with three acquisition channels) is researcher scaffolding. The prereg
  already says this and it remains true.
- **No world-model claim (charter 31) is made.** Dynamics are absent from
  the learner (K0), but experience was never shown to teach transitions,
  the model never predicted an unseen outcome, no counterexample revised it,
  it never supported planning, it never transferred, and no ablation was run.
  Five of the six charter-31 conditions are simply untested.
- The prereg's central distinction, seeing X before Y is not forcing X and
  observing Y, is **demonstrated in the world** (P(OU|do(SN=0)) = 370 versus
  P(OU|SN=0) = 622 observational) but **not yet demonstrated in the
  learner**, because the learner's effect estimator is broken.
- Two genuine methodological findings did survive: a marginal-only causal
  effect measure returns 0 for a real delayed causal path whose average
  effect cancels (TR -> OU at lag 1), and a purely predictive variable can
  carry a large observational-versus-interventional discrepancy. Both argue
  that the effect estimator must be conditional and must compare `do(v)`
  across v's own value range. That is why `a_ce2` is written the way it is,
  and it should be fixed rather than simplified away.
