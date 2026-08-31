# R32 E51V — Trajectory-Critical Local Objective Result

Date executed: 2026-08-30
Branch: `r32-agent-sequential-frontier`
Canonical status: R27 remains canonical.

## Status

`VALID NATIVE DIAGNOSTIC — TRAJECTORY_OBJECTIVE_TRADEOFF WITH LARGE PARETO-LIKE MOVEMENT`

E51V held the 32 learner-visible features, frozen commit ordering, learner-grown 32-cell routing tree, local linear expert architecture, UNKNOWN semantics, and connection topology fixed. The only experimental change was to train the same local expert bank on learner-selected trajectory-critical states under an exact multiple-instance trajectory violation loss.

## Native authority

- GitHub Actions run: `33352007155`
- source head: `c4df4edad8dac77e639f7804169d88cb848f11ed`
- artifact id: `9744015333`
- artifact digest: `sha256:47dd825dc248cfb7f0c23083baf8f34d5da6639b406e1b395e5bee7b96eabbf4`
- assembled native source SHA256: `642174d78dd3fe6183e82eeda05d2c75a439cf7d37b7df411175de1c118325a3`
- E51V helper SHA256: `68cd2da6b87660a25b227a1a9370b1cd6483c5ed984ad6bacb78a36d5619f672`
- patched native run SHA256: `b0a0c4eca38c31b2e457149acc1374a84c2b4530d395d99dfe6aa0d16a3118a0`
- main injection SHA256: `fa88c9d7f8422d474fc015c9e901747872171d2c168c466047d26e5f9551f19e`
- frozen E45 core SHA256: `6812efb4c2cb990a59bd0f33f0a44469950201cac6633099fa4f4b2c7ae276e0`
- native binary SHA256: `c9e5f7c9123e4117a51d1ccc96f589559739643895a68c0cb2adce925c287470`
- two native builds byte-identical: PASS
- native exit code: 0
- native runtime: about 299 s

## Integrity

- E50 parent integrity: PASS.
- stage-75/76/77 world/domain separation: PASS.
- world assignment failures: 0.
- development: 12,960 episodes / 220,320 states.
- validation: 5,400 episodes / 91,800 states.
- UNKNOWN nonzero targets/positive warrant: 0.
- evaluator truth exposed to inference: 0.
- ambiguity label exposed: 0.
- validation membership exposed: 0.
- commit ordering changed: 0.
- new learner-visible features: 0.
- cross-cell edges: 0.
- graph privileged: 0.
- state-SSE controls forward/reverse identical: PASS.
- trajectory treatment forward/reverse identical: PASS.
- accepted trajectory rounds: 3.
- final development trajectory violation loss: 282,964.
- overall integrity: PASS.
- sealed confirmation executed: 0.

## Development trajectory movement

| Arm | Reached trajectories / 12,960 | Trajectory violation loss |
|---|---:|---:|
| A — 96-sweep state-SSE | 12,855 | 11,471,766 |
| B — 192-sweep state-SSE | 12,859 | 11,632,055 |
| C — first accepted trajectory round | 12,900 | 4,128,573 |
| D — final accepted trajectory round | **12,943** | **282,964** |

The objective change therefore had large causal effect on the quantity it was designed to optimize. The final treatment leaves only 17 development trajectories violated, versus 105 for the matched 96-sweep control.

## Fresh validation

| Arm | Known reachable / 4,200 | No-unique UNKNOWN reachable / 1,200 | paired gains vs A | paired losses vs A | switching losses vs A |
|---|---:|---:|---:|---:|---:|
| A — 96-sweep state-SSE | 4,174 | 1,160 | 0 | 0 | 0 |
| B — 192-sweep state-SSE | 4,177 | 1,159 | 3 | 1 | 0 |
| C — first trajectory round | 4,188 | 1,177 | 32 | 1 | 0 |
| D — final trajectory round | **4,191** | **1,195** | **53** | **1** | **0** |

The final trajectory arm improves both aggregate capability dimensions dramatically relative to both state-SSE controls. It is only five no-unique episodes short of exact UNKNOWN reachability and nine known episodes short of exact known reachability.

It did not satisfy the preregistered partial-rescue gate because it lost one trajectory previously solved by the 96-sweep control. Therefore the frozen outcome is `TRAJECTORY_OBJECTIVE_TRADEOFF`, not rescue, and confirmation remains sealed.

## Failure concentration

Final treatment per evaluator mode:

- mode 0: 600 / 600
- mode 1: **595 / 600**
- mode 2: 600 / 600
- mode 3: **591 / 600**
- modes 4–8: 600 / 600 each.

Thus all 14 remaining validation failures are concentrated in two regimes: five no-unique mode-1 trajectories and nine mode-3 change/switch trajectories. The treatment introduced zero losses in the preregistered switching/reversal paired-loss audit relative to the 96-sweep control; its nine mode-3 failures are largely inherited/residual rather than newly created.

## State-sign behavior

The trajectory treatment intentionally does not maximize average state classification. Final validation state sign counts are:

- positive: 48,695 / 63,486;
- negative: 18,669 / 28,314.

These are not better than the state-SSE controls, yet episode reachability is much better. This directly confirms the E51U diagnosis that average state-level SSE/sign accuracy is not the right capability objective at this frontier.

## Causal conclusion

E51V strongly rejects the hypothesis that dynamic graph/connectivity machinery is already required for the residual R32 terminal problem. With **no topology, feature, routing, or action-order change**, a trajectory-aligned objective removed most of the residual capability failures.

The remaining bottleneck is now training/optimization of that trajectory objective, not proven missing connectivity. In particular, the trajectory candidate learner currently reuses the older bounded local-expert fitter, while the matched state-SSE lineage has already demonstrated meaningful behavior changes at much larger optimization dose. Training-first protocol therefore requires a trajectory-objective optimization-dose/stability experiment before any cross-context connection mechanism is justified.

The next experiment should keep the exact E51V cognition and compare larger optimization dose inside each critical-state refit, while measuring paired episode preservation. It should also test a generic conservative acceptance rule that never accepts a development update which increases the count of already-solved trajectories, using trajectory violation loss only as the secondary objective. This is generic learner optimization, not an ambiguity rule.

No E51V result promotes R32 or establishes AGI/consciousness.