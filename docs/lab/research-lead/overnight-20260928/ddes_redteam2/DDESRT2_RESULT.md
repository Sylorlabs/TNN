# DDESRT2 RESULT: Fresh Red Team 2 (4-Variable Generality Attack)

Adversary prereg: 8e2a8ecde (frozen before any attack code).
Target: repaired DDES (ddesr.zag, REPAIR-PASS 17c97a2cd).
Method: pure Zag, no Python, no em dashes. 3/3 byte-identical runs.

## Verdict: ATTACK-SUCCEEDS (K2). K1 passes. K3 passes.

## K1 (sealed): PASS

Prereg 8e2a8ecde committed alone before any attack code existed.
Delays 11 and 12 verified absent from all frozen DDES source
(ddes/, ddes_adv/, ddes_repair/, ddes_depth/) via grep before
implementation. The 4-variable structure was never tested in any
frozen world. Commit order verified: prereg strictly precedes
implementation.

## K2 (generality break): ATTACK-SUCCEEDS

Sealed World H (4 variables: X=0, A=1, B=2, Y=3):
H0 = [(X,Y,11)], H1 = [(X,Y,12)]. Both truth configs run.

The VERBATIM frozen functions (compute_arrivals, compute_frontier)
correctly handle 4 variables:
- compute_arrivals with n_vars=4 produces correct 4-element vectors.
- compute_frontier with n_vars=4 finds (V*=3, t*=11).

But the VERBATIM frozen synthesize_plan breaks:
- Target: V*=3, t*=11, schema=1.
- Frozen formula: obs = 4 - v_star = 4 - 3 = 1.
- Action 1 is W (wait), not an observation.
- Synthesized plan: [S, W*11, W]. The final "observation" is a wait.
- The plan contains NO observation action.

Empirical result (3/3 byte-identical, md5
4f7010a587450021f956c8bb470e17d0, exit 0, zero stderr):

WORLD H (4-var)
TARGET V*=3 t*=11 schema=1
PLAN [S,W,W,W,W,W,W,W,W,W,W,W,W] candidates_built=1
LAST_ACTION=1 (W)
GENERALITY-BREAK: final action is W, not an observation.
The frozen obs = 4 - v_star formula yields 1 for v_star=3.

Both configs: generality_breaks=2/2. The attack does not proceed to
execution because the plan is malformed (no observation to eliminate
hypotheses).

Root cause: the "generic arithmetic" comment in synthesize_plan
claims "No branch on variable id", but the formula obs = 4 - v_star
is only valid for v_star in {1,2} (3-variable worlds). For v_star=3,
it produces the W action. The synthesis logic bakes in the
3-variable assumption. A truly generic synthesis would need an
observation encoding that scales with variable count (e.g.,
action = 2 + v_star, or a separate observation table).

Scope note: this does not void the 3-variable BUILD-PASS or
REPAIR-PASS. For all frozen 3-variable worlds, v_star is 1 or 2,
and obs = 4 - v_star correctly yields 3 (OZ) or 2 (OY). The
generality claim is bounded: the derivation machinery is generic
over delay values and hypothesis structure within 3 variables, but
the synthesis observation encoding is 3-variable-specific.

## K3 (purity): PASS

Pure Zag at every stage (source, znc build, execution, analysis).
Zero Python invocations. Zero em-dash bytes in all committed files
(byte-checked with grep -P).

## Net assessment

DDES is what it claims to be within 3 variables: genuine one-shot
derivation, zero enumeration, sound after repair. But the "generic"
label overstates the synthesis: the observation action encoding
(obs = 4 - v_star) is hardcoded for 3 variables. Extending DDES to
N variables requires redesigning the action encoding, not just
passing n_vars=4.

This is a generality bound, not a soundness hole. The 3-variable
results stand. Future work claiming "generic executable semantics"
must demonstrate the synthesis works for variable counts beyond
the frozen 3.

## Files

- PREREG_DDESRT2.md (8e2a8ecde)
- ddes_rt2.zag (frozen functions verbatim + new 4-var driver)
- DDESRT2_RESULT.md (this file)
- run1.txt, run2.txt, run3.txt (md5 4f7010a587450021f956c8bb470e17d0)
