# R32 E51P — Learner-Owned Local Conditional Weight Experts Result

Date executed: 2026-08-30
Branch: `r32-agent-sequential-frontier`
Canonical status: R27 remains canonical.

## Status

`VALID NATIVE NEGATIVE — CONDITIONAL WEIGHTS RESTORE KNOWN REACHABILITY BUT LEAVE A NO-UNIQUE TRADEOFF`

E51P tested whether the same learner-grown local regions used by E51O require different feature weighting rather than only different scalar offsets. The answer is yes: local conditional weight experts substantially improve the reachable decision geometry, including exact known-state reachability at 16+ cells, but they do not yet make UNKNOWN reachable on every no-unique trajectory.

## Native authority

- GitHub Actions run: `33345365195`
- source head: `597bbd5f6863a1a8856c075f0715b2deec98e746`
- artifact id: `9741864315`
- artifact digest: `sha256:ff0fd92d4d586812a96ab7e6f0c031af0300332d158674c5517166db772c1de2`
- assembled native source SHA256: `581c9e92040b74136a8e94f1d3b714256d7f5bd23151289b37a66078937906bf`
- frozen E45 core SHA256: `6812efb4c2cb990a59bd0f33f0a44469950201cac6633099fa4f4b2c7ae276e0`
- native binary SHA256: `e790442f7e6c61745761439d822c5704b2e6807c3f5b23ed9e568fbb4b898f0d`
- two native builds byte-identical: PASS
- native runtime: 206 s
- native exit code: 0

## Integrity

- E50 parent integrity: PASS
- development world IDs: 61,000,000 .. 61,012,959
- validation world IDs: 62,000,000 .. 62,005,399
- sealed confirmation world IDs: 63,000,000 .. 63,010,799
- world partition gate: PASS
- evaluator-domain initial-state gate: PASS
- world assignment failures: 0
- development: 12,960 episodes / 220,320 states
- validation: 5,400 episodes / 91,800 states
- UNKNOWN target nonzero: 0
- UNKNOWN learned parameters: 0
- commit order changed: no
- global topology changed: no
- graph privileged: no
- base terminal fit identity: PASS
- global linear identity: PASS
- learner-grown routing-tree identity: PASS
- conditional expert forward/reverse identity: PASS
- every accepted conditional-weight update strictly reduced development SSE: PASS
- overall integrity: PASS
- sealed confirmation executed: 0

## Conditional expert optimization

All arms used the same cumulative learner-grown routing tree but fit their local expert weights independently from zero.

| Cells | accepted coordinate updates | sweeps | stored i32-equivalent units |
|---:|---:|---:|---:|
| 4 | 1,007 | 12 | 264 |
| 8 | 2,100 | 12 | 528 |
| 16 | 4,381 | 12 | 1,056 |
| 32 | 8,829 | 12 | 2,112 |
| 64 | 17,832 | 12 | 4,224 |

Every arm reached the 12-sweep resource ceiling rather than an optimizer plateau, so more training optimization remains a legitimate later discriminator. However, validation behavior is already sufficient to reject a simple monotone-capacity interpretation.

## Fresh validation reachability

Format: known correct reachability / 4,200; no-unique UNKNOWN reachability / 1,200.

Controls:

- uncalibrated base: **4195 ; 1166**
- global linear sign calibration: **4198 ; 1151**
- 64-cell local scalar memory: **4196 ; 1154**

Conditional local weight experts:

- 4 cells: **4199 ; 1153**
- 8 cells: **4199 ; 1166**
- 16 cells: **4200 ; 1165**
- 32 cells: **4200 ; 1170**
- 64 cells: **4200 ; 1169**

The 32-cell expert is the strongest tested operating point: it preserves exact known reachability and improves no-unique UNKNOWN reachability to 1,170 / 1,200. But it still leaves 30 no-unique trajectories with no reachable negative commit score, so the exact validation gate fails and confirmation remains sealed.

## Sign classification

32-cell development:

- positive: 127,955 / 144,697
- negative: 54,500 / 75,623

32-cell validation:

- positive: 53,092 / 60,208
- negative: 22,559 / 31,592

The learner still has substantial sign error. Larger 64-cell capacity improves negative sign classification further but does not improve reachability monotonically, which means capacity alone is not the current proof.

## Causal conclusion

E51P establishes a real architectural fact:

**context-dependent local feature weights are materially more expressive than global calibration or one scalar local offset.**

This supports flexible, context-sensitive connection weighting rather than a rigid global graph. It does not show that explicit graph topology is beneficial.

The remaining failure has narrowed further. At 16+ cells every known validation episode has at least one state where the correct commit remains nonnegative, but 30–35 no-unique trajectories still never drive every commit below neutral UNKNOWN. Before adding feature interactions, more cells, or dynamic connections, the next causal experiment should audit the residual no-unique margin geometry under the frozen 32-cell expert:

- minimum top-commit score reachable on every no-unique trajectory;
- maximum correct-commit margin available on every known trajectory;
- per-cell concentration of blocked no-unique trajectories;
- whether any scalar correction interval can eliminate blocked no-unique cases without destroying known reachability;
- whether blocked trajectories share local residual feature directions that are distinguishable to the learner.

If the residual margins are separable with additional training/weight optimization, continue training-first. If they require state-dependent interactions within the same cells, test learner-created local feature interactions next. If residuals require routing state or temporary cross-region context, only then test dynamic routed connections against fixed/weighted controls.

No E51P result promotes R32 or establishes consciousness/AGI.
