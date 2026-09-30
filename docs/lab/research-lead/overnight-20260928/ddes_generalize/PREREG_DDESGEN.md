# PREREG: DDES N-Variable Generalization Test

Frozen before any generalization implementation or test execution.
This prereg commits the generalization design, the sealed 5-variable
world, the frozen analytic expectations, and the kill bars. Any
amendment must be committed transparently and re-frozen before
implementation; no bar may be altered after seeing results.

## Context

DDES Red Team 2 (b19e0e594): ATTACK-SUCCEEDS. Sealed 4-variable
World H exposed that the frozen `synthesize_plan` computes the
observation action as `obs = 4 - v_star`, which is valid only for
3-variable worlds (v_star in {1,2}). For v_star=3 the formula yields
action 1 (W), producing a plan with no observation. All 3-variable
results stand; this is a generality bound, not a soundness hole.

Task (A1 follow-up): determine whether the bound is FIXABLE by a
generic encoding or FUNDAMENTAL to the representation. Attempt the
generalization, test on 3, 4, and 5 variables, and answer whether
the fix requires researcher-authored changes per variable count or
whether the learner can derive the encoding.

## Generalization design (frozen)

The frozen derivation core (compute_arrivals, compute_frontier,
eff_waits) is already generic over n_vars: no changes needed there.
The 3-variable-specific elements and their generic replacements:

1. `synthesize_plan`: `obs = 4 - v_star` replaced by
   `obs = 2 + v_star`. Codes 0=S and 1=W stay reserved;
   observations occupy codes 2,3,4,... one per variable id.
   Single arithmetic rule, valid for all v_star >= 1. No branch
   on variable id, no per-count table.

2. `world_step`: hardcoded 3-variable state layout replaced by a
   parameterized layout for n_vars=N:
   values at st[v*4], time at st[N*4],
   timestamps at st[N*4+4+v*4]. Total 8N+4 bytes.
   Observation dispatch: action a >= 2 observes variable (a-2)
   via st[(a-2)*4]. Propagation passes: `pass < n_vars`
   (frozen used `pass < 3`). All arithmetic in N; no per-count
   branches.

3. `ddes_world`: `n_vars` becomes a parameter instead of the
   hardcoded 3. Buffer sizes scale as 4N (arrivals) and 8N+4
   (state). Schema loop, frontier selection, elimination logic
   unchanged (already generic).

4. `emit_plan`: prints action a >= 2 as O(a-2) instead of the
   hardcoded OY/OZ names. Display only.

5. `predict`: arrivals buffer sized 4*n_vars instead of 16.

New file `ddes_gen.zag` implements the above. The 3-variable
encoding changes as a side effect (OY moves from code 2 to code 4);
byte-identity with frozen 3-variable runs is NOT expected or
required. Correct convergence is what is tested.

## Sealed 5-variable World I (designed now, frozen here)

5 variables: X=0, A=1, B=2, C=3, Y=4. Delays 13 and 14 verified
absent from all frozen DDES source (ddes/, ddes_adv/,
ddes_repair/, ddes_depth/, ddes_redteam2/) before implementation.

H0 = [(X,C,13),(C,Y,0)]
H1 = [(X,Y,14)]

Frozen analytic derivation (set-X schema):
- H0 arrivals: X=0, A=INF, B=INF, C=13, Y=13.
- H1 arrivals: X=0, A=INF, B=INF, C=INF, Y=14.
- Frontier: C differs (13 vs INF, t*=13); Y differs (13 vs 14,
  t*=13). Tie at t*=13; lowest variable id wins: C (v=3).
- Target: (V*=3, t*=13), schema=1.
- Plan: [S] + 13x[W] + [O3], where O3 = code 2+3 = 5. Length 15.

Frozen expectations per config:
- cfg0 (truth=H0): TARGET V*=3 t*=13. PLAN [S,Wx13,O3].
  EXEC real=1 (C arrives at 13; observation after 13 waits sees 1).
  PRED h0=1 (13<=13), h1=0 (INF<=13 false).
  SURVIVE h0, ELIM h1, CONVERGE-OK.
- cfg1 (truth=H1): same plan. EXEC real=0 (C never arrives).
  PRED h0=1, h1=0. ELIM h0, SURVIVE h1, CONVERGE-OK.

## 4-variable regression (World H, from RT2 prereg)

Vars X=0, A=1, B=2, Y=3. H0 = [(X,Y,11)], H1 = [(X,Y,12)].
- Frontier: Y only (11 vs 12), t*=11. Target (V*=3, t*=11).
- Plan: [S] + 11x[W] + [O3] (code 5). Length 13.
- cfg0 (truth=H0): EXEC real=1. PRED h0=1, h1=0.
  SURVIVE h0, ELIM h1, CONVERGE-OK.
- cfg1 (truth=H1): EXEC real=0. PRED h0=1, h1=0.
  ELIM h0, SURVIVE h1, CONVERGE-OK.

## 3-variable regression (World A, from frozen ddesr)

Vars X=0, Z=1, Y=2. H0 = [(X,Z,2),(Z,Y,0)], H1 = [(X,Y,1)].
- H0 arrivals: X=0, Z=2, Y=2. H1 arrivals: X=0, Z=INF, Y=1.
- Frontier: Z (2 vs INF, t*=2); Y (2 vs 1, t*=1).
  Earliest: Y at t*=1. Target (V*=2, t*=1), schema=1.
- Plan: [S] + 1x[W] + [O2] (code 4). Length 3.
- cfg0 (truth=H0): EXEC real=0 (Y arrives at 2; after 1 wait
  sees 0). PRED h0=0 (2<=1 false), h1=1 (1<=1).
  SURVIVE h0, ELIM h1, CONVERGE-OK.
- cfg1 (truth=H1): EXEC real=1. PRED h0=0, h1=1.
  ELIM h0, SURVIVE h1, CONVERGE-OK.

## Method (frozen)

New file `ddes_gen.zag` under
`docs/lab/research-lead/overnight-20260928/ddes_generalize/`:
copies compute_arrivals, compute_frontier, eff_waits VERBATIM
from frozen ddesr.zag; implements synthesize_plan_gen,
world_step_gen, ddes_world_gen, emit_plan_gen, predict as
specified above; includes load_world_A (3-var, from frozen),
load_world_H (4-var, from RT2), load_world_I (5-var, sealed
here); main() runs all six configs (3 worlds x 2 truths).

Compiled with znc, run 3 times. Byte-identical outputs required.

## Kill bars (all must pass for GENERALIZATION-TESTED)

- K1 (generalization attempted and documented): this prereg plus
  the implementation plus a result document exist, all committed,
  describing exactly what was generalized and what semantic
  authority remains researcher-authored. Kill: no implementation,
  or implementation silently reintroduces per-count branches.
- K2 (tested on 3/4/5 variables, or impossibility argument):
  either (a) all six configs CONVERGE-OK with the frozen
  expectations matched line-for-line, 3/3 byte-identical runs;
  or (b) a documented impossibility argument identifying the
  exact representation barrier that blocks generalization, with
  the failing mechanism named and an architectural change
  proposed. Kill: silent partial testing, or claiming FIXABLE
  without the 5-variable sealed test passing.
- K3 (purity): pure Zag at every stage (source, znc build,
  execution, analysis). Zero Python invocations. Zero em-dash
  bytes in all committed files (byte-checked). Kill: any Python
  or any em-dash byte.

## Commit order

This prereg is committed alone. The implementation commit must be
a strict descendant. Verified via git merge-base --is-ancestor
before the result is reported.
