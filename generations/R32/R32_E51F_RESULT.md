# R32 E51F — Exact Sequential State-Aliasing Audit Result

Date: 2026-08-30
Branch: `r32-agent-sequential-frontier`
Workflow run: `33334471203`
Native result: `VALID DIAGNOSTIC — NO_EXACT_ALIASING_FOUND_TEST_VALUE_FUNCTION_CAPACITY_NEXT`
Canonical status: R27 unchanged.

## Integrity

- E50 parent integrity: pass.
- Fresh validation seed manifest: 5,400; zero assignment failures.
- Native builds byte-identical: SHA-256 `ee39534515136dd8e0ec094f8b0ac8071ab14d5777d953066605d9f2ca89af96`.
- Native exit code: 0.
- Evaluator truth as policy input: 0.
- Topology changed: 0.
- Graph privileged: 0.
- Evidence artifact ID: `9738616373`.

## Result

For each of the two learner-visible terminal representations, E51F audited 91,800 sequential states: 71,400 known states and 20,400 no-unique states.

Model 0:
- unique feature keys: 91,800 / 91,800;
- exact alias groups: 0;
- conflicting exact aliases: 0;
- cross-class exact conflicts: 0.

Model 1:
- unique feature keys: 91,800 / 91,800;
- exact alias groups: 0;
- conflicting exact aliases: 0;
- cross-class exact conflicts: 0.

## Interpretation

The residual E51E reachability failures are not caused by two validation states with incompatible desired terminal behavior having identical learner-visible feature vectors. The next causal discriminator is therefore value-function capacity/generalization on the same state information, not another hand-authored feature addition and not a connection-topology rewrite.

No R32 promotion claim is supported by E51F.
