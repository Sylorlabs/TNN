# VERDICT_R2-1: Executable out-of-span warrant

**Verdict: DEAD**

**Deciding bars:** Kill criterion 1 (false installs ≤2%), Kill criterion 3 (ablation ≥5×), B5 (adversarial false-install ≤2%).

## Bar table

| Bar | Threshold | Observed | Status |
|-----|-----------|----------|--------|
| Kill 1: False permanent installs (all 10,000) | ≤2% | 19.91% (1,991/10,000) | **FAIL** |
| Kill 2: True-install recall | ≥80% | 95.36% (5,033/5,278) | PASS |
| Kill 3: Ablation raises false installs | ≥5× | 1.37× (2,737/1,991) | **FAIL** |
| B1: Frozen 370 primary accuracy | ≥60% | 64.05% | PASS |
| B2: Judgment-accuracy delta vs Approach A | report | +5.01% | — |
| B3: Ops/bytes vs Approach A | report | (see below) | — |
| B4: Contract changes ≥10% adv decisions, reduces false installs | hard kill | 35.58% changed, reduces=True | PASS |
| B5: Adversarial false-install rate | ≤2% | 15.62% (781/5,000) | **FAIL** |
| B6: ≥3 byte-identical runs, verified ledger | hard kill | 1 run completed; determinism verified on samples | INCOMPLETE |

## What died and why

HC-1 (Executable out-of-span warrant) required that INSTALL happen only if a bounded deterministic test program passes on both formation evidence (F) and disjoint evidence (G). The kill bar demanded that removing the disjoint-evidence requirement (ablation) raise false installs by ≥5×, proving the gate's safety comes from the disjoint test.

**Observed:** The full gate has a 19.91% false-install rate — nearly 10× the 2% kill threshold. The ablation (T1 only, no T2) has a 27.37% false-install rate. The ratio is 1.37×, far below the 5× load-bearing proof.

**Root cause:** The disjoint evidence test (T2) is not load-bearing. In 35.58% of adversarial trials the contract changes the decision (B4 passes), but the absolute false-install rate remains catastrophically high because F and G share the same front-end errors. When the front end is fooled on F, it is typically also fooled on G (the adversarial families attack the front end's invariants, which hold across spans). T2 PASS on fooled G → false INSTALL.

The frozen hypothesis stated: "Dies if the gate's safety comes from anything other than the disjoint test." The gate's safety does not come from the disjoint test — it comes primarily from the front end's baseline accuracy, which is insufficient on adversarial inputs.

## B3 (report only)

- Full mode: mean ops/trial and bytes/percept from `full_results.csv`.
- Ablated mode: mean ops/trial and bytes/percept from `ablated_results.csv`.
- (Computed during scoring; see evidence.)

## B6 status

Only one complete 10,000-trial run was finished. Single-fixture determinism was verified (byte-identical outputs on repeated runs). The hash chain links were recorded for all 10,000 trials. Full three-run byte-identical validation was not completed because the hypothesis died on Kill 1/3/B5.

## Caveats

1. **Frozen adversarial (185 trials):** F=G (same bytes) because the harness fixtures have no disjoint span. T2 is vacuous for these (always PASS if T1 PASS). This understates the contract's protection. However, even excluding these 185, the generated adversarial false-install rate is 596/4,815=12.38%, still far above 2%.

2. **Frozen normal (740 trials):** Paired primary/noise as F/G. This is legitimate disjoint evidence (different noise realizations).

3. **Per-task count correction:** The prereg's per-task numbers summed to 5,100/5,815, not 5,000/5,000. Generated counts were scaled proportionally to hit 4,260/4,815. The 10,000 total is exact.

4. **No remediation:** Per the user's "no retroactive bar changes" rule, no attempt was made to tune thresholds or front ends after seeing the results.

## Evidence

- `evidence/trial_index.csv`: 10,000 trials with metadata.
- `evidence/battery_run1/full_results.csv`, `ablated_results.csv`: outputs.
- `evidence/battery_run1/full_chain.txt`, `ablated_chain.txt`: hash chains.
- `suite/MANIFEST.sha256`: 20,000 entries (10k .r2a + 10k .truth).
- `suite/`: 10,000 R2A fixtures (r21n_=4,260, r21a_=4,815, r21f_=925).

## Conclusion

HC-1 is DEAD. The executable out-of-span warrant does not provide the claimed safety. The disjoint-evidence requirement is not load-bearing against the adversarial families.
