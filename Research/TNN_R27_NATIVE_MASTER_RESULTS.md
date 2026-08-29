# R27 Native Master Architecture — Executed Results

## Evidence classes

1. **Canonical inherited evidence:** R27 verifier rerun, 33/33 PASS.
2. **Native Zag implementation evidence:** source + static/source-contract validation only because `znc` is unavailable.
3. **External reference validation:** numerical stress tests mirror the generic architecture but are **not native TNN execution**.

## Previous 0% integrated identity was invalid as a changed-view test

Source audit found the old R27-completion identity classifier was fit on `train` entities while the integrated test selected `heldout` entities. That means `same_entity_changed_view_*` was actually testing a previously unseen identity. The reported 0% therefore cannot support the claim that a known entity had 0% changed-view persistence. The old sibling integrated score was also collapsed from a global threshold rather than measured per target.

## Core visual information microscope / tournament

At dose 16, mean across the executed hidden seeds:

| Candidate | Clean | View permutation | Hard permutation | Scale/light | Occlusion | Compound |
|---|---:|---:|---:|---:|---:|---:|
| raw_ordered | 1.000 | 0.085 | 0.031 | 1.000 | 0.085 | 0.094 |
| sorted_normalized | 1.000 | 1.000 | 1.000 | 0.999 | 0.098 | 0.099 |
| pairwise_relational | 1.000 | 0.992 | 0.994 | 0.978 | 0.062 | 0.054 |
| hybrid_relational | 1.000 | 0.999 | 1.000 | 0.999 | 0.096 | 0.101 |

Conclusion: generic relational/permutation-invariant core evidence fixes the viewpoint representation collapse, but **does not solve occlusion**. Occlusion must rely on temporal entity continuity/active observation rather than pretending missing pixels contain identity. The relational core candidate is implemented in Zag as a protected-core shadow candidate; no promotion until native confirmation.

## Entity continuity experiments

- First temporal persistence reference: overall **88.12%**, occlusion/compound **75.80%**, true-switch accuracy **56.82%**.
- Multi-view set variant improved switches to about **72.1%** but reduced occlusion to about **53.9%**.
- Contextual hybrid confirmation slice regressed to about **75.8% overall / 39.5% occlusion**, so it was rolled back.

This is a real residual architecture problem; no 100% identity claim is made.

## Memory policy

With weak storage pressure the learned policy converged to `EXACT_ALL`, which is rational and was retained as a finding: TNN should not forget merely to mimic humans. Under strong resource pressure the learned policy achieved the best tested utility with roughly **2.54 storage units/episode**, **82.1% relevant recall**, and **36.7% exact-detail recall**, outperforming exact-all on the defined utility because exact storage was costly. The memory policy remains a learnable TNN decision, not a developmental phase schedule.

## Autonomous PAM Foundry

Two opcode-credit learners failed and were preserved:

- global credit learner: worse than random;
- per-op ablation learner: worse still because PAM utility is compositional.

The replacement whole-graph evolutionary shadow search achieved:

- evolved hidden mean: **252.02**
- random hidden mean: **196.09**
- gain: **+55.93**
- hidden win rate: **99.33%**

The **search mechanism**, not a particular topology, is now the canonical Foundry design in the shadow Zag source.

## Connected speech without VAD

External reference decoder using anonymous motifs + duration search:

- clean: **99.98%** vs boundary control **100.00%**
- noisy: **99.10%** vs boundary control **100.00%**
- harder duration/noise/blending challenge: **71.24%**

The near-perfect nominal result therefore **fails robustness qualification**.

## Master teaching

Adaptive Master beats matched random/diverse teaching early but not indefinitely:

| Dose | Adaptive | Random/diverse |
|---:|---:|---:|
| 8 | 68.57% | 63.87% |
| 16 | 75.31% | 69.25% |
| 32 | 82.06% | 77.51% |
| 64 | 86.54% | 82.85% |
| 128 | 87.92% | 88.34% |
| 256 | 89.94% | 89.57% |
| 512 | 89.89% | 90.93% |

This supports strong diagnostic teaching early, then diversification/withdrawal rather than permanent Master control.

## Independent sibling teaching reference

- passive description identification: **96.45%**
- with one discriminating question: **98.08%**

This is high but below 100%, and remains external reference evidence.

## Name grounding reference

Across the 10-seed reference battery: clean mean **100.00%**, late-noise mean **97.95%**. The harder speech test prevents a broad spoken-name robustness claim.

## Failure attribution / traceability

The generic failure classifier correctly separated all **7/7** designed failure classes in the external contract test: undertraining, teacher plateau, memory loss, routing miss, representation loss, interference, and resource saturation. Source contract checks confirm traced entry points for memory, PAM creation, entity resolution, world-model updates, name binding, sibling testimony, active observation, and failure diagnosis.

## Integrated qualification

**NOT RUN NATIVELY / NOT PASSED.** External component references are insufficient for promotion, and the entity/occlusion and hard-speech fronts remain below target.
