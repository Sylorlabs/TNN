# R32 E51R — Conditional Expert Optimization-Dose Result

Date executed: 2026-08-30
Branch: `r32-agent-sequential-frontier`
Canonical status: R27 remains canonical.

## Status

`VALID NATIVE DIAGNOSTIC — EXPERT_OPTIMIZATION_SIGNAL`

E51R held the 32-cell conditional-weight architecture fixed and changed only the optimizer sweep resource ceiling. Longer optimization preserved exact known reachability and produced a small no-unique gain, but 24 and 48 sweeps had identical episode reachability even though the 48-sweep optimizer was still accepting strict-loss updates.

## Native authority

- GitHub Actions run: `33347031184`
- source head: `0b1c0e5ee828c2f204e4424459f7e302f4e9fd19`
- artifact id: `9742373839`
- artifact digest: `sha256:1e1213765a5c2fc51c1dcd4e7f8f9d5ec5a0fc4238e377cfb2273a6098475b15`
- assembled native source SHA256: `88a47b2f504b35d005a95a44d8c0b34b3b4c86fd3e5909eb3e4aad7bda6ae99e`
- native binary SHA256: `619b87d6ec00b264b63fd58e061314387253a6acbaa2668c8e9a560281b54cb3`
- frozen E45 core SHA256: `6812efb4c2cb990a59bd0f33f0a44469950201cac6633099fa4f4b2c7ae276e0`
- two native builds byte-identical: PASS
- native exit code: 0
- native execution runtime: about 192 s

## Integrity

- E50 parent integrity: PASS
- development worlds: 65,000,000 .. 65,012,959
- validation worlds: 66,000,000 .. 66,005,399
- sealed confirmation worlds: 67,000,000 .. 67,010,799
- world/domain separation: PASS
- world assignment failures: 0
- development: 12,960 episodes / 220,320 states
- validation: 5,400 episodes / 91,800 states
- UNKNOWN target nonzero: 0
- UNKNOWN learned parameters: 0
- terminal fit identity: PASS
- global linear identity: PASS
- routing-tree identity: PASS
- expert forward/reverse identity: PASS
- every accepted local expert update strictly reduced development SSE: PASS
- global topology changed: no
- graph privileged: no
- overall integrity: PASS
- sealed confirmation executed: 0

## Optimization dose

| Sweep ceiling | accepted updates | accepted sweeps | known reachable | no-unique UNKNOWN reachable |
|---:|---:|---:|---:|---:|
| 12 | 8,900 | 12 | 4,200 / 4,200 | 1,165 / 1,200 |
| 24 | 16,183 | 24 | 4,200 / 4,200 | 1,166 / 1,200 |
| 48 | 28,541 | 48 | 4,200 / 4,200 | 1,166 / 1,200 |

Controls on the same validation worlds:

- uncalibrated base: 4,200 / 4,200 known; 1,162 / 1,200 no-unique UNKNOWN;
- global linear calibration: 4,200 / 4,200 known; 1,154 / 1,200 no-unique UNKNOWN.

The 48-sweep expert still reached the resource ceiling with accepted updates, so parameter optimization had not numerically converged. However, capability reachability did not improve from 24 to 48 sweeps.

Validation negative-state sign correctness did continue to rise slightly with optimization: 22,661 / 31,513 at 12 sweeps, 22,788 at 24, and 22,962 at 48. Positive-side correctness fell modestly while episode-level known reachability remained exact.

## Causal conclusion

The same context-dependent local weighting mechanism still has trainable residual error, but the capability gain from additional coordinate sweeps is already extremely small: one additional no-unique trajectory from 12 to 24 and zero additional trajectories from 24 to 48.

Per the preregistered training-first rule, one wider optimization-dose extension is justified because the 48-sweep arm still accepted strict-loss updates. That extension should use cumulative snapshots so 48/96/192 sweeps can be compared efficiently on the same fixed 32-cell architecture. If episode reachability remains flat while training loss/sign accuracy continue moving, the mechanism is capability-limited rather than merely under-optimized and learner-owned local interactions become justified.

No E51R result promotes R32 or establishes AGI/consciousness.
