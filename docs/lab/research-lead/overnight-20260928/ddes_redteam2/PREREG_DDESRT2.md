# PREREG: DDES Fresh Red Team 2 (4-Variable Generality Attack)

Frozen before any attack implementation or sealed-world execution.
Target: repaired DDES (ddesr.zag, REPAIR-PASS 17c97a2cd).

## Stance

Assume the repaired BUILD-PASS claim is sound for 3 variables. This
adversary attacks the GENERALITY of the "generic" machinery. The
repaired source claims generic executable semantics: compute_arrivals,
compute_frontier, synthesize_plan, and predict are described as generic
over variable ids, delay values, and world structure. The driver
(ddes_world) hardcodes n_vars=3, but the synthesis logic itself
contains a 3-variable-specific formula.

This attack does not target the 3-variable soundness (World F found
that hole; the repair closed it). It targets whether the derivation
machinery is actually generic, or whether 3-variable assumptions are
baked into the "generic" functions themselves.

## Sealed World H (designed now, frozen here)

4 variables: X=0, A=1, B=2, Y=3. The DDES author never saw 4-variable
worlds. Frozen worlds use delays 0,1,2,3,4,5,7,8,9. World H uses 11
and 12.

H0 = [(X,Y,11)]
H1 = [(X,Y,12)]

Analytic derivation (frozen expectation):
- H0 arrivals: X=0, A=INF, B=INF, Y=11.
- H1 arrivals: X=0, A=INF, B=INF, Y=12.
- Frontier: Y only (11 vs 12). Earliest t* = 11.
- Target: (V*=3, t*=11), schema=1 (set-X).

The target variable Y has id 3. This is the critical test: the frozen
synthesize_plan computes the observation action as obs = 4 - v_star.
For v_star=3, obs = 1, which is the W (wait) action, not an
observation. The "generic" synthesis produces a plan whose final
action is a wait, not an observation.

Frozen expectations:
- compute_arrivals with n_vars=4 must produce correct 4-element
  arrival vectors (it takes n_vars as a parameter).
- compute_frontier with n_vars=4 must find (V*=3, t*=11).
- synthesize_plan with v_star=3 must produce a plan. The predicted
  output under the frozen formula is [S, W*11, W] where the final W
  is the misencoded "observation". The plan contains no observation
  action.
- A correct generic synthesis would encode an observation for
  variable 3 (e.g., action 4 or higher). The frozen code has no such
  encoding.

## Method (frozen)

A new Zag file copies the following functions VERBATIM from the
frozen ddesr.zag (no modifications): compute_arrivals,
compute_frontier, eff_waits, synthesize_plan, predict, plus the
utility functions (z_alloc, emit, get32, set32, i64s, e64,
emit_plan, plan_counter). A new 4-variable world_step and driver are
written (adapted for 4 variables; the frozen world_step is
3-variable-specific and cannot be reused verbatim for 4 vars). A new
load_world_H and main() run World H on both truth configs.

The test prints the synthesized plan. The attack succeeds if the
plan's final action is W (1) instead of an observation, proving the
synthesis logic is 3-variable-specific.

The new file is compiled with znc and run 3 times. Byte-identical
outputs required.

## Kill bars (all must pass for ATTACK-SUCCEEDS)

- K1 (sealed): this prereg is committed alone before any attack code
  exists. Delays 11 and 12 appear in no frozen DDES source file.
  Verified by grep over ddes/, ddes_adv/, ddes_repair/, and
  ddes_depth/ before implementation. The 4-variable structure was
  never tested in any frozen world. Kill (prereg invalid): any
  evidence the world was visible to the DDES author, or prereg not
  strictly preceding implementation (verified via git merge-base
  --is-ancestor).
- K2 (generality break): the attack SUCCEEDS (generality claim
  killed) if synthesize_plan with v_star=3 produces obs=1 (W action)
  as the final plan element, i.e., the plan contains no observation
  action. The attack FAILS (generality holds) if the plan contains a
  valid observation action for variable 3. This is a direct empirical
  test of the frozen formula obs = 4 - v_star.
- K3 (purity): pure Zag, zero Python at any stage (source, build,
  execution, analysis). Zero em-dash bytes in all committed files
  (byte-checked with grep). Kill: any Python invocation or any
  em-dash byte.

## Verdict mapping

- ATTACK-SUCCEEDS if K2 kills (the synthesis is proven
  3-variable-specific; the "generic" claim is bounded).
- ATTACK-FAILS if K2 does not kill (the synthesis handles 4
  variables correctly, generality holds beyond 3 vars).
- K1 and K3 are validity bars; if either fails, the attack is VOID.

## Scope note

This attack does not challenge the 3-variable soundness (repaired),
the zero-enumeration claim (K1 stood), or the L2 classification (K3
confirmed). It tests one specific generality boundary: does the
"generic" synthesis logic generalize beyond 3 variables, or is the
variable count baked in? A kill here bounds the generality claim; it
does not void the 3-variable BUILD-PASS or REPAIR-PASS.
