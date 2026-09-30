# DDES Multi-Step Adaptive Intervention Planner: Result

Date: 2026-09-30. Pure Zag. Prereg frozen in commit edcefc164 BEFORE any
implementation file existed in the owned path.

## Verdict: DDES-MULTISTEP-PASS

The continuing learner's causal path now chains discriminating
interventions: each round recomputes the earliest disagreement frontier
over the CURRENT SURVIVOR SET, so the next experiment is derived
conditioned on the previous round's real outcome. All three kill bars
pass.

## What was built

File `ddes_multistep.zag` (pure Zag, zero Python). The derivation core
(compute_arrivals, compute_frontier, eff_waits, synthesize_plan_gen,
predict_gen, world_step_gen) is copied verbatim from the frozen sources
(56db8d606, 843c45fee). New: ledger stride 544 with n_cands (2 or 3)
candidate blocks plus sealed true block; frontier_surv, the
n-candidate frontier generalization (earliest schema/var/t where
arrivals are not all equal across survivors); oneshot (original
one-shot logic generalized, resolves iff exactly one survivor); adapt
(the chaining round loop with BUDGET=3, no-frontier,
world-outside-set, no-progress, and budget termination guards).

Three modes in one binary: MODE=BASE (withhold on AMBIGUOUS),
MODE=ONESHOT (single frontier over the full candidate set),
MODE=ADAPT (chaining planner).

## Multi-step demonstration (test a)

M1 (e2): h0=[(X->Y,1)], h1=[(X->Y,2)], h2=[(X->Z,2),(Z->Y,0)],
true=h2, passive (Y,2)=1.

One-shot insufficiency shown first:
```
ONESHOT e2 TARGET V*=1 t*=1 schema=1
ONESHOT e2 PLAN [S,W,O(1)] built=1
ONESHOT e2 EXEC real=0
ONESHOT e2 PRED h0=1 h1=0 h2=0
ONESHOT e2 ELIM h0
ONESHOT e2 ONESHOT-RESOLVE-FAIL survivors=2
```
The single frontier cannot discriminate h1 from h2; the entry stays
AMBIGUOUS under one-shot logic.

Adaptive chaining resolves it:
```
ADAPT e2 ROUND 1 survivors=[h0,h1,h2] TARGET V*=1 t*=1 schema=1
ADAPT e2 ROUND 1 PLAN [S,W,O(1)] built=1
ADAPT e2 ROUND 1 EXEC real=0
ADAPT e2 ROUND 1 PRED h0=1 h1=0 h2=0
ADAPT e2 ROUND 1 ELIM h0
ADAPT e2 ROUND 2 survivors=[h1,h2] TARGET V*=2 t*=2 schema=1
ADAPT e2 ROUND 2 PLAN [S,W,W,O(2)] built=1
ADAPT e2 ROUND 2 EXEC real=1
ADAPT e2 ROUND 2 PRED h1=0 h2=1
ADAPT e2 ROUND 2 ELIM h1
ADAPT e2 RESOLVED winner=h2 rounds=2
```
Round 2's target (Z, t=2) is derived from the reduced survivor set,
which exists only because of round 1's real outcome. Post queries
(Y,1) -> 0, (Y,2) -> 1 both correct.

M2 (e3): h0=[(X->Y,1)], h1=[(X->Z,1),(Z->Y,1)],
h2=[(X->Z,2),(Z->Y,0)], true=h1. ONESHOT-RESOLVE-FAIL survivors=2
again; ADAPT resolves winner=h1 in 2 rounds with round 2 target
(V*=2, t*=1, schema=1), plan [S,W,O(2)], real=1, ELIM h2. Post
queries (Z,1) -> 1, (Z,2) -> 1 correct. The chaining is generic
across families, not case-specific.

## One-shot regression (test b)

Case A (e4): the original 2-candidate ambiguity. MODE=ONESHOT
resolves winner=h1 rounds=1; MODE=ADAPT also resolves winner=h1
with rounds=1 (no chaining needed, no spurious extra round).
MODE=BASE still withholds. Post queries correct in both resolving
modes.

## Termination (test c)

M1 and M2 resolve in exactly 2 rounds; A in 1 round. The budget
never binds. The no-progress and budget guards are coded and frozen
as backstops; the derivation math guarantees at least one
elimination per round whenever the true world is inside the
candidate set (at the frontier (V*,t*), predictions always split:
the min-arrival side predicts 1, the other side 0, and the real
outcome matches at least one side), so the planner cannot loop.

## No enumeration

Each round builds exactly one plan from a derived (V*, t*, schema);
plans_built=1 per round. No plan space is enumerated. BUDGET=3
bounds ROUNDS, not plan length; each round's plan is assembled from
a derived target with no length bound in the derivation path.

## No regression

The 7 P1/P2 output lines (e0/e1 FEED, ENTRY, Q) are byte-identical
across MODE=BASE, MODE=ONESHOT, and MODE=ADAPT (shell diff clean).

## Determinism

3/3 runs byte-identical, md5 8792fa4d59b5eb87b60c3f19205f6c0b.
Exit 0, zero stderr on all runs (RUN1/2/3.txt, RUN1/2/3.err).

## Disclosure: VERIFY.sh summary-count correction

The frozen prereg never stated summary totals; my implementation-side
VERIFY.sh transcribed them with an addition error (7/7 and 11/11
instead of the correct 8/8 and 12/12: ONESHOT is 1+2+1+1+3=8 checks,
ADAPT is 1+2+3+3+3=12 checks). The two expectations were corrected to
the arithmetically correct values before the verdict; no frozen bar
was altered (K2's letter names only the behavioral outcomes, all of
which hold exactly as frozen). The binary and all frozen traces are
unchanged by this correction.

## Kill bar verdicts

- K1 (prereg precedence): PASS. Prereg commit edcefc164 strictly
  precedes the implementation commit; verified with
  git merge-base --is-ancestor.
- K2 (multi-step plus regression): PASS. (a) On M1 and M2,
  MODE=ONESHOT emits ONESHOT-RESOLVE-FAIL survivors=2 and MODE=ADAPT
  resolves with the frozen winner in rounds=2, every frozen
  TARGET/PLAN/EXEC/PRED value matching, post queries correct;
  (b) on A, both ONESHOT and ADAPT resolve winner=h1 (ADAPT in
  rounds=1), post queries correct; (c) P1/P2 lines byte-identical
  across modes.
- K3 (purity and determinism): PASS. Pure Zag, zero Python at every
  step; 3/3 byte-identical; zero em/en dash bytes per shell-only
  check_no_dash.sh; exit 0, zero stderr.

## Classification

Bounded L2. NOT L3. Researcher still owns: hypothesis format, the
frozen case set, the derivation algorithm, action vocabulary, the
budget constant. The learner authors: the decision to chain, each
round's target conditioned on the observed outcome, each plan's
length and sequence, and the resolution from the real outcomes.

## Recommended next step

Adaptive design on the law-revert family: extend the planner's feed
protocol to time-indexed passive evidence (early/late observations)
so a change-then-revert ambiguity becomes expressible as competing
rule graphs, then freeze a revert-family case where round 1 must
first establish the changed law and round 2, conditioned on the
revert evidence, must re-derive against the reverted law. Rationale:
the C1 clean wave exposed revision-after-revert as the live
mechanism boundary; chaining gives the learner a second derived
experiment exactly when the first outcome contradicts the changed-law
hypothesis. Arena C9 re-entry should wait until the revert family
has a verdict, so the number measures the adaptive mechanism, not
the one-shot one.
