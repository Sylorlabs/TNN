# R32 E51O — Learner-Owned Local Calibration Memory Result

Date executed: 2026-08-30
Branch: `r32-agent-sequential-frontier`
Canonical status: R27 remains canonical.

## Status

`VALID NATIVE NEGATIVE — WEAK MONOTONE LOCAL-CAPACITY SIGNAL WITH MATERIAL KNOWN/UNKNOWN TRADEOFF`

E51O tested whether the heterogeneous commit-vs-UNKNOWN boundary identified by E51N could be repaired by bounded learner-owned local scalar memory on the unchanged 32-feature state. The mechanism was native Zag v2, recruited its own prototypes from development residuals, and did not change connection topology or commit ordering.

## Native authority

- GitHub Actions run: `33344918710`
- source head: `f8ce1d7f325ae824930891d8f5419223fc34c401`
- artifact id: `9741707094`
- artifact digest: `sha256:7f7869f2c40b5c14380039801d9dda9c9c0af80c1c22039e44636d5b3189c748`
- assembled native source SHA256: `3a77660c89b44bc5d46ded7765812cede89016d130142c63c4020c3c63516065`
- frozen E45 core SHA256: `6812efb4c2cb990a59bd0f33f0a44469950201cac6633099fa4f4b2c7ae276e0`
- native binary SHA256: `47cad88ad718148a50af97d26c842e85e07027810aa9bad67bc90c77c3ca6b73`
- two native builds byte-identical: PASS
- native experiment runtime: 116 s
- native exit code: 0

## Integrity

- E50 parent integrity: PASS
- fresh development world IDs: 58,000,000 .. 58,012,959
- fresh validation world IDs: 59,000,000 .. 59,005,399
- sealed confirmation IDs: 60,000,000 .. 60,010,799
- world partition gate: PASS
- five evaluator-domain initial-state ranges: PASS
- world assignment failures: 0
- development: 12,960 episodes / 220,320 states
- validation: 5,400 episodes / 91,800 states
- UNKNOWN target nonzero: 0
- UNKNOWN learned parameters: 0
- base terminal forward/reverse identity: PASS
- global linear forward/reverse identity: PASS
- global 16-hinge forward/reverse identity: PASS
- local prototype/correction forward/reverse identity: PASS
- every accepted local split strictly reduced development loss: PASS
- accepted local cells: 64
- overall integrity: PASS
- confirmation executed: 0

## Resource curve

The local memory stores one 32-feature prototype, one parent index, and one scalar residual correction per cell.

| Cells | stored i32-equivalent units | worst-case validation routing feature-distance ops |
|---:|---:|---:|
| 8 | 272 | 41,126,400 |
| 16 | 544 | 88,128,000 |
| 32 | 1,088 | 182,131,200 |
| 64 | 2,176 | 370,137,600 |

All four cumulative capacities were reached by learner-owned development-loss-improving recruitment.

## Fresh validation reachability

Format: known correct reachability / 4,200; no-unique UNKNOWN reachability / 1,200.

Controls:

- uncalibrated terminal ordering head: **4194 ; 1158**
- global linear sign calibration: **4176 ; 1159**
- global linear + 16 learner-selected hinges: **4172 ; 1170**

Local residual memory:

- 8 cells: **4174 ; 1163**
- 16 cells: **4175 ; 1163**
- 32 cells: **4175 ; 1166**
- 64 cells: **4175 ; 1166**

No arm reached the exact validation gate. Confirmation remained sealed.

## Sign-fit behavior

At 64 cells:

- development positive sign correct: 127,351 / 144,844
- development negative sign correct: 50,815 / 75,476
- validation positive sign correct: 55,345 / 63,463
- validation negative sign correct: 17,257 / 28,337

The learner therefore still has substantial development error after all 64 local scalar cells have been recruited.

## Interpretation

The local capacity curve is technically monotone within the local family:

- known reachability: 4174 → 4175 → 4175 → 4175
- no-unique UNKNOWN reachability: 1163 → 1163 → 1166 → 1166

But the signal is weak and rapidly saturating. It costs roughly 13.6x more routing work from 8 to 64 cells for only +1 known reachability and +3 no-unique reachability. Moreover every local arm remains materially worse than the uncalibrated base on known reachability.

This is therefore not evidence that simply scaling scalar prototypes to hundreds or thousands is the right cognitive architecture. The result says the boundary is local, but **one scalar offset per local region is still too low-capacity**.

The next causal discriminator should keep the same learner-visible state and the same learner-grown local routing, but allow each recruited region to own a small conditional **weight correction** rather than only one scalar correction. That directly tests whether the missing flexibility is region-specific feature weighting. It is a matched weight-system experiment, not a graph rewrite.

No E51O result promotes R32 or establishes consciousness/AGI.
