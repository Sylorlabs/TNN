# REPORT: XDOMAIN-CAUSAL-ADAPT -- causal model to intervention with required adaptation

Verdict: **BUILD-PASS**. All seven kill bars pass (K1-K5, K7 in-binary;
K6 via shell sha256). No bar was weakened or moved after preregistration.

## What was built

Pure-Zag experiment (pinned znc, safebin, no forbidden executables;
NAMECHECK.md Step 0 recorded). Three source parts assembled into
`xca_full.zag`, compiled to `xca_bin`:

- `xca_world.zag`: experiment side. Source world S (a,b,c; b=2a,
  c=a+b, full observability), target world T (p,q,r,d,s observed;
  h hidden; q=2p, h=p+q, r=h, d=r+1, s=r+d), probe API
  (`w_t_probe`: set one observed var to 6, read all observed),
  namespace bind, and harness-only truth evaluators.
- `xca_learner.zag`: learner side. Generic causal discovery
  (`l_discover`: MUL(k)/ADD form fitting with a preregistered
  prefer-ADD tie-break), X-driven adaptation (`l_adapt` with
  `has_x=1`), literal copy (`l_copy`), and the from-scratch baseline
  (`l_adapt` with `has_x=0`: order-based probing +
  linear-extrapolation planner).
- `xca_driver.zag`: harness. Runs phases, executes interventions,
  checks every frozen bar, emits the report.

Two implementation refinements were made after the prereg commit; both
are behavior-preserving and documented here, neither changes any
frozen number or bar: (1) the intervention candidate set is DERIVED
(all observed vars except the leaf-analog target and its downstream
children; emitted as `derived_ncand=3` and checked by K5) rather than
listed; (2) the learner/harness separation was hardened so the learner
never calls the truth evaluators (`w_t_eval`/`w_s_eval`) -- the learner
commits to an intervention variable and the driver executes it
(verified by grep audit).

## Results by kill bar

- **K1 X-LEARNED-INDEPENDENTLY: PASS.** Discovery from S data only
  (4 obs rows + 1 structural probe on b, which falsifies the
  observationally-tied MUL(3) model of c) recovers exactly
  b=MUL(2) of a, c=ADD(a,b), a root; roles root/mid/leaf; tie-break
  triggers 0. Source demo: set a=10 -> c=30 beats set b=10 -> c=11.
- **K2 COPY-FAILS: PASS.** Literal reuse ("set a to 10") hits an
  unbound name in T; inapplicable=1; outcome r=3 (ambient) < 30.
  Adaptation is REQUIRED, not optional.
- **K3 ADAPTATION-WORKS: PASS.** Role map exactly {a->p, b->q, c->r};
  d classified non-role (no equation; probe confirms delta_r=0);
  s downstream of the leaf-analog; probe1=p measured total-effect 3
  == X-predicted (2+1); tie-break triggers 1 (r: MUL(3) vs ADD);
  policy sets p=10 -> r=30 == harness-verified optimum;
  predicted outcomes (p:30, q:11, d:3) all match truth -- including
  q's, which was TRANSFERRED from X's ADD form, never probed.
  The adapted model never recovers hidden h yet is interventionally
  correct on the whole candidate set: partial observability handled.
- **K4 ADAPTED-OUTPERFORMS: PASS.** Adapted mean 30 > copy 3;
  30*6=180 > scratch sum 142 (mean 23.67); adapted min 30 >
  scratch min 11. Mechanism (preregistered): X converts
  order-sensitive blind probing into order-invariant directed
  probing -- scratch ties adapted (30) in 4/6 presentation orders
  and collapses to 11 in 2/6; adapted is 30 in all orders.
- **K5 NO-PAIR-TEMPLATE: PASS.** In-binary: adapt and scratch both
  use 4 obs rows + 2 probes; derived candidate count 3. Manual code
  audit: `l_discover`/`l_adapt` contain no branches on T variable
  identities/names and no S/T-pair special-casing; all probe choices
  and the policy binding come from computed role scores and X's edge
  forms; X trained on S only; no paired (S,T) rows exist anywhere.
- **K6 DETERMINISTIC-3x3: PASS.** sha256 identical across 3 runs:
  `64a8d327ceb420959bc4272c8c6aa11205c0ff4978263317688252ba468132a2`.
- **K7 ABLATION-OF-X: PASS.** The lesion is structural: scratch IS
  `l_adapt` with `has_x=0` (same code path, X removed). Mean drops
  30 -> 142/6, min drops 30 -> 11. The full adapted-vs-scratch gap
  is attributable to X.

## Adaptation mechanism (for the parent)

Signature-based structural alignment + interface re-binding:

1. **Specialize:** X's edge-form inventory {MUL(2), ADD} is matched
   against T's observational fits, binding roles a->p (root),
   b->q (MUL(2)), c->r (ADD with parents (p,q)).
2. **Extend:** target-only variables are classified, not ignored:
   d (offset readout, matches no X form) -> predicted inert,
   confirmed by probe; s (child of the leaf-analog) -> downstream
   extra; h (hidden) -> acknowledged unmodeled, harmless because
   the coarse model is interventionally correct without it.
3. **Interface-adapt:** the source policy schema "set ROOT to max"
   is re-bound through the role map (ROOT->p); extras are excluded
   from the policy interface.

X-driven probe selection (the K4 mechanism): probe the highest
role-score variable (p: confirm the decision-relevant total effect
X predicts), then the lowest-score candidate (d: test X's risky
exclusion prediction). Both probes confirm X; the policy then
transfers with zero order-sensitivity.

## Honest boundaries

- The from-scratch baseline is a REAL zero-prior algorithm, not a
  strawman; it ties the adapted learner whenever its 2-probe budget
  happens to cover p (4/6 orders). The adapted advantage is
  robustness (order-invariance) and sample efficiency, not
  outcome dominance under lucky ordering. This was the preregistered
  K4 mechanism and it is exactly what the numbers show.
- The discovery tie-break (prefer ADD / preserve mediators) is a
  fixed generic bias, applied identically in S, T, and scratch;
  it triggers once (T's r). Without it, r's form would stay
  observationally tied; the bar-relevant fact is the final model
  is correct, which K3 checks directly.
- Single-shot, single-variable, deterministic, linear-ish worlds by
  design; multi-step planning and stochasticity are out of scope.

## Files

- `PREREG.md` (committed alone at a7d65146a, before implementation)
- `NAMECHECK.md` (toolchain guard record)
- `xca_world.zag`, `xca_learner.zag`, `xca_driver.zag`,
  `xca_full.zag`, `xca_bin`, `xca_compile.txt`
- `xca_run1.txt`, `xca_run2.txt`, `xca_run3.txt` (byte-identical)
- `REPORT.md` (this file)
